# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from __future__ import print_function

import argparse
import os
import re
import sys
from collections import defaultdict, namedtuple

import llnl.util.filesystem
import llnl.util.tty as tty
import llnl.util.tty.colify as colify
import six
import spack
import spack.cmd
import spack.cmd.common.arguments
import spack.error
import spack.util.environment
import spack.util.spack_yaml as syaml

description = "manage external packages in Spack configuration"
section = "config"
level = "short"


def setup_parser(subparser):
    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='external_command')

    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar

    find_parser = sp.add_parser(
        'find', help='add external packages to packages.yaml'
    )
    find_parser.add_argument(
        '--not-buildable', action='store_true', default=False,
        help="packages with detected externals won't be built with Spack")
    find_parser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.config.default_modify_scope('packages'),
        help="configuration scope to modify")
    spack.cmd.common.arguments.add_common_arguments(find_parser, ['tags'])
    find_parser.add_argument('packages', nargs=argparse.REMAINDER)

    sp.add_parser(
        'list', help='list detectable packages, by repository and name'
    )


def is_executable(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)


def _get_system_executables():
    """Get the paths of all executables available from the current PATH.

    For convenience, this is constructed as a dictionary where the keys are
    the executable paths and the values are the names of the executables
    (i.e. the basename of the executable path).

    There may be multiple paths with the same basename. In this case it is
    assumed there are two different instances of the executable.
    """
    path_hints = spack.util.environment.get_path('PATH')
    search_paths = llnl.util.filesystem.search_paths_for_executables(
        *path_hints)

    path_to_exe = {}
    # Reverse order of search directories so that an exe in the first PATH
    # entry overrides later entries
    for search_path in reversed(search_paths):
        for exe in os.listdir(search_path):
            exe_path = os.path.join(search_path, exe)
            if is_executable(exe_path):
                path_to_exe[exe_path] = exe
    return path_to_exe


ExternalPackageEntry = namedtuple(
    'ExternalPackageEntry',
    ['spec', 'base_dir'])


def _generate_pkg_config(external_pkg_entries):
    """Generate config according to the packages.yaml schema for a single
    package.

    This does not generate the entire packages.yaml. For example, given some
    external entries for the CMake package, this could return::

        {
            'externals': [{
                'spec': 'cmake@3.17.1',
                'prefix': '/opt/cmake-3.17.1/'
            }, {
                'spec': 'cmake@3.16.5',
                'prefix': '/opt/cmake-3.16.5/'
            }]
       }
    """

    pkg_dict = syaml.syaml_dict()
    pkg_dict['externals'] = []
    for e in external_pkg_entries:
        if not _spec_is_valid(e.spec):
            continue

        external_items = [('spec', str(e.spec)), ('prefix', e.base_dir)]
        if e.spec.external_modules:
            external_items.append(('modules', e.spec.external_modules))

        if e.spec.extra_attributes:
            external_items.append(
                ('extra_attributes',
                 syaml.syaml_dict(e.spec.extra_attributes.items()))
            )

        # external_items.extend(e.spec.extra_attributes.items())
        pkg_dict['externals'].append(
            syaml.syaml_dict(external_items)
        )

    return pkg_dict


def _spec_is_valid(spec):
    try:
        str(spec)
    except spack.error.SpackError:
        # It is assumed here that we can at least extract the package name from
        # the spec so we can look up the implementation of
        # determine_spec_details
        tty.warn('Constructed spec for {0} does not have a string'
                 ' representation'.format(spec.name))
        return False

    try:
        spack.spec.Spec(str(spec))
    except spack.error.SpackError:
        tty.warn('Constructed spec has a string representation but the string'
                 ' representation does not evaluate to a valid spec: {0}'
                 .format(str(spec)))
        return False

    return True


def external_find(args):
    # Construct the list of possible packages to be detected
    packages_to_check = []

    # Add the packages that have been required explicitly
    if args.packages:
        packages_to_check = list(spack.repo.get(pkg) for pkg in args.packages)
        if args.tags:
            allowed = set(spack.repo.path.packages_with_tags(*args.tags))
            packages_to_check = [x for x in packages_to_check if x in allowed]

    if args.tags and not packages_to_check:
        # If we arrived here we didn't have any explicit package passed
        # as argument, which means to search all packages.
        # Since tags are cached it's much faster to construct what we need
        # to search directly, rather than filtering after the fact
        packages_to_check = [
            spack.repo.get(pkg) for pkg in
            spack.repo.path.packages_with_tags(*args.tags)
        ]

    # If the list of packages is empty, search for every possible package
    if not args.tags and not packages_to_check:
        packages_to_check = spack.repo.path.all_packages()

    pkg_to_entries = _get_external_packages(packages_to_check)
    new_entries = _update_pkg_config(
        args.scope, pkg_to_entries, args.not_buildable
    )
    if new_entries:
        path = spack.config.config.get_config_filename(args.scope, 'packages')
        msg = ('The following specs have been detected on this system '
               'and added to {0}')
        tty.msg(msg.format(path))
        spack.cmd.display_specs(new_entries)
    else:
        tty.msg('No new external packages detected')


def _group_by_prefix(paths):
    groups = defaultdict(set)
    for p in paths:
        groups[os.path.dirname(p)].add(p)
    return groups.items()


def _convert_to_iterable(single_val_or_multiple):
    x = single_val_or_multiple
    if x is None:
        return []
    elif isinstance(x, six.string_types):
        return [x]
    elif isinstance(x, spack.spec.Spec):
        # Specs are iterable, but a single spec should be converted to a list
        return [x]

    try:
        iter(x)
        return x
    except TypeError:
        return [x]


