# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import llnl.util.tty as tty

import spack.cmd
import spack.environment as ev
import spack.paths
from spack.util.path import substitute_path_variables

description = "manage included configs and concrete environments in the active environment"
section = "environments"
level = "long"

subcommands = ["add", "remove", "list"]


def include_list_setup_parser(subparser):
    """List include(s) in the active environment"""

    expand_group = subparser.add_mutually_exclusive_group()
    expand_group.add_argument("--expand", action="store_true")
    expand_group.add_argument("--no-expand", action="store_false", dest="expand")

    # TODO: Add recursive listing option for environments including environments with include
    #       The default for list should be to only list the comonents listed in the active
    #       environment.


def include_list(env, args):
    include = env.manifest.list_includes(concrete=args.concrete)

    if sys.stdout.isatty():
        if include:
            tty.msg(
                "Included "
                + ("Concrete Environments" if args.concrete else "Configuration Scopes")
            )
        else:
            tty.msg("No includes found")

    if include:
        msg = ""
        for inc in include:
            if args.expand:
                formatted_inc = substitute_path_variables(inc)
            else:
                # Collapse the prefix to the active environment or spack root variables
                formatted_inc = inc.replace(env.path, "$env")
                formatted_inc = formatted_inc.replace(spack.paths.spack_root, "$spack")

            # Print the env name and path
            env_name = ev.environment_name(inc)
            if not env_name == inc:
                formatted_inc = f"{env_name} ({formatted_inc})"

            msg += f"\n\t{formatted_inc}"

        tty.msg(msg)


def include_add_setup_parser(subparser):
    """Add include(s) to the active environment"""
    subparser.add_argument(
        "includes",
        metavar="includes",
        nargs="+",
        help="List of path(s) to configs or environments to include",
    )


def include_add(env, args):
    with env.write_transaction():
        invalid = env.manifest.add_includes(args.includes, concrete=args.concrete)
        env.write()

        if not len(invalid) == len(args.includes):
            msg = f"Adding includes to {env.name}"
            for inc in args.includes:
                if inc not in invalid:
                    msg += f"\n\t{inc}"
            tty.msg(msg)

        if invalid:
            msg = "Invalid Paths"
            for p in invalid:
                msg = msg + f"\n\t{p}"

            tty.warn(msg)


def include_remove_setup_parser(subparser):
    """Remove include(s) from the active environment"""
    subparser.add_argument(
        "includes",
        metavar="includes",
        nargs="+",
        help="List of path(s) to configs or environments to include",
    )


def include_remove(env, args):
    with env.write_transaction():
        unknown_includes = env.manifest.remove_includes(args.includes, concrete=args.concrete)
        env.write()

        if unknown_includes:
            msg = "Unknown includes"
            for inc in unknown_includes:
                msg += f"\n\t{inc}"
            tty.warn(msg)


#: Dictionary mapping subcommand names and aliases to functions
subcommand_functions = {}


#
# spack include
#
def setup_parser(subparser):
    # The concrete option applies to all of the subcommands
    subparser.add_argument(
        "--concrete", action="store_true", help="Include paths/names are concrete environment(s)"
    )
    sp = subparser.add_subparsers(metavar="ACTION", dest="include_command")

    for name in subcommands:
        if isinstance(name, (list, tuple)):
            name, aliases = name[0], name[1:]
        else:
            aliases = []

        # add commands to subcommands dict
        function_name = "include_%s" % name
        function = globals()[function_name]
        for alias in [name] + aliases:
            subcommand_functions[alias] = function

        # make a subparser and run the command's setup function on it
        setup_parser_cmd_name = "include_%s_setup_parser" % name
        setup_parser_cmd = globals()[setup_parser_cmd_name]

        subsubparser = sp.add_parser(name, aliases=aliases, help=setup_parser_cmd.__doc__)
        setup_parser_cmd(subsubparser)


def include(parser, args):
    """Look for a function called environment_<name> and call it."""
    action = subcommand_functions[args.include_command]

    # This command requires an active environment
    env = spack.cmd.require_active_env(cmd_name="include")
    if not env:
        tty.msg("No active environment")
        return

    action(env, args)
