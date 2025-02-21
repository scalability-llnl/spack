# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import copy
import sys

import llnl.util.lang
import llnl.util.tty as tty
import llnl.util.tty.color as color

import spack.cmd as cmd
import spack.config
import spack.environment as ev
import spack.repo
import spack.spec
import spack.store
from spack.cmd.common import arguments

from ..enums import InstallRecordStatus

description = "list and search installed packages"
section = "basic"
level = "short"


def setup_parser(subparser):
    format_group = subparser.add_mutually_exclusive_group()
    format_group.add_argument(
        "--format",
        action="store",
        default=None,
        help="output specs with the specified format string",
    )
    format_group.add_argument(
        "-H",
        "--hashes",
        action="store_const",
        dest="format",
        const="{/hash}",
        help="same as '--format {/hash}'; use with xargs or $()",
    )
    format_group.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="output specs as machine-readable json records",
    )

    subparser.add_argument(
        "-I", "--install-status", action="store_true", help="show install status of packages"
    )

    subparser.add_argument(
        "-d", "--deps", action="store_true", help="output dependencies along with found specs"
    )

    subparser.add_argument(
        "-p", "--paths", action="store_true", help="show paths to package install directories"
    )
    subparser.add_argument(
        "--groups",
        action="store_true",
        default=None,
        dest="groups",
        help="display specs in arch/compiler groups (default on)",
    )
    subparser.add_argument(
        "--no-groups",
        action="store_false",
        default=None,
        dest="groups",
        help="do not group specs by arch/compiler",
    )

    arguments.add_common_arguments(subparser, ["long", "very_long", "tags", "namespaces"])

    subparser.add_argument(
        "-r",
        "--only-roots",
        action="store_true",
        help="don't show full list of installed specs in an environment",
    )
    subparser.add_argument(
        "-c",
        "--show-concretized",
        action="store_true",
        help="show concretized specs in an environment",
    )
    subparser.add_argument(
        "-f",
        "--show-flags",
        action="store_true",
        dest="show_flags",
        help="show spec compiler flags",
    )
    subparser.add_argument(
        "--show-full-compiler",
        action="store_true",
        dest="show_full_compiler",
        help="show full compiler specs",
    )
    implicit_explicit = subparser.add_mutually_exclusive_group()
    implicit_explicit.add_argument(
        "-x",
        "--explicit",
        action="store_true",
        help="show only specs that were installed explicitly",
    )
    implicit_explicit.add_argument(
        "-X",
        "--implicit",
        action="store_true",
        help="show only specs that were installed as dependencies",
    )
    subparser.add_argument(
        "-u",
        "--unknown",
        action="store_true",
        dest="unknown",
        help="show only specs Spack does not have a package for",
    )
    subparser.add_argument(
        "-m",
        "--missing",
        action="store_true",
        dest="missing",
        help="show missing dependencies as well as installed specs",
    )
    subparser.add_argument(
        "-v",
        "--variants",
        action="store_true",
        dest="variants",
        help="show variants in output (can be long)",
    )
    subparser.add_argument(
        "--loaded", action="store_true", help="show only packages loaded in the user environment"
    )
    only_missing_or_deprecated = subparser.add_mutually_exclusive_group()
    only_missing_or_deprecated.add_argument(
        "-M",
        "--only-missing",
        action="store_true",
        dest="only_missing",
        help="show only missing dependencies",
    )
    only_missing_or_deprecated.add_argument(
        "--only-deprecated", action="store_true", help="show only deprecated packages"
    )
    subparser.add_argument(
        "--deprecated",
        action="store_true",
        help="show deprecated packages as well as installed specs",
    )
    subparser.add_argument(
        "--install-tree",
        action="store",
        default="all",
        help="Install trees to query: 'all' (default), 'local', 'upstream', upstream name or path",
    )

    subparser.add_argument("--start-date", help="earliest date of installation [YYYY-MM-DD]")
    subparser.add_argument("--end-date", help="latest date of installation [YYYY-MM-DD]")
    arguments.add_common_arguments(subparser, ["constraint"])


def query_arguments(args):
    if args.only_missing and (args.deprecated or args.missing):
        raise RuntimeError("cannot use --only-missing with --deprecated, or --missing")

    if args.only_deprecated and (args.deprecated or args.missing):
        raise RuntimeError("cannot use --only-deprecated with --deprecated, or --missing")

    installed = InstallRecordStatus.INSTALLED
    if args.only_missing:
        installed = InstallRecordStatus.MISSING
    elif args.only_deprecated:
        installed = InstallRecordStatus.DEPRECATED

    if args.missing:
        installed |= InstallRecordStatus.MISSING

    if args.deprecated:
        installed |= InstallRecordStatus.DEPRECATED

    predicate_fn = None
    if args.unknown:
        predicate_fn = lambda x: not spack.repo.PATH.exists(x.spec.name)

    explicit = None
    if args.explicit:
        explicit = True
    if args.implicit:
        explicit = False

    q_args = {"installed": installed, "predicate_fn": predicate_fn, "explicit": explicit}

    install_tree = args.install_tree
    upstreams = spack.config.get("upstreams", {})
    if install_tree in upstreams.keys():
        install_tree = upstreams[install_tree]["install_tree"]
    q_args["install_tree"] = install_tree

    # Time window of installation
    for attribute in ("start_date", "end_date"):
        date = getattr(args, attribute)
        if date:
            q_args[attribute] = llnl.util.lang.pretty_string_to_date(date)

    return q_args


def make_env_decorator(env):
    """Create a function for decorating specs when in an environment."""

    roots = set(env.roots())
    removed = set(env.removed_specs())

    def decorator(spec, fmt):
        # add +/-/* to show added/removed/root specs
        if any(spec.dag_hash() == r.dag_hash() for r in roots):
            return color.colorize(f"@*{{{fmt}}}")
        elif spec in removed:
            return color.colorize(f"@K{{{fmt}}}")
        else:
            return fmt

    return decorator


