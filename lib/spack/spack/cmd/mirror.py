# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import llnl.util.tty as tty
from llnl.util.tty.colify import colify

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.concretize
import spack.config
import spack.environment as ev
import spack.mirror
import spack.repo
import spack.util.url as url_util
import spack.util.web as web_util

from spack.spec import Spec
from spack.error import SpackError
from spack.util.spack_yaml import syaml_dict

description = "manage mirrors (source and binary)"
section = "config"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ['no_checksum', 'deprecated'])

    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='mirror_command')

    # Create
    create_parser = sp.add_parser('create', help=mirror_create.__doc__)
    create_parser.add_argument('-d', '--directory', default=None,
                               help="directory in which to create mirror")

    create_parser.add_argument(
        '-a', '--all', action='store_true',
        help="mirror all versions of all packages in Spack, or all packages"
             " in the current environment if there is an active environment"
             " (this requires significant time and space)")
    create_parser.add_argument(
        '-f', '--file', help="file with specs of packages to put in mirror")
    create_parser.add_argument(
        '--exclude-file',
        help="specs which Spack should not try to add to a mirror"
             " (listed in a file, one per line)")
    create_parser.add_argument(
        '--exclude-specs',
        help="specs which Spack should not try to add to a mirror"
             " (specified on command line)")

    create_parser.add_argument(
        '--skip-unstable-versions', action='store_true',
        help="don't cache versions unless they identify a stable (unchanging)"
             " source code")
    create_parser.add_argument(
        '-D', '--dependencies', action='store_true',
        help="also fetch all dependencies")
    create_parser.add_argument(
        '-n', '--versions-per-spec',
        help="the number of versions to fetch for each spec, choose 'all' to"
             " retrieve all versions of each package")
    arguments.add_common_arguments(create_parser, ['specs'])

    # Destroy
    destroy_parser = sp.add_parser('destroy', help=mirror_destroy.__doc__)

    destroy_target = destroy_parser.add_mutually_exclusive_group(required=True)
    destroy_target.add_argument('-m', '--mirror-name',
                                metavar='mirror_name',
                                type=str,
                                help="find mirror to destroy by name")
    destroy_target.add_argument('--mirror-url',
                                metavar='mirror_url',
                                type=str,
                                help="find mirror to destroy by url")

    # used to construct scope arguments below
    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar

    # Add
    add_parser = sp.add_parser('add', help=mirror_add.__doc__)
    add_parser.add_argument(
        'name', help="mnemonic name for mirror", metavar="mirror")
    add_parser.add_argument(
        'url', help="url of mirror directory from 'spack mirror create'")
    add_parser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.config.default_modify_scope(),
        help="configuration scope to modify")

    # Remove
    remove_parser = sp.add_parser('remove', aliases=['rm'],
                                  help=mirror_remove.__doc__)
    remove_parser.add_argument(
        'name', help="mnemonic name for mirror", metavar="mirror")
    remove_parser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.config.default_modify_scope(),
        help="configuration scope to modify")

    # Set-Url
    set_url_parser = sp.add_parser('set-url', help=mirror_set_url.__doc__)
    set_url_parser.add_argument(
        'name', help="mnemonic name for mirror", metavar="mirror")
    set_url_parser.add_argument(
        'url', help="url of mirror directory from 'spack mirror create'")
    set_url_parser.add_argument(
        '--push', action='store_true',
        help="set only the URL used for uploading new packages")
    set_url_parser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.config.default_modify_scope(),
        help="configuration scope to modify")

    # List
    list_parser = sp.add_parser('list', help=mirror_list.__doc__)
    list_parser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.config.default_list_scope(),
        help="configuration scope to read from")