def _determine_base_dir(prefix):
    # Given a prefix where an executable is found, assuming that prefix
    # contains /bin/, strip off the 'bin' directory and all subsequent
    # directories to get a Spack-compatible prefix
    assert os.path.isdir(prefix)

    components = prefix.split(os.sep)
    if 'bin' not in components:
        return None
    idx = components.index('bin')
    return os.sep.join(components[:idx])


def _get_predefined_externals():
    # Pull from all scopes when looking for preexisting external package
    # entries
    pkg_config = spack.config.get('packages')
    already_defined_specs = set()
    for pkg_name, per_pkg_cfg in pkg_config.items():
        for item in per_pkg_cfg.get('externals', []):
            already_defined_specs.add(spack.spec.Spec(item['spec']))
    return already_defined_specs


def _update_pkg_config(scope, pkg_to_entries, not_buildable):
    predefined_external_specs = _get_predefined_externals()

    pkg_to_cfg, all_new_specs = {}, []
    for pkg_name, ext_pkg_entries in pkg_to_entries.items():
        new_entries = list(
            e for e in ext_pkg_entries
            if (e.spec not in predefined_external_specs))

        pkg_config = _generate_pkg_config(new_entries)
        all_new_specs.extend([
            spack.spec.Spec(x['spec']) for x in pkg_config.get('externals', [])
        ])
        if not_buildable:
            pkg_config['buildable'] = False
        pkg_to_cfg[pkg_name] = pkg_config

    pkgs_cfg = spack.config.get('packages', scope=scope)

    pkgs_cfg = spack.config.merge_yaml(pkgs_cfg, pkg_to_cfg)
    spack.config.set('packages', pkgs_cfg, scope=scope)

    return all_new_specs


def _get_external_packages(packages_to_check, system_path_to_exe=None):
    if not system_path_to_exe:
        system_path_to_exe = _get_system_executables()

    exe_pattern_to_pkgs = defaultdict(list)
    for pkg in packages_to_check:
        if hasattr(pkg, 'executables'):
            for exe in pkg.executables:
                exe_pattern_to_pkgs[exe].append(pkg)

    pkg_to_found_exes = defaultdict(set)
    for exe_pattern, pkgs in exe_pattern_to_pkgs.items():
        compiled_re = re.compile(exe_pattern)
        for path, exe in system_path_to_exe.items():
            if compiled_re.search(exe):
                for pkg in pkgs:
                    pkg_to_found_exes[pkg].add(path)

    pkg_to_entries = defaultdict(list)
    resolved_specs = {}  # spec -> exe found for the spec

    for pkg, exes in pkg_to_found_exes.items():
        if not hasattr(pkg, 'determine_spec_details'):
            tty.warn("{0} must define 'determine_spec_details' in order"
                     " for Spack to detect externally-provided instances"
                     " of the package.".format(pkg.name))
            continue

        # TODO: iterate through this in a predetermined order (e.g. by package
        # name) to get repeatable results when there are conflicts. Note that
        # if we take the prefixes returned by _group_by_prefix, then consider
        # them in the order that they appear in PATH, this should be sufficient
        # to get repeatable results.
        for prefix, exes_in_prefix in _group_by_prefix(exes):
            # TODO: multiple instances of a package can live in the same
            # prefix, and a package implementation can return multiple specs
            # for one prefix, but without additional details (e.g. about the
            # naming scheme which differentiates them), the spec won't be
            # usable.
            specs = _convert_to_iterable(
                pkg.determine_spec_details(prefix, exes_in_prefix))

            if not specs:
                tty.debug(
                    'The following executables in {0} were decidedly not '
                    'part of the package {1}: {2}'
                    .format(prefix, pkg.name, ', '.join(
                        _convert_to_iterable(exes_in_prefix)))
                )

            for spec in specs:
                pkg_prefix = _determine_base_dir(prefix)

                if not pkg_prefix:
                    tty.debug("{0} does not end with a 'bin/' directory: it"
                              " cannot be added as a Spack package"
                              .format(prefix))
                    continue

                if spec in resolved_specs:
                    prior_prefix = ', '.join(
                        _convert_to_iterable(resolved_specs[spec]))

                    tty.debug(
                        "Executables in {0} and {1} are both associated"
                        " with the same spec {2}"
                        .format(prefix, prior_prefix, str(spec)))
                    continue
                else:
                    resolved_specs[spec] = prefix

                try:
                    spec.validate_detection()
                except Exception as e:
                    msg = ('"{0}" has been detected on the system but will '
                           'not be added to packages.yaml [reason={1}]')
                    tty.warn(msg.format(spec, str(e)))
                    continue

                if spec.external_path:
                    pkg_prefix = spec.external_path

                pkg_to_entries[pkg.name].append(
                    ExternalPackageEntry(spec=spec, base_dir=pkg_prefix))

    return pkg_to_entries


def external_list(args):
    # Trigger a read of all packages, might take a long time.
    list(spack.repo.path.all_packages())
    # Print all the detectable packages
    tty.msg("Detectable packages per repository")
    for namespace, pkgs in sorted(spack.package.detectable_packages.items()):
        print("Repository:", namespace)
        colify.colify(pkgs, indent=4, output=sys.stdout)


def external(parser, args):
    action = {'find': external_find, 'list': external_list}
    action[args.external_command](args)