def display_env(env, args, decorator, results):
    """Display extra find output when running in an environment.

    In an environment, `spack find` outputs a preliminary section
    showing the root specs of the environment (this is in addition
    to the section listing out specs matching the query parameters).

    """
    tty.msg("In environment %s" % env.name)

    num_roots = len(env.user_specs) or "No"
    tty.msg(f"{num_roots} root specs")

    concrete_specs = {
        root: concrete_root
        for root, concrete_root in zip(env.concretized_user_specs, env.concrete_roots())
    }

    def root_decorator(spec, string):
        """Decorate root specs with their install status if needed"""
        concrete = concrete_specs.get(spec)
        if concrete:
            status = color.colorize(concrete.install_status().value)
            hash = concrete.dag_hash()
        else:
            status = color.colorize(spack.spec.InstallStatus.absent.value)
            hash = "-" * 32

        # TODO: status has two extra spaces on the end of it, but fixing this and other spec
        # TODO: space format idiosyncrasies is complicated. Fix this eventually
        status = status[:-2]

        if args.long or args.very_long:
            hash = color.colorize(f"@K{{{hash[: 7 if args.long else None]}}}")
            return f"{status} {hash} {string}"
        else:
            return f"{status} {string}"

    with spack.store.STORE.db.read_transaction():
        cmd.display_specs(
            env.user_specs,
            args,
            # these are overrides of CLI args
            paths=False,
            long=False,
            very_long=False,
            # these enforce details in the root specs to show what the user asked for
            namespaces=True,
            show_flags=True,
            show_full_compiler=True,
            decorator=root_decorator,
            variants=True,
        )

    print()

    if env.included_concrete_envs:
        tty.msg("Included specs")

        # Root specs cannot be displayed with prefixes, since those are not
        # set for abstract specs. Same for hashes
        root_args = copy.copy(args)
        root_args.paths = False

        # Roots are displayed with variants, etc. so that we can see
        # specifically what the user asked for.
        cmd.display_specs(
            env.included_user_specs,
            root_args,
            decorator=lambda s, f: color.colorize("@*{%s}" % f),
            namespace=True,
            show_flags=True,
            show_full_compiler=True,
            variants=True,
        )
        print()


def _find_query(args, env):
    q_args = query_arguments(args)
    concretized_but_not_installed = list()
    if env:
        all_env_specs = env.all_specs()
        if args.constraint:
            init_specs = cmd.parse_specs(args.constraint)
            env_specs = env.all_matching_specs(*init_specs)
        else:
            env_specs = all_env_specs

        spec_hashes = set(x.dag_hash() for x in env_specs)
        specs_meeting_q_args = set(spack.store.STORE.db.query(hashes=spec_hashes, **q_args))

        results = list()
        with spack.store.STORE.db.read_transaction():
            for spec in env_specs:
                if not spec.installed:
                    concretized_but_not_installed.append(spec)
                if spec in specs_meeting_q_args:
                    results.append(spec)
    else:
        results = args.specs(**q_args)

    # use groups by default except with format.
    if args.groups is None:
        args.groups = not args.format

    # Exit early with an error code if no package matches the constraint
    if concretized_but_not_installed and args.show_concretized:
        pass
    elif results:
        pass
    elif args.constraint:
        raise cmd.NoSpecMatches()

    # If tags have been specified on the command line, filter by tags
    if args.tags:
        packages_with_tags = spack.repo.PATH.packages_with_tags(*args.tags)
        results = [x for x in results if x.name in packages_with_tags]
        concretized_but_not_installed = [
            x for x in concretized_but_not_installed if x.name in packages_with_tags
        ]

    if args.loaded:
        results = cmd.filter_loaded_specs(results)

    return results, concretized_but_not_installed


def find(parser, args):
    env = ev.active_environment()

    if not env and args.only_roots:
        tty.die("-r / --only-roots requires an active environment")
    if not env and args.show_concretized:
        tty.die("-c / --show-concretized requires an active environment")

    try:
        results, concretized_but_not_installed = _find_query(args, env)
    except cmd.NoSpecMatches:
        # Note: this uses args.constraint vs. args.constraint_specs because
        # the latter only exists if you call args.specs()
        tty.die(f"No package matches the query: {' '.join(args.constraint)}")

    if args.install_status or args.show_concretized:
        status_fn = spack.spec.Spec.install_status
    else:
        status_fn = None

    # Display the result
    if args.json:
        cmd.display_specs_as_json(results, deps=args.deps)
    else:
        decorator = make_env_decorator(env) if env else lambda s, f: f

        if not args.format:
            if env:
                display_env(env, args, decorator, results)

        if not args.only_roots:
            display_results = list(results)
            if args.show_concretized:
                display_results += concretized_but_not_installed
            cmd.display_specs(
                display_results, args, decorator=decorator, all_headers=True, status_fn=status_fn
            )

        # print number of installed packages last (as the list may be long)
        if sys.stdout.isatty() and args.groups:
            installed_suffix = ""
            concretized_suffix = " to be installed"

            if args.only_roots:
                installed_suffix += " (not shown)"
                concretized_suffix += " (not shown)"
            else:
                if env and not args.show_concretized:
                    concretized_suffix += " (show with `spack find -c`)"

            pkg_type = "loaded" if args.loaded else "installed"
            cmd.print_how_many_pkgs(results, pkg_type, suffix=installed_suffix)

            if env:
                cmd.print_how_many_pkgs(
                    concretized_but_not_installed, "concretized", suffix=concretized_suffix
                )
