# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
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
from spack.database import InstallStatuses

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
    subparser.add_argument(
        "-M",
        "--only-missing",
        action="store_true",
        dest="only_missing",
        help="show only missing dependencies",
    )
    subparser.add_argument(
        "--deprecated",
        action="store_true",
        help="show deprecated packages as well as installed specs",
    )
    subparser.add_argument(
        "--only-deprecated", action="store_true", help="show only deprecated packages"
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
    # Set up query arguments.
    installed = []
    if not (args.only_missing or args.only_deprecated):
        installed.append(InstallStatuses.INSTALLED)
    if (args.deprecated or args.only_deprecated) and not args.only_missing:
        installed.append(InstallStatuses.DEPRECATED)
    if (args.missing or args.only_missing) and not args.only_deprecated:
        installed.append(InstallStatuses.MISSING)

    known = any
    if args.unknown:
        known = False

    explicit = any
    if args.explicit:
        explicit = True
    if args.implicit:
        explicit = False

    q_args = {"installed": installed, "known": known, "explicit": explicit}

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

    Find in an environment outputs 2 or 3 sections:

    1. Root specs
    2. Concretized roots (if asked for with -c)
    3. Installed specs

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


def find(parser, args):
    env = ev.active_environment()

    if not env and args.only_roots:
        tty.die("-r / --only-roots requires an active environment")
    if not env and args.show_concretized:
        tty.die("-c / --show-concretized requires an active environment")

    if env:
        if args.constraint:
            init_specs = spack.cmd.parse_specs(args.constraint)
            results = env.all_matching_specs(*init_specs)
        else:
            results = env.all_specs()
    else:
        q_args = query_arguments(args)
        results = args.specs(**q_args)

    decorator = make_env_decorator(env) if env else lambda s, f: f

    # use groups by default except with format.
    if args.groups is None:
        args.groups = not args.format

    # Exit early with an error code if no package matches the constraint
    if not results and args.constraint:
        constraint_str = " ".join(str(s) for s in args.constraint_specs)
        tty.die(f"No package matches the query: {constraint_str}")

    # If tags have been specified on the command line, filter by tags
    if args.tags:
        packages_with_tags = spack.repo.PATH.packages_with_tags(*args.tags)
        results = [x for x in results if x.name in packages_with_tags]

    if args.loaded:
        results = spack.cmd.filter_loaded_specs(results)

    if args.install_status or args.show_concretized:
        status_fn = spack.spec.Spec.install_status
    else:
        status_fn = None

    # Display the result
    if args.json:
        cmd.display_specs_as_json(results, deps=args.deps)
    else:
        if not args.format:
            if env:
                display_env(env, args, decorator, results)

        if not args.only_roots:
            display_results = results
            if not args.show_concretized:
                display_results = list(x for x in results if x.installed)
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
            spack.cmd.print_how_many_pkgs(
                list(x for x in results if x.installed), pkg_type, suffix=installed_suffix
            )

            if env:
                spack.cmd.print_how_many_pkgs(
                    list(x for x in results if not x.installed),
                    "concretized",
                    suffix=concretized_suffix,
                )
