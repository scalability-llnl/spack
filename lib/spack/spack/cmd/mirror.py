# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import llnl.util.lang as lang
import llnl.util.tty as tty
import llnl.util.tty.colify as colify

import spack.caches
import spack.cmd
import spack.concretize
import spack.config
import spack.environment as ev
import spack.mirror
import spack.repo
import spack.spec
import spack.util.web as web_util
from spack.cmd.common import arguments
from spack.error import SpackError

description = "manage mirrors (source and binary)"
section = "config"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ["no_checksum"])

    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="mirror_command")

    # Create
    create_parser = sp.add_parser("create", help=mirror_create.__doc__)
    create_parser.add_argument(
        "-d", "--directory", default=None, help="directory in which to create mirror"
    )

    create_parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="mirror all versions of all packages in Spack, or all packages"
        " in the current environment if there is an active environment"
        " (this requires significant time and space)",
    )
    create_parser.add_argument("-f", "--file", help="file with specs of packages to put in mirror")
    create_parser.add_argument(
        "--exclude-file",
        help="specs which Spack should not try to add to a mirror"
        " (listed in a file, one per line)",
    )
    create_parser.add_argument(
        "--exclude-specs",
        help="specs which Spack should not try to add to a mirror (specified on command line)",
    )

    create_parser.add_argument(
        "--skip-unstable-versions",
        action="store_true",
        help="don't cache versions unless they identify a stable (unchanging) source code",
    )
    create_parser.add_argument(
        "-D", "--dependencies", action="store_true", help="also fetch all dependencies"
    )
    create_parser.add_argument(
        "-n",
        "--versions-per-spec",
        help="the number of versions to fetch for each spec, choose 'all' to"
        " retrieve all versions of each package",
    )
    create_parser.add_argument(
        "--private",
        action="store_true",
        help="for a private mirror, include non-redistributable packages",
    )
    arguments.add_common_arguments(create_parser, ["specs"])
    arguments.add_concretizer_args(create_parser)

    # Destroy
    destroy_parser = sp.add_parser("destroy", help=mirror_destroy.__doc__)

    destroy_target = destroy_parser.add_mutually_exclusive_group(required=True)
    destroy_target.add_argument(
        "-m",
        "--mirror-name",
        metavar="mirror_name",
        type=str,
        help="find mirror to destroy by name",
    )
    destroy_target.add_argument(
        "--mirror-url", metavar="mirror_url", type=str, help="find mirror to destroy by url"
    )

    # Add
    add_parser = sp.add_parser("add", help=mirror_add.__doc__)
    add_parser.add_argument("name", help="mnemonic name for mirror", metavar="mirror")
    add_parser.add_argument("url", help="url of mirror directory from 'spack mirror create'")
    add_parser.add_argument(
        "--scope",
        action=arguments.ConfigScope,
        default=lambda: spack.config.default_modify_scope(),
        help="configuration scope to modify",
    )
    add_parser.add_argument(
        "--type",
        action="append",
        choices=("binary", "source"),
        help=(
            "specify the mirror type: for both binary "
            "and source use `--type binary --type source` (default)"
        ),
    )
    add_parser.add_argument(
        "--autopush",
        action="store_true",
        help=("set mirror to push automatically after installation"),
    )
    add_parser_signed = add_parser.add_mutually_exclusive_group(required=False)
    add_parser_signed.add_argument(
        "--unsigned",
        help="do not require signing and signature verification when pushing and installing from "
        "this build cache",
        action="store_false",
        default=None,
        dest="signed",
    )
    add_parser_signed.add_argument(
        "--signed",
        help="require signing and signature verification when pushing and installing from this "
        "build cache",
        action="store_true",
        default=None,
        dest="signed",
    )
    arguments.add_connection_args(add_parser, False)
    # Remove
    remove_parser = sp.add_parser("remove", aliases=["rm"], help=mirror_remove.__doc__)
    remove_parser.add_argument("name", help="mnemonic name for mirror", metavar="mirror")
    remove_parser.add_argument(
        "--scope",
        action=arguments.ConfigScope,
        default=lambda: spack.config.default_modify_scope(),
        help="configuration scope to modify",
    )

    # Set-Url
    set_url_parser = sp.add_parser("set-url", help=mirror_set_url.__doc__)
    set_url_parser.add_argument("name", help="mnemonic name for mirror", metavar="mirror")
    set_url_parser.add_argument("url", help="url of mirror directory from 'spack mirror create'")
    set_url_push_or_fetch = set_url_parser.add_mutually_exclusive_group(required=False)
    set_url_push_or_fetch.add_argument(
        "--push", action="store_true", help="set only the URL used for uploading"
    )
    set_url_push_or_fetch.add_argument(
        "--fetch", action="store_true", help="set only the URL used for downloading"
    )
    set_url_parser.add_argument(
        "--scope",
        action=arguments.ConfigScope,
        default=lambda: spack.config.default_modify_scope(),
        help="configuration scope to modify",
    )
    arguments.add_connection_args(set_url_parser, False)

    # Set
    set_parser = sp.add_parser("set", help=mirror_set.__doc__)
    set_parser.add_argument("name", help="mnemonic name for mirror", metavar="mirror")
    set_parser_push_or_fetch = set_parser.add_mutually_exclusive_group(required=False)
    set_parser_push_or_fetch.add_argument(
        "--push", action="store_true", help="modify just the push connection details"
    )
    set_parser_push_or_fetch.add_argument(
        "--fetch", action="store_true", help="modify just the fetch connection details"
    )
    set_parser.add_argument(
        "--type",
        action="append",
        choices=("binary", "source"),
        help=(
            "specify the mirror type: for both binary "
            "and source use `--type binary --type source`"
        ),
    )
    set_parser.add_argument("--url", help="url of mirror directory from 'spack mirror create'")
    set_parser_autopush = set_parser.add_mutually_exclusive_group(required=False)
    set_parser_autopush.add_argument(
        "--autopush",
        help="set mirror to push automatically after installation",
        action="store_true",
        default=None,
        dest="autopush",
    )
    set_parser_autopush.add_argument(
        "--no-autopush",
        help="set mirror to not push automatically after installation",
        action="store_false",
        default=None,
        dest="autopush",
    )
    set_parser_unsigned = set_parser.add_mutually_exclusive_group(required=False)
    set_parser_unsigned.add_argument(
        "--unsigned",
        help="do not require signing and signature verification when pushing and installing from "
        "this build cache",
        action="store_false",
        default=None,
        dest="signed",
    )
    set_parser_unsigned.add_argument(
        "--signed",
        help="require signing and signature verification when pushing and installing from this "
        "build cache",
        action="store_true",
        default=None,
        dest="signed",
    )
    set_parser.add_argument(
        "--scope",
        action=arguments.ConfigScope,
        default=lambda: spack.config.default_modify_scope(),
        help="configuration scope to modify",
    )
    arguments.add_connection_args(set_parser, False)

    # List
    list_parser = sp.add_parser("list", help=mirror_list.__doc__)
    list_parser.add_argument(
        "--scope", action=arguments.ConfigScope, help="configuration scope to read from"
    )