def mirror_add(args):
    """Add a mirror to Spack."""
    url = url_util.format(args.url)

    mirrors = spack.config.get('mirrors', scope=args.scope)
    if not mirrors:
        mirrors = syaml_dict()

    if args.name in mirrors:
        tty.die("Mirror with name %s already exists." % args.name)

    items = [(n, u) for n, u in mirrors.items()]
    items.insert(0, (args.name, url))
    mirrors = syaml_dict(items)
    spack.config.set('mirrors', mirrors, scope=args.scope)


def mirror_remove(args):
    """Remove a mirror by name."""
    name = args.name

    mirrors = spack.config.get('mirrors', scope=args.scope)
    if not mirrors:
        mirrors = syaml_dict()

    if name not in mirrors:
        tty.die("No mirror with name %s" % name)

    old_value = mirrors.pop(name)
    spack.config.set('mirrors', mirrors, scope=args.scope)

    debug_msg_url = "url %s"
    debug_msg = ["Removed mirror %s with"]
    values = [name]

    try:
        fetch_value = old_value['fetch']
        push_value = old_value['push']

        debug_msg.extend(("fetch", debug_msg_url, "and push", debug_msg_url))
        values.extend((fetch_value, push_value))
    except TypeError:
        debug_msg.append(debug_msg_url)
        values.append(old_value)

    tty.debug(" ".join(debug_msg) % tuple(values))
    tty.msg("Removed mirror %s." % name)


def mirror_set_url(args):
    """Change the URL of a mirror."""
    url = url_util.format(args.url)

    mirrors = spack.config.get('mirrors', scope=args.scope)
    if not mirrors:
        mirrors = syaml_dict()

    if args.name not in mirrors:
        tty.die("No mirror found with name %s." % args.name)

    entry = mirrors[args.name]

    try:
        fetch_url = entry['fetch']
        push_url = entry['push']
    except TypeError:
        fetch_url, push_url = entry, entry

    changes_made = False

    if args.push:
        changes_made = changes_made or push_url != url
        push_url = url
    else:
        changes_made = (
            changes_made or fetch_url != push_url or push_url != url)

        fetch_url, push_url = url, url

    items = [
        (
            (n, u)
            if n != args.name else (
                (n, {"fetch": fetch_url, "push": push_url})
                if fetch_url != push_url else (n, fetch_url)
            )
        )
        for n, u in mirrors.items()
    ]

    mirrors = syaml_dict(items)
    spack.config.set('mirrors', mirrors, scope=args.scope)

    if changes_made:
        tty.msg(
            "Changed%s url for mirror %s." %
            ((" (push)" if args.push else ""), args.name))
    else:
        tty.msg("Url already set for mirror %s." % args.name)


def mirror_list(args):
    """Print out available mirrors to the console."""

    mirrors = spack.mirror.MirrorCollection(scope=args.scope)
    if not mirrors:
        tty.msg("No mirrors configured.")
        return

    mirrors.display()


def _read_specs_from_file(filename):
    specs = []
    with open(filename, "r") as stream:
        for i, string in enumerate(stream):
            try:
                s = Spec(string)
                s.package
                specs.append(s)
            except SpackError as e:
                tty.debug(e)
                tty.die("Parse error in %s, line %d:" % (filename, i + 1),
                        ">>> " + string, str(e))
    return specs


