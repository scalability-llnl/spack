# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import sys
import warnings

import llnl.util.tty as tty
from llnl.util.lang import index_by
from llnl.util.tty.colify import colify
from llnl.util.tty.color import colorize

import spack.compilers.config
import spack.config
import spack.spec
from spack.cmd.common import arguments

description = "manage compilers"
section = "system"
level = "long"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="compiler_command")

    # Find
    find_parser = sp.add_parser(
        "find",
        aliases=["add"],
        help="search the system for compilers to add to Spack configuration",
    )
    mixed_toolchain_group = find_parser.add_mutually_exclusive_group()
    mixed_toolchain_group.add_argument(
        "--mixed-toolchain",
        action="store_true",
        default=False,
        help="(DEPRECATED) Allow mixed toolchains (for example: clang, clang++, gfortran)",
    )
    mixed_toolchain_group.add_argument(
        "--no-mixed-toolchain",
        action="store_false",
        dest="mixed_toolchain",
        help="(DEPRECATED) Do not allow mixed toolchains (for example: clang, clang++, gfortran)",
    )
    find_parser.add_argument("add_paths", nargs=argparse.REMAINDER)
    find_parser.add_argument(
        "--scope",
        action=arguments.ConfigScope,
        default=lambda: spack.config.default_modify_scope("packages"),
        help="configuration scope to modify",
    )
    arguments.add_common_arguments(find_parser, ["jobs"])

    # Remove
    remove_parser = sp.add_parser("remove", aliases=["rm"], help="remove compiler by spec")
    remove_parser.add_argument(
        "-a", "--all", action="store_true", help="remove ALL compilers that match spec"
    )
    remove_parser.add_argument("compiler_spec")
    remove_parser.add_argument(
        "--scope", action=arguments.ConfigScope, default=None, help="configuration scope to modify"
    )

    # List
    list_parser = sp.add_parser("list", help="list available compilers")
    list_parser.add_argument(
        "--scope", action=arguments.ConfigScope, help="configuration scope to read from"
    )

    # Info
    info_parser = sp.add_parser("info", help="show compiler paths")
    info_parser.add_argument("compiler_spec")
    info_parser.add_argument(
        "--scope", action=arguments.ConfigScope, help="configuration scope to read from"
    )


def compiler_find(args):
    """Search either $PATH or a list of paths OR MODULES for compilers and
    add them to Spack's configuration.
    """
    if args.mixed_toolchain:
        warnings.warn(
            "The '--mixed-toolchain' option has been deprecated in Spack v0.23, and currently "
            "has no effect. The option will be removed in Spack v1.1"
        )

    paths = args.add_paths or None
    new_compilers = spack.compilers.config.find_compilers(
        path_hints=paths, scope=args.scope, max_workers=args.jobs
    )
    if new_compilers:
        n = len(new_compilers)
        s = "s" if n > 1 else ""
        filename = spack.config.CONFIG.get_config_filename(args.scope, "packages")
        tty.msg(f"Added {n:d} new compiler{s} to {filename}")
        compiler_strs = sorted(f"{spec.name}@{spec.versions}" for spec in new_compilers)
        colify(reversed(compiler_strs), indent=4)
    else:
        tty.msg("Found no new compilers")
    tty.msg("Compilers are defined in the following files:")
    colify(spack.compilers.config.compiler_config_files(), indent=4)


def compiler_remove(args):
    remover = spack.compilers.config.CompilerRemover(spack.config.CONFIG)
    candidates = remover.mark_compilers(match=args.compiler_spec, scope=args.scope)
    if not candidates:
        tty.die(f"No compiler matches '{args.compiler_spec}'")

    compiler_strs = reversed(sorted(f"{spec.name}@{spec.versions}" for spec in candidates))

    if not args.all and len(candidates) > 1:
        tty.error(f"multiple compilers match the spec '{args.compiler_spec}':")
        print()
        colify(compiler_strs, indent=4)
        print()
        print(
            "Either use a stricter spec to select only one, or use `spack compiler remove -a`"
            " to remove all of them."
        )
        sys.exit(1)

    remover.flush()
    tty.msg("The following compilers have been removed:")
    print()
    colify(compiler_strs, indent=4)
    print()


def compiler_info(args):
    """Print info about all compilers matching a spec."""
    query = spack.spec.Spec(args.compiler_spec)
    all_compilers = spack.compilers.config.all_compilers(scope=args.scope, init_config=False)

    compilers = [x for x in all_compilers if x.satisfies(query)]

    if not compilers:
        tty.die(f"No compilers match spec {query.cformat()}")
    else:
        for c in compilers:
            print(f"{c.cformat()}:")
            print(f"  prefix: {c.external_path}")
            extra_attributes = getattr(c, "extra_attributes", {})
            if "compilers" in extra_attributes:
                print("  compilers:")
                for language, exe in extra_attributes.get("compilers", {}).items():
                    print(f"    {language}: {exe}")
            if "flags" in extra_attributes:
                print("  flags:")
                for flag, flag_value in extra_attributes["flags"].items():
                    print(f"    {flag} = {flag_value}")
            if "environment" in extra_attributes:
                environment = extra_attributes["environment"]
                if len(environment.get("set", {})) != 0:
                    print("\tenvironment:")
                    print("\t    set:")
                    for key, value in environment["set"].items():
                        print(f"\t        {key} = {value}")
            if "extra_rpaths" in extra_attributes:
                print("  extra rpaths:")
                for extra_rpath in extra_attributes["extra_rpaths"]:
                    print(f"    {extra_rpath}")
            if getattr(c, "external_modules", []):
                print("  modules: ")
                for module in c.external_modules:
                    print(f"    {module}")
            print()


def compiler_list(args):
    compilers = spack.compilers.config.all_compilers(scope=args.scope, init_config=False)

    # If there are no compilers in any scope, and we're outputting to a tty, give a
    # hint to the user.
    if len(compilers) == 0:
        if not sys.stdout.isatty():
            return
        msg = "No compilers available"
        if args.scope is None:
            msg += ". Run `spack compiler find` to autodetect compilers"
        tty.msg(msg)
        return

    index = index_by(compilers, spack.compilers.config.name_os_target)

    tty.msg("Available compilers")

    # For a container, take each element which does not evaluate to false and
    # convert it to a string. For elements which evaluate to False (e.g. None)
    # convert them to '' (in which case it still evaluates to False but is a
    # string type). Tuples produced by this are guaranteed to be comparable in
    # Python 3
    convert_str = lambda tuple_container: tuple(str(x) if x else "" for x in tuple_container)

    index_str_keys = list((convert_str(x), y) for x, y in index.items())
    ordered_sections = sorted(index_str_keys, key=lambda item: item[0])
    for i, (key, compilers) in enumerate(ordered_sections):
        if i >= 1:
            print()
        name, os, target = key
        os_str = os
        if target:
            os_str += f"-{target}"
        cname = f"{spack.spec.COMPILER_COLOR}{{{name}}} {os_str}"
        tty.hline(colorize(cname), char="-")
        colify(reversed(sorted(c.format("{name}@{version}") for c in compilers)))


def compiler(parser, args):
    action = {
        "add": compiler_find,
        "find": compiler_find,
        "remove": compiler_remove,
        "rm": compiler_remove,
        "info": compiler_info,
        "list": compiler_list,
    }
    action[args.compiler_command](args)