def mirror_add(args):
    """add a mirror to Spack"""
    if (
        args.s3_access_key_id
        or args.s3_access_key_secret
        or args.s3_access_token
        or args.s3_profile
        or args.s3_endpoint_url
        or args.type
        or args.oci_username
        or args.oci_password
        or args.autopush
        or args.signed is not None
    ):
        connection = {"url": args.url}
        if args.s3_access_key_id and args.s3_access_key_secret:
            connection["access_pair"] = [args.s3_access_key_id, args.s3_access_key_secret]
        if args.s3_access_token:
            connection["access_token"] = args.s3_access_token
        if args.s3_profile:
            connection["profile"] = args.s3_profile
        if args.s3_endpoint_url:
            connection["endpoint_url"] = args.s3_endpoint_url
        if args.oci_username and args.oci_password:
            connection["access_pair"] = [args.oci_username, args.oci_password]
        if args.type:
            connection["binary"] = "binary" in args.type
            connection["source"] = "source" in args.type
        if args.autopush:
            connection["autopush"] = args.autopush
        if args.signed is not None:
            connection["signed"] = args.signed
        mirror = spack.mirror.Mirror(connection, name=args.name)
    else:
        mirror = spack.mirror.Mirror(args.url, name=args.name)
    spack.mirror.add(mirror, args.scope)


def mirror_remove(args):
    """remove a mirror by name"""
    spack.mirror.remove(args.name, args.scope)