def _determine_specs_to_mirror(args):
    if args.specs and args.all:
        raise SpackError("Cannot specify specs on command line if you"
                         " chose to mirror all specs with '--all'")
    elif args.file and args.all:
        raise SpackError("Cannot specify specs with a file ('-f') if you"
                         " chose to mirror all specs with '--all'")

    if not args.versions_per_spec:
        num_versions = 1
    elif args.versions_per_spec == 'all':
        num_versions = 'all'
    else:
        try:
            num_versions = int(args.versions_per_spec)
        except ValueError:
            raise SpackError(
                "'--versions-per-spec' must be a number or 'all',"
                " got '{0}'".format(args.versions_per_spec))

    # try to parse specs from the command line first.
    with spack.concretize.disable_compiler_existence_check():
        specs = spack.cmd.parse_specs(args.specs, concretize=True)

        # If there is a file, parse each line as a spec and add it to the list.
        if args.file:
            if specs:
                tty.die("Cannot pass specs on the command line with --file.")
            specs = _read_specs_from_file(args.file)

        env_specs = None
        if not specs:
            # If nothing is passed, use environment or all if no active env
            if not args.all:
                tty.die("No packages were specified.",
                        "To mirror all packages, use the '--all' option"
                        " (this will require significant time and space).")

            env = ev.get_env(args, 'mirror')
            if env:
                env_specs = env.all_specs()
            else:
                specs = [Spec(n) for n in spack.repo.all_package_names()]
        else:
            # If the user asked for dependencies, traverse spec DAG get them.
            if args.dependencies:
                new_specs = set()
                for spec in specs:
                    spec.concretize()
                    for s in spec.traverse():
                        new_specs.add(s)
                specs = list(new_specs)

            # Skip external specs, as they are already installed
            external_specs = [s for s in specs if s.external]
            specs = [s for s in specs if not s.external]

            for spec in external_specs:
                msg = 'Skipping {0} as it is an external spec.'
                tty.msg(msg.format(spec.cshort_spec))

        if env_specs:
            if args.versions_per_spec:
                tty.warn("Ignoring '--versions-per-spec' for mirroring specs"
                         " in environment.")
            mirror_specs = env_specs
        else:
            if num_versions == 'all':
                mirror_specs = spack.mirror.get_all_versions(specs)
            else:
                mirror_specs = spack.mirror.get_matching_versions(
                    specs, num_versions=num_versions)
            mirror_specs.sort(
                key=lambda s: (s.name, s.version))

    exclude_specs = []
    if args.exclude_file:
        exclude_specs.extend(_read_specs_from_file(args.exclude_file))
    if args.exclude_specs:
        exclude_specs.extend(
            spack.cmd.parse_specs(str(args.exclude_specs).split()))
    if exclude_specs:
        mirror_specs = list(
            x for x in mirror_specs
            if not any(x.satisfies(y, strict=True) for y in exclude_specs))

    return mirror_specs


def mirror_create(args):
    """Create a directory to be used as a spack mirror, and fill it with
       package archives."""
    mirror_specs = _determine_specs_to_mirror(args)

    mirror = spack.mirror.Mirror(
        args.directory or spack.config.get('config:source_cache'))

    directory = url_util.format(mirror.push_url)

    existed = web_util.url_exists(directory)

    # Actually do the work to create the mirror
    present, mirrored, error = spack.mirror.create(
        directory, mirror_specs, args.skip_unstable_versions)
    p, m, e = len(present), len(mirrored), len(error)

    verb = "updated" if existed else "created"
    tty.msg(
        "Successfully %s mirror in %s" % (verb, directory),
        "Archive stats:",
        "  %-4d already present"  % p,
        "  %-4d added"            % m,
        "  %-4d failed to fetch." % e)
    if error:
        tty.error("Failed downloads:")
        colify(s.cformat("{name}{@version}") for s in error)
        sys.exit(1)


def mirror_destroy(args):
    """Given a url, recursively delete everything under it."""
    mirror_url = None

    if args.mirror_name:
        result = spack.mirror.MirrorCollection().lookup(args.mirror_name)
        mirror_url = result.push_url
    elif args.mirror_url:
        mirror_url = args.mirror_url

    web_util.remove_url(mirror_url, recursive=True)


def mirror(parser, args):
    action = {'create': mirror_create,
              'destroy': mirror_destroy,
              'add': mirror_add,
              'remove': mirror_remove,
              'rm': mirror_remove,
              'set-url': mirror_set_url,
              'list': mirror_list}

    if args.no_checksum:
        spack.config.set('config:checksum', False, scope='command_line')

    if args.deprecated:
        spack.config.set('config:deprecated', True, scope='command_line')

    action[args.mirror_command](args)
