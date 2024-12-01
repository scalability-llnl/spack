# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import sys

import llnl.util.tty as tty
from llnl.util.lang import index_by
from llnl.util.tty.colify import colify
from llnl.util.tty.color import colorize

import spack.compilers
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
        default=sys.platform == "darwin",
        help="Allow mixed toolchains (for example: clang, clang++, gfortran)",
    )
    mixed_toolchain_group.add_argument(
        "--no-mixed-toolchain",
        action="store_false",
        dest="mixed_toolchain",
        help="Do not allow mixed toolchains (for example: clang, clang++, gfortran)",
    )
    find_parser.add_argument("add_paths", nargs=argparse.REMAINDER)
    find_parser.add_argument(
        "--scope",
        action=arguments.ConfigScope,
        default=lambda: spack.config.default_modify_scope("compilers"),
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
    paths = args.add_paths or None
    new_compilers = spack.compilers.find_compilers(
        path_hints=paths,
        scope=args.scope,
        mixed_toolchain=args.mixed_toolchain,
        max_workers=args.jobs,
    )
    if new_compilers:
        n = len(new_compilers)
        s = "s" if n > 1 else ""
        filename = spack.config.CONFIG.get_config_filename(args.scope, "compilers")
        tty.msg(f"Added {n:d} new compiler{s} to {filename}")
        compiler_strs = sorted(f"{c.spec.name}@{c.spec.version}" for c in new_compilers)
        colify(reversed(compiler_strs), indent=4)
    else:
        tty.msg("Found no new compilers")
    tty.msg("Compilers are defined in the following files:")
    colify(spack.compilers.compiler_config_files(), indent=4)


def compiler_remove(args):
    compiler_spec = spack.spec.CompilerSpec(args.compiler_spec)
    candidate_compilers = spack.compilers.compilers_for_spec(compiler_spec, scope=args.scope)

    if not candidate_compilers:
        tty.die("No compilers match spec %s" % compiler_spec)

    if not args.all and len(candidate_compilers) > 1:
        tty.error(f"Multiple compilers match spec {compiler_spec}. Choose one:")
        colify(reversed(sorted([c.spec.display_str for c in candidate_compilers])), indent=4)
        tty.msg("Or, use `spack compiler remove -a` to remove all of them.")
        sys.exit(1)

    for current_compiler in candidate_compilers:
        spack.compilers.remove_compiler_from_config(current_compiler.spec, scope=args.scope)
        tty.msg(f"{current_compiler.spec.display_str} has been removed")


def compiler_info(args):
    """Print info about all compilers matching a spec."""
    cspec = spack.spec.CompilerSpec(args.compiler_spec)
    compilers = spack.compilers.compilers_for_spec(cspec, scope=args.scope)

    if not compilers:
        tty.die("No compilers match spec %s" % cspec)
    else:
        for c in compilers:
            print(c.spec.display_str + ":")
            print("\tpaths:")
            for cpath in ["cc", "cxx", "f77", "fc"]:
                print("\t\t%s = %s" % (cpath, getattr(c, cpath, None)))
            if c.flags:
                print("\tflags:")
                for flag, flag_value in c.flags.items():
                    print("\t\t%s = %s" % (flag, flag_value))
            if len(c.environment) != 0:
                if len(c.environment.get("set", {})) != 0:
                    print("\tenvironment:")
                    print("\t    set:")
                    for key, value in c.environment["set"].items():
                        print("\t        %s = %s" % (key, value))
            if c.extra_rpaths:
                print("\tExtra rpaths:")
                for extra_rpath in c.extra_rpaths:
                    print("\t\t%s" % extra_rpath)
            print("\tmodules  = %s" % c.modules)
            print("\toperating system  = %s" % c.operating_system)


def compiler_list(args):
    compilers = spack.compilers.all_compilers(scope=args.scope, init_config=False)

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

    index = index_by(compilers, lambda c: (c.spec.name, c.operating_system, c.target))

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
            os_str += "-%s" % target
        cname = "%s{%s} %s" % (spack.spec.COMPILER_COLOR, name, os_str)
        tty.hline(colorize(cname), char="-")
        colify(reversed(sorted(c.spec.display_str for c in compilers)))


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