def _configure_mirror(args):
    mirrors = spack.config.get("mirrors", scope=args.scope)

    if args.name not in mirrors:
        tty.die(f"No mirror found with name {args.name}.")

    entry = spack.mirror.Mirror(mirrors[args.name], args.name)
    direction = "fetch" if args.fetch else "push" if args.push else None
    changes = {}
    if args.url:
        changes["url"] = args.url
    if args.s3_access_key_id and args.s3_access_key_secret:
        changes["access_pair"] = [args.s3_access_key_id, args.s3_access_key_secret]
    if args.s3_access_token:
        changes["access_token"] = args.s3_access_token
    if args.s3_profile:
        changes["profile"] = args.s3_profile
    if args.s3_endpoint_url:
        changes["endpoint_url"] = args.s3_endpoint_url
    if args.oci_username and args.oci_password:
        changes["access_pair"] = [args.oci_username, args.oci_password]
    if getattr(args, "signed", None) is not None:
        changes["signed"] = args.signed
    if getattr(args, "autopush", None) is not None:
        changes["autopush"] = args.autopush

    # argparse cannot distinguish between --binary and --no-binary when same dest :(
    # notice that set-url does not have these args, so getattr
    if getattr(args, "type", None):
        changes["binary"] = "binary" in args.type
        changes["source"] = "source" in args.type

    changed = entry.update(changes, direction)

    if changed:
        mirrors[args.name] = entry.to_dict()
        spack.config.set("mirrors", mirrors, scope=args.scope)
    else:
        tty.msg("No changes made to mirror %s." % args.name)


def mirror_set(args):
    """configure the connection details of a mirror"""
    _configure_mirror(args)


def mirror_set_url(args):
    """change the URL of a mirror"""
    _configure_mirror(args)


def mirror_list(args):
    """print out available mirrors to the console"""

    mirrors = spack.mirror.MirrorCollection(scope=args.scope)
    if not mirrors:
        tty.msg("No mirrors configured.")
        return

    mirrors.display()


def specs_from_text_file(filename, concretize=False):
    """Return a list of specs read from a text file.

    The file should contain one spec per line.

    Args:
        filename (str): name of the file containing the abstract specs.
        concretize (bool): if True concretize the specs before returning
            the list.
    """
    with open(filename, "r") as f:
        specs_in_file = f.readlines()
        specs_in_file = [s.strip() for s in specs_in_file]
    return spack.cmd.parse_specs(" ".join(specs_in_file), concretize=concretize)


def concrete_specs_from_user(args):
    """Return the list of concrete specs that the user wants to mirror. The list
    is passed either from command line or from a text file.
    """
    specs = concrete_specs_from_cli_or_file(args)
    specs = extend_with_additional_versions(specs, num_versions=versions_per_spec(args))
    if args.dependencies:
        specs = extend_with_dependencies(specs)
    specs = filter_externals(specs)
    specs = list(set(specs))
    specs.sort(key=lambda s: (s.name, s.version))
    return specs


def extend_with_additional_versions(specs, num_versions):
    if num_versions == "all":
        mirror_specs = spack.mirror.get_all_versions(specs)
    else:
        mirror_specs = spack.mirror.get_matching_versions(specs, num_versions=num_versions)
    mirror_specs = [x.concretized() for x in mirror_specs]
    return mirror_specs


def filter_externals(specs):
    specs, external_specs = lang.stable_partition(specs, predicate_fn=lambda x: not x.external)
    for spec in external_specs:
        msg = "Skipping {0} as it is an external spec."
        tty.msg(msg.format(spec.cshort_spec))
    return specs


def extend_with_dependencies(specs):
    """Extend the input list by adding all the dependencies explicitly."""
    result = set()
    for spec in specs:
        for s in spec.traverse():
            result.add(s)
    return list(result)


def concrete_specs_from_cli_or_file(args):
    tty.msg("Concretizing input specs")
    with spack.concretize.disable_compiler_existence_check():
        if args.specs:
            specs = spack.cmd.parse_specs(args.specs, concretize=True)
            if not specs:
                raise SpackError("unable to parse specs from command line")

        if args.file:
            specs = specs_from_text_file(args.file, concretize=True)
            if not specs:
                raise SpackError("unable to parse specs from file '{}'".format(args.file))
    return specs


class IncludeFilter:
    def __init__(self, args):
        self.exclude_specs = []
        if args.exclude_file:
            self.exclude_specs.extend(specs_from_text_file(args.exclude_file, concretize=False))
        if args.exclude_specs:
            self.exclude_specs.extend(spack.cmd.parse_specs(str(args.exclude_specs).split()))
        self.private = args.private

    def __call__(self, x):
        return all([self._not_license_excluded(x), self._not_cmdline_excluded(x)])

    def _not_license_excluded(self, x):
        """True if the spec is for a private mirror, or as long as the
        package does not explicitly forbid redistributing source."""
        if self.private:
            return True
        elif x.package_class.redistribute_source(x):
            return True
        else:
            tty.debug(
                "Skip adding {0} to mirror: the package.py file"
                " indicates that a public mirror should not contain"
                " it.".format(x.name)
            )
            return False

    def _not_cmdline_excluded(self, x):
        """True if a spec was not explicitly excluded by the user."""
        return not any(x.satisfies(y) for y in self.exclude_specs)


def concrete_specs_from_environment():
    env = ev.active_environment()
    assert env, "an active environment is required"
    mirror_specs = env.all_specs()
    mirror_specs = filter_externals(mirror_specs)
    return mirror_specs


