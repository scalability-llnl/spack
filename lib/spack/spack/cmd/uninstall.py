# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import sys
import itertools

import spack.cmd
import spack.environment as ev
import spack.error
import spack.package
import spack.cmd.common.arguments as arguments
import spack.repo
import spack.store
from spack.database import InstallStatuses

from llnl.util import tty
from llnl.util.tty.colify import colify

description = "remove installed packages"
section = "build"
level = "short"

error_message = """You can either:
    a) use a more specific spec, or
    b) specify the spec by its hash (e.g. `spack uninstall /hash`), or
    c) use `spack uninstall --all` to uninstall ALL matching specs.
"""

# Arguments for display_specs when we find ambiguity
display_args = {
    'long': True,
    'show_flags': False,
    'variants': False,
    'indent': 4,
}


def setup_parser(subparser):
    epilog_msg = ("Specs to be uninstalled are specified using the spec syntax"
                  " (`spack help --spec`) and can be identified by their "
                  "hashes. To remove packages that are needed only at build "
                  "time and were not explicitly installed see `spack gc -h`."
                  "\n\nWhen using the --all option ALL packages matching the "
                  "supplied specs will be uninstalled. For instance, "
                  "`spack uninstall --all libelf` uninstalls all the versions "
                  "of `libelf` currently present in Spack's store. If no spec "
                  "is supplied, all installed packages will be uninstalled. "
                  "If used in an environment, all packages in the environment "
                  "will be uninstalled.")
    subparser.epilog = epilog_msg
    subparser.add_argument(
        '-f', '--force', action='store_true', dest='force',
        help="remove regardless of whether other packages or environments "
        "depend on this one")
    arguments.add_common_arguments(
        subparser, ['recurse_dependents', 'yes_to_all', 'installed_specs'])
    subparser.add_argument(
        '-a', '--all', action='store_true', dest='all',
        help="remove ALL installed packages that match each supplied spec"
    )


def find_matching_specs(env, specs, allow_multiple_matches=False, force=False):
    """Returns a list of specs matching the not necessarily
       concretized specs given from cli

    Args:
        env (Environment): active environment, or ``None`` if there is not one
        specs (list): list of specs to be matched against installed packages
        allow_multiple_matches (bool): if True multiple matches are admitted

    Return:
        list of specs
    """
    # constrain uninstall resolution to current environment if one is active
    hashes = env.all_hashes() if env else None

    # List of specs that match expressions given via command line
    specs_from_cli = []
    has_errors = False
    for spec in specs:
        install_query = [InstallStatuses.INSTALLED, InstallStatuses.DEPRECATED]
        matching = spack.store.db.query_local(spec, hashes=hashes,
                                              installed=install_query)
        # For each spec provided, make sure it refers to only one package.
        # Fail and ask user to be unambiguous if it doesn't
        if not allow_multiple_matches and len(matching) > 1:
            tty.error('{0} matches multiple packages:'.format(spec))
            sys.stderr.write('\n')
            spack.cmd.display_specs(matching, output=sys.stderr,
                                    **display_args)
            sys.stderr.write('\n')
            sys.stderr.flush()
            has_errors = True

        # No installed package matches the query
        if len(matching) == 0 and spec is not any:
            if env:
                pkg_type = "packages in environment '%s'" % env.name
            else:
                pkg_type = 'installed packages'
            tty.die('{0} does not match any {1}.'.format(spec, pkg_type))

        specs_from_cli.extend(matching)

    if has_errors:
        tty.die(error_message)

    return specs_from_cli


def installed_dependents(specs, env):
    """Map each spec to a list of its installed dependents.

    Args:
        specs (list): list of Specs
        env (Environment): the active environment, or None

    Returns:
        (tuple of dicts): two mappings: one from specs to their dependent
            environments in the active environment (or global scope if
            there is no environment), and one from specs to their
            dependents in *inactive* environments (empty if there is no
            environment

    """
    active_dpts = {}
    inactive_dpts = {}

    env_hashes = set(env.all_hashes()) if env else set()

    all_specs_in_db = spack.store.db.query()

    for spec in specs:
        installed = [x for x in all_specs_in_db if spec in x]

        # separate installed dependents into dpts in this environment and
        # dpts that are outside this environment
        for dpt in installed:
            if dpt not in specs:
                if not env or dpt.dag_hash() in env_hashes:
                    active_dpts.setdefault(spec, set()).add(dpt)
                else:
                    inactive_dpts.setdefault(spec, set()).add(dpt)

    return active_dpts, inactive_dpts


def dependent_environments(specs):
    """Map each spec to environments that depend on it.

    Args:
        specs (list): list of Specs
    Returns:
        (dict): mapping from spec to lists of dependent Environments

    """
    dependents = {}
    for env in ev.all_environments():
        hashes = set(env.all_hashes())
        for spec in specs:
            if spec.dag_hash() in hashes:
                dependents.setdefault(spec, []).append(env)
    return dependents


def inactive_dependent_environments(spec_envs):
    """Strip the active environment from a dependent map.

    Take the output of ``dependent_environment()`` and remove the active
    environment from all mappings.  Remove any specs in the map that now
    have no dependent environments.  Return the result.

    Args:
        (dict): mapping from spec to lists of dependent Environments
    Returns:
        (dict): mapping from spec to lists of *inactive* dependent Environments
    """
    spec_inactive_envs = {}
    for spec, de_list in spec_envs.items():
        inactive = [de for de in de_list if not de.active]
        if inactive:
            spec_inactive_envs[spec] = inactive

    return spec_inactive_envs