def all_specs_with_all_versions():
    specs = [spack.spec.Spec(n) for n in spack.repo.all_package_names()]
    mirror_specs = spack.mirror.get_all_versions(specs)
    mirror_specs.sort(key=lambda s: (s.name, s.version))
    return mirror_specs


def versions_per_spec(args):
    """Return how many versions should be mirrored per spec."""
    if not args.versions_per_spec:
        num_versions = 1
    elif args.versions_per_spec == "all":
        num_versions = "all"
    else:
        try:
            num_versions = int(args.versions_per_spec)
        except ValueError:
            raise SpackError(
                "'--versions-per-spec' must be a number or 'all',"
                " got '{0}'".format(args.versions_per_spec)
            )
    return num_versions


def process_mirror_stats(present, mirrored, error):
    p, m, e = len(present), len(mirrored), len(error)
    tty.msg(
        "Archive stats:",
        "  %-4d already present" % p,
        "  %-4d added" % m,
        "  %-4d failed to fetch." % e,
    )
    if error:
        tty.error("Failed downloads:")
        colify.colify(s.cformat("{name}{@version}") for s in error)
        sys.exit(1)


def mirror_create(args):
    """create a directory to be used as a spack mirror, and fill it with package archives"""
    if args.specs and args.all:
        raise SpackError(
            "cannot specify specs on command line if you chose to mirror all specs with '--all'"
        )

    if args.file and args.all:
        raise SpackError(
            "cannot specify specs with a file if you chose to mirror all specs with '--all'"
        )

    if args.file and args.specs:
        raise SpackError("cannot specify specs with a file AND on command line")

    if not args.specs and not args.file and not args.all:
        raise SpackError(
            "no packages were specified.",
            "To mirror all packages, use the '--all' option "
            "(this will require significant time and space).",
        )

    if args.versions_per_spec and args.all:
        raise SpackError(
            "cannot specify '--versions_per-spec' and '--all' together",
            "The option '--all' already implies mirroring all versions for each package.",
        )

    # When no directory is provided, the source dir is used
    path = args.directory or spack.caches.fetch_cache_location()

    mirror_specs, mirror_fn = _specs_and_action(args)
    mirror_fn(mirror_specs, path=path, skip_unstable_versions=args.skip_unstable_versions)


def _specs_and_action(args):
    include_fn = IncludeFilter(args)

    if args.all and not ev.active_environment():
        mirror_specs = all_specs_with_all_versions()
        mirror_fn = create_mirror_for_all_specs
    elif args.all and ev.active_environment():
        mirror_specs = concrete_specs_from_environment()
        mirror_fn = create_mirror_for_individual_specs
    else:
        mirror_specs = concrete_specs_from_user(args)
        mirror_fn = create_mirror_for_individual_specs

    mirror_specs, _ = lang.stable_partition(mirror_specs, predicate_fn=include_fn)
    return mirror_specs, mirror_fn


def create_mirror_for_all_specs(mirror_specs, path, skip_unstable_versions):
    mirror_cache, mirror_stats = spack.mirror.mirror_cache_and_stats(
        path, skip_unstable_versions=skip_unstable_versions
    )
    for candidate in mirror_specs:
        pkg_cls = spack.repo.PATH.get_pkg_class(candidate.name)
        pkg_obj = pkg_cls(spack.spec.Spec(candidate))
        mirror_stats.next_spec(pkg_obj.spec)
        spack.mirror.create_mirror_from_package_object(pkg_obj, mirror_cache, mirror_stats)
    process_mirror_stats(*mirror_stats.stats())


def create_mirror_for_individual_specs(mirror_specs, path, skip_unstable_versions):
    present, mirrored, error = spack.mirror.create(path, mirror_specs, skip_unstable_versions)
    tty.msg("Summary for mirror in {}".format(path))
    process_mirror_stats(present, mirrored, error)


def mirror_destroy(args):
    """given a url, recursively delete everything under it"""
    mirror_url = None

    if args.mirror_name:
        result = spack.mirror.MirrorCollection().lookup(args.mirror_name)
        mirror_url = result.push_url
    elif args.mirror_url:
        mirror_url = args.mirror_url

    web_util.remove_url(mirror_url, recursive=True)


def mirror(parser, args):
    action = {
        "create": mirror_create,
        "destroy": mirror_destroy,
        "add": mirror_add,
        "remove": mirror_remove,
        "rm": mirror_remove,
        "set-url": mirror_set_url,
        "set": mirror_set,
        "list": mirror_list,
    }

    if args.no_checksum:
        spack.config.set("config:checksum", False, scope="command_line")

    action[args.mirror_command](args)