def _remove_from_env(spec, env):
    """Remove a spec from an environment if it is a root."""
    try:
        # try removing the spec from the current active
        # environment. this will fail if the spec is not a root
        env.remove(spec, force=True)
    except ev.SpackEnvironmentError:
        pass  # ignore non-root specs


def do_uninstall(env, specs, force):
    """Uninstalls all the specs in a list.

    Args:
        env (Environment): active environment, or ``None`` if there is not one
        specs (list): list of specs to be uninstalled
        force (bool): force uninstallation (boolean)
    """
    packages = []
    for item in specs:
        try:
            # should work if package is known to spack
            packages.append(item.package)
        except spack.repo.UnknownEntityError:
            # The package.py file has gone away -- but still
            # want to uninstall.
            spack.package.Package.uninstall_by_spec(item, force=True)

    # A package is ready to be uninstalled when nothing else references it,
    # unless we are requested to force uninstall it.
    is_ready = lambda x: not spack.store.db.query_by_spec_hash(x)[1].ref_count
    if force:
        is_ready = lambda x: True

    while packages:
        ready = [x for x in packages if is_ready(x.spec.dag_hash())]
        if not ready:
            msg = 'unexpected error [cannot proceed uninstalling specs with' \
                  ' remaining dependents {0}]'
            msg = msg.format(', '.join(x.name for x in packages))
            raise spack.error.SpackError(msg)

        packages = [x for x in packages if x not in ready]
        for item in ready:
            item.do_uninstall(force=force)


def get_uninstall_list(args, specs, env):
    # Gets the list of installed specs that match the ones give via cli
    # args.all takes care of the case where '-a' is given in the cli
    uninstall_list = find_matching_specs(env, specs, args.all, args.force)

    # Takes care of '-R'
    active_dpts, inactive_dpts = installed_dependents(uninstall_list, env)

    # if we are in the global scope, we complain if you try to remove a
    # spec that's in an environment.  If we're in an environment, we'll
    # just *remove* it from the environment, so we ignore this
    # error when *in* an environment
    spec_envs = dependent_environments(uninstall_list)
    spec_envs = inactive_dependent_environments(spec_envs)

    # Process spec_dependents and update uninstall_list
    has_error = not args.force and (
        (active_dpts and not args.dependents)  # dependents in the current env
        or (not env and spec_envs)  # there are environments that need specs
    )

    # say why each problem spec is needed
    if has_error:
        specs = set(active_dpts)
        if not env:
            specs.update(set(spec_envs))  # environments depend on this

        for i, spec in enumerate(sorted(specs)):
            # space out blocks of reasons
            if i > 0:
                print()

            spec_format = '{name}{@version}{%compiler}{/hash:7}'
            tty.info("Will not uninstall %s" % spec.cformat(spec_format),
                     format='*r')

            dependents = active_dpts.get(spec)
            if dependents:
                print('The following packages depend on it:')
                spack.cmd.display_specs(dependents, **display_args)

            if not env:
                envs = spec_envs.get(spec)
                if envs:
                    print('It is used by the following environments:')
                    colify([e.name for e in envs], indent=4)

        msgs = []
        if active_dpts:
            msgs.append(
                'use `spack uninstall --dependents` to remove dependents too')
        if spec_envs:
            msgs.append(
                'use `spack -e ENV remove` to remove from environment ENV')
        print()
        tty.die('There are still dependents.', *msgs)

    elif args.dependents:
        for spec, lst in active_dpts.items():
            uninstall_list.extend(lst)
        uninstall_list = list(set(uninstall_list))

    # only force-remove (don't completely uninstall) specs that still
    # have external dependent envs or pkgs
    removes = set(inactive_dpts)
    if env:
        removes.update(spec_envs)

    # remove anything in removes from the uninstall list
    uninstall_list = set(uninstall_list) - removes

    return uninstall_list, removes


def uninstall_specs(args, specs):
    env = ev.get_env(args, 'uninstall')

    uninstall_list, remove_list = get_uninstall_list(args, specs, env)
    anything_to_do = set(uninstall_list).union(set(remove_list))

    if not anything_to_do:
        tty.warn('There are no package to uninstall.')
        return

    if not args.yes_to_all:
        confirm_removal(anything_to_do)

    if env:
        # Remove all the specs that are supposed to be uninstalled or just
        # removed.
        with env.write_transaction():
            for spec in itertools.chain(remove_list, uninstall_list):
                _remove_from_env(spec, env)
            env.write()

    # Uninstall everything on the list
    do_uninstall(env, uninstall_list, args.force)


def confirm_removal(specs):
    """Display the list of specs to be removed and ask for confirmation.

    Args:
        specs (list): specs to be removed
    """
    tty.msg('The following packages will be uninstalled:\n')
    spack.cmd.display_specs(specs, **display_args)
    print('')
    answer = tty.get_yes_or_no('Do you want to proceed?', default=False)
    if not answer:
        tty.msg('Aborting uninstallation')
        sys.exit(0)


def uninstall(parser, args):
    if not args.specs and not args.all:
        tty.die('uninstall requires at least one package argument.',
                '  Use `spack uninstall --all` to uninstall ALL packages.')

    # [any] here handles the --all case by forcing all specs to be returned
    specs = spack.cmd.parse_specs(args.specs) if args.specs else [any]
    uninstall_specs(args, specs)
