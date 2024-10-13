# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This is the implementation of the Spack command line executable.

In a normal Spack installation, this is invoked from the bin/spack script
after the system path is set up.
"""
import argparse

# import spack.modules.common
import inspect
import io
import operator
import os
import os.path
import pstats
import re
import shlex
import signal
import subprocess as sp
import sys
import traceback
import warnings
from typing import List, Tuple

import archspec.cpu

import llnl.util.lang
import llnl.util.tty as tty
import llnl.util.tty.colify
import llnl.util.tty.color as color
from llnl.util.tty.log import log_output

import spack
import spack.cmd
import spack.config
import spack.environment as ev
import spack.error
import spack.modules
import spack.paths
import spack.platforms
import spack.repo
import spack.spec
import spack.store
import spack.util.debug
import spack.util.environment
import spack.util.lock
from spack.error import SpackError

#: names of profile statistics
stat_names = pstats.Stats.sort_arg_dict_default

#: help levels in order of detail (i.e., number of commands shown)
levels = ["short", "long"]

#: intro text for help at different levels
intro_by_level = {
    "short": "These are common spack commands:",
    "long": "Complete list of spack commands:",
}

#: control top-level spack options shown in basic vs. advanced help
options_by_level = {"short": ["h", "k", "V", "color"], "long": "all"}

#: Longer text for each section, to show in help
section_descriptions = {
    "admin": "administration",
    "basic": "query packages",
    "build": "build packages",
    "config": "configuration",
    "developer": "developer",
    "environment": "environment",
    "extensions": "extensions",
    "help": "more help",
    "packaging": "create packages",
    "system": "system",
}

#: preferential command order for some sections (e.g., build pipeline is
#: in execution order, not alphabetical)
section_order = {
    "basic": ["list", "info", "find"],
    "build": [
        "fetch",
        "stage",
        "patch",
        "configure",
        "build",
        "restage",
        "install",
        "uninstall",
        "clean",
    ],
    "packaging": ["create", "edit"],
}

#: Properties that commands are required to set.
required_command_properties = ["level", "section", "description"]

spack_ld_library_path = os.environ.get("LD_LIBRARY_PATH", "")

#: Whether to print backtraces on error
SHOW_BACKTRACE = False


def add_all_commands(parser):
    """Add all spack subcommands to the parser."""
    for cmd in spack.cmd.all_commands():
        parser.add_command(cmd)


def index_commands():
    """create an index of commands by section for this help level"""
    index = {}
    for command in spack.cmd.all_commands():
        cmd_module = spack.cmd.get_module(command)

        # make sure command modules have required properties
        for p in required_command_properties:
            prop = getattr(cmd_module, p, None)
            if not prop:
                tty.die("Command doesn't define a property '%s': %s" % (p, command))

        # add commands to lists for their level and higher levels
        for level in reversed(levels):
            level_sections = index.setdefault(level, {})
            commands = level_sections.setdefault(cmd_module.section, [])
            commands.append(command)
            if level == cmd_module.level:
                break

    return index


class SpackHelpFormatter(argparse.RawTextHelpFormatter):
    def _format_actions_usage(self, actions, groups):
        """Formatter with more concise usage strings."""
        usage = super()._format_actions_usage(actions, groups)

        # Eliminate any occurrence of two or more consecutive spaces
        usage = re.sub(r"[ ]{2,}", " ", usage)

        # compress single-character flags that are not mutually exclusive
        # at the beginning of the usage string
        chars = "".join(re.findall(r"\[-(.)\]", usage))
        usage = re.sub(r"\[-.\] ?", "", usage)
        if chars:
            usage = "[-%s] %s" % (chars, usage)
        return usage.strip()

    def add_arguments(self, actions):
        actions = sorted(actions, key=operator.attrgetter("option_strings"))
        super().add_arguments(actions)


class SpackArgumentParser(argparse.ArgumentParser):
    def format_help_sections(self, level):
        """Format help on sections for a particular verbosity level.

        Args:
            level (str): 'short' or 'long' (more commands shown for long)
        """
        if level not in levels:
            raise ValueError("level must be one of: %s" % levels)

        # lazily add all commands to the parser when needed.
        add_all_commands(self)

        """Print help on subcommands in neatly formatted sections."""
        formatter = self._get_formatter()

        # Create a list of subcommand actions. Argparse internals are nasty!
        # Note: you can only call _get_subactions() once.  Even nastier!
        if not hasattr(self, "actions"):
            self.actions = self._subparsers._actions[-1]._get_subactions()

        # make a set of commands not yet added.
        remaining = set(spack.cmd.all_commands())

        def add_group(group):
            formatter.start_section(group.title)
            formatter.add_text(group.description)
            formatter.add_arguments(group._group_actions)
            formatter.end_section()

        def add_subcommand_group(title, commands):
            """Add informational help group for a specific subcommand set."""
            cmd_set = set(c for c in commands)

            # make a dict of commands of interest
            cmds = dict((a.dest, a) for a in self.actions if a.dest in cmd_set)

            # add commands to a group in order, and add the group
            group = argparse._ArgumentGroup(self, title=title)
            for name in commands:
                group._add_action(cmds[name])
                if name in remaining:
                    remaining.remove(name)
            add_group(group)

        # select only the options for the particular level we're showing.
        show_options = options_by_level[level]
        if show_options != "all":
            opts = dict(
                (opt.option_strings[0].strip("-"), opt) for opt in self._optionals._group_actions
            )

            new_actions = [opts[letter] for letter in show_options]
            self._optionals._group_actions = new_actions

        # custom, more concise usage for top level
        help_options = self._optionals._group_actions
        help_options = help_options + [self._positionals._group_actions[-1]]
        formatter.add_usage(self.usage, help_options, self._mutually_exclusive_groups)

        # description
        formatter.add_text(self.description)

        # start subcommands
        formatter.add_text(intro_by_level[level])

        # add argument groups based on metadata in commands
        index = index_commands()
        sections = index[level]

        for section in sorted(sections):
            if section == "help":
                continue  # Cover help in the epilog.

            group_description = section_descriptions.get(section, section)

            to_display = sections[section]
            commands = []

            # add commands whose order we care about first.
            if section in section_order:
                commands.extend(cmd for cmd in section_order[section] if cmd in to_display)

            # add rest in alphabetical order.
            commands.extend(cmd for cmd in sorted(sections[section]) if cmd not in commands)

            # add the group to the parser
            add_subcommand_group(group_description, commands)

        # optionals
        add_group(self._optionals)

        # epilog
        formatter.add_text(
            """\
{help}:
  spack help --all       list all commands and options
  spack help <command>   help on a specific command
  spack help --spec      help on the package specification syntax
  spack docs             open https://spack.rtfd.io/ in a browser
""".format(
                help=section_descriptions["help"]
            )
        )

        # determine help from format above
        return formatter.format_help()

    def add_subparsers(self, **kwargs):
        """Ensure that sensible defaults are propagated to subparsers"""
        kwargs.setdefault("metavar", "SUBCOMMAND")

        # From Python 3.7 we can require a subparser, earlier versions
        # of argparse will error because required=True is unknown
        if sys.version_info[:2] > (3, 6):
            kwargs.setdefault("required", True)

        sp = super().add_subparsers(**kwargs)
        # This monkey patching is needed for Python 3.6, which supports
        # having a required subparser but don't expose the API used above
        if sys.version_info[:2] == (3, 6):
            sp.required = True

        old_add_parser = sp.add_parser

        def add_parser(name, **kwargs):
            kwargs.setdefault("formatter_class", SpackHelpFormatter)
            return old_add_parser(name, **kwargs)

        sp.add_parser = add_parser
        return sp

    def add_command(self, cmd_name):
        """Add one subcommand to this parser."""
        # lazily initialize any subparsers
        if not hasattr(self, "subparsers"):
            # remove the dummy "command" argument.
            if self._actions[-1].dest == "command":
                self._remove_action(self._actions[-1])
            self.subparsers = self.add_subparsers(metavar="COMMAND", dest="command")

        if cmd_name not in self.subparsers._name_parser_map:
            # each command module implements a parser() function, to which we
            # pass its subparser for setup.
            module = spack.cmd.get_module(cmd_name)

            # build a list of aliases
            alias_list = []
            aliases = spack.config.get("config:aliases")
            if aliases:
                alias_list = [k for k, v in aliases.items() if shlex.split(v)[0] == cmd_name]

            subparser = self.subparsers.add_parser(
                cmd_name,
                aliases=alias_list,
                help=module.description,
                description=module.description,
            )
            module.setup_parser(subparser)

        # return the callable function for the command
        return spack.cmd.get_command(cmd_name)

    def format_help(self, level="short"):
        if self.prog == "spack":
            # use format_help_sections for the main spack parser, but not
            # for subparsers
            return self.format_help_sections(level)
        else:
            # in subparsers, self.prog is, e.g., 'spack install'
            return super().format_help()

    def _check_value(self, action, value):
        # converted value must be one of the choices (if specified)
        if action.choices is not None and value not in action.choices:
            cols = llnl.util.tty.colify.colified(sorted(action.choices), indent=4, tty=True)
            msg = "invalid choice: %r choose from:\n%s" % (value, cols)
            raise argparse.ArgumentError(action, msg)


def make_argument_parser(**kwargs):
    """Create an basic argument parser without any subcommands added."""
    parser = SpackArgumentParser(
        formatter_class=SpackHelpFormatter,
        add_help=False,
        description=(
            "A flexible package manager that supports multiple versions,\n"
            "configurations, platforms, and compilers."
        ),
        **kwargs,
    )

    # stat names in groups of 7, for nice wrapping.
    stat_lines = list(zip(*(iter(stat_names),) * 7))

    parser.add_argument(
        "-h",
        "--help",
        dest="help",
        action="store_const",
        const="short",
        default=None,
        help="show this help message and exit",
    )
    parser.add_argument(
        "-H",
        "--all-help",
        dest="help",
        action="store_const",
        const="long",
        default=None,
        help="show help for all commands (same as spack help --all)",
    )
    parser.add_argument(
        "--color",
        action="store",
        default=None,
        choices=("always", "never", "auto"),
        help="when to colorize output (default: auto)",
    )
    parser.add_argument(
        "-c",
        "--config",
        default=None,
        action="append",
        dest="config_vars",
        help="add one or more custom, one off config settings",
    )
    parser.add_argument(
        "-C",
        "--config-scope",
        dest="config_scopes",
        action="append",
        metavar="DIR|ENV",
        help="add directory or environment as read-only configuration scope, without activating "
        "the environment.",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="count",
        default=0,
        help="write out debug messages\n\n(more d's for more verbosity: -d, -dd, -ddd, etc.)",
    )
    parser.add_argument("--timestamp", action="store_true", help="add a timestamp to tty output")
    parser.add_argument("--pdb", action="store_true", help="run spack under the pdb debugger")

    env_group = parser.add_mutually_exclusive_group()
    env_group.add_argument(
        "-e",
        "--env",
        dest="env",
        metavar="ENV",
        action="store",
        help="run with a specific environment (see spack env)",
    )
    env_group.add_argument(
        "-D",
        "--env-dir",
        dest="env_dir",
        metavar="DIR",
        action="store",
        help="run with an environment directory (ignore managed environments)",
    )
    env_group.add_argument(
        "-E",
        "--no-env",
        dest="no_env",
        action="store_true",
        help="run without any environments activated (see spack env)",
    )
    parser.add_argument(
        "--use-env-repo",
        action="store_true",
        help="when running in an environment, use its package repository",
    )

    parser.add_argument(
        "-k",
        "--insecure",
        action="store_true",
        help="do not check ssl certificates when downloading",
    )
    parser.add_argument(
        "-l",
        "--enable-locks",
        action="store_true",
        dest="locks",
        default=None,
        help="use filesystem locking (default)",
    )
    parser.add_argument(
        "-L",
        "--disable-locks",
        action="store_false",
        dest="locks",
        help="do not use filesystem locking (unsafe)",
    )
    parser.add_argument(
        "-m", "--mock", action="store_true", help="use mock packages instead of real ones"
    )
    parser.add_argument(
        "-b",
        "--bootstrap",
        action="store_true",
        help="use bootstrap configuration (bootstrap store, config, externals)",
    )
    parser.add_argument(
        "-p",
        "--profile",
        action="store_true",
        dest="spack_profile",
        help="profile execution using cProfile",
    )
    parser.add_argument(
        "--sorted-profile",
        default=None,
        metavar="STAT",
        help=f"profile and sort\n\none or more of: {stat_lines[0]}",
    )
    parser.add_argument(
        "--lines",
        default=20,
        action="store",
        help="lines of profile output or 'all' (default: 20)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="print additional output during builds"
    )
    parser.add_argument(
        "--stacktrace",
        action="store_true",
        default="SPACK_STACKTRACE" in os.environ,
        help="add stacktraces to all printed statements",
    )
    parser.add_argument(
        "--backtrace",
        action="store_true",
        default="SPACK_BACKTRACE" in os.environ,
        help="always show backtraces for exceptions",
    )
    parser.add_argument(
        "-V", "--version", action="store_true", help="show version number and exit"
    )
    parser.add_argument(
        "--print-shell-vars", action="store", help="print info needed by setup-env.*sh"
    )

    return parser


def send_warning_to_tty(message, *args):
    """Redirects messages to tty.warn."""
    tty.warn(message)


def setup_main_options(args):
    """Configure spack globals based on the basic options."""
    # Assign a custom function to show warnings
    warnings.showwarning = send_warning_to_tty

    # Set up environment based on args.
    tty.set_verbose(args.verbose)
    tty.set_debug(args.debug)
    tty.set_stacktrace(args.stacktrace)

    # debug must be set first so that it can even affect behavior of
    # errors raised by spack.config.

    if args.debug or args.backtrace:
        spack.error.debug = True
        global SHOW_BACKTRACE
        SHOW_BACKTRACE = True

    if args.debug:
        spack.util.debug.register_interrupt_handler()
        spack.config.set("config:debug", True, scope="command_line")
        spack.util.environment.TRACING_ENABLED = True

    if args.timestamp:
        tty.set_timestamp(True)

    # override lock configuration if passed on command line
    if args.locks is not None:
        if args.locks is False:
            spack.util.lock.check_lock_safety(spack.paths.prefix)
        spack.config.set("config:locks", args.locks, scope="command_line")

    if args.mock:
        import spack.util.spack_yaml as syaml

        key = syaml.syaml_str("repos")
        key.override = True
        spack.config.CONFIG.scopes["command_line"].sections["repos"] = syaml.syaml_dict(
            [(key, [spack.paths.mock_packages_path])]
        )
        spack.repo.PATH = spack.repo.create(spack.config.CONFIG)

    # If the user asked for it, don't check ssl certs.
    if args.insecure:
        tty.warn("You asked for --insecure. Will NOT check SSL certificates.")
        spack.config.set("config:verify_ssl", False, scope="command_line")

    # Use the spack config command to handle parsing the config strings
    for config_var in args.config_vars or []:
        spack.config.add(fullpath=config_var, scope="command_line")

    # On Windows10 console handling for ASCI/VT100 sequences is not
    # on by default. Turn on before we try to write to console
    # with color
    color.try_enable_terminal_color_on_windows()
    # when to use color (takes always, auto, or never)
    if args.color is not None:
        color.set_color_when(args.color)


def allows_unknown_args(command):
    """Implements really simple argument injection for unknown arguments.

    Commands may add an optional argument called "unknown args" to
    indicate they can handle unknonwn args, and we'll pass the unknown
    args in.
    """
    info = dict(inspect.getmembers(command))
    varnames = info["__code__"].co_varnames
    argcount = info["__code__"].co_argcount
    return argcount == 3 and varnames[2] == "unknown_args"


def _invoke_command(command, parser, args, unknown_args):
    """Run a spack command *without* setting spack global options."""
    if allows_unknown_args(command):
        return_val = command(parser, args, unknown_args)
    else:
        if unknown_args:
            tty.die("unrecognized arguments: %s" % " ".join(unknown_args))
        return_val = command(parser, args)

    # Allow commands to return and error code if they want
    return 0 if return_val is None else return_val


class SpackCommand:
    """Callable object that invokes a spack command (for testing).

    Example usage::

        install = SpackCommand('install')
        install('-v', 'mpich')

    Use this to invoke Spack commands directly from Python and check
    their output.
    """

    def __init__(self, command_name, subprocess=False):
        """Create a new SpackCommand that invokes ``command_name`` when called.

        Args:
            command_name (str): name of the command to invoke
            subprocess (bool): whether to fork a subprocess or not. Currently not supported on
                Windows, where it is always False.
        """
        self.parser = make_argument_parser()
        self.command_name = command_name
        # TODO: figure out how to support this on windows
        self.subprocess = subprocess if sys.platform != "win32" else False

    def __call__(self, *argv, **kwargs):
        """Invoke this SpackCommand.

        Args:
            argv (list): command line arguments.

        Keyword Args:
            fail_on_error (optional bool): Don't raise an exception on error
            global_args (optional list): List of global spack arguments:
                simulates ``spack [global_args] [command] [*argv]``

        Returns:
            (str): combined output and error as a string

        On return, if ``fail_on_error`` is False, return value of command
        is set in ``returncode`` property, and the error is set in the
        ``error`` property.  Otherwise, raise an error.
        """
        # set these before every call to clear them out
        self.returncode = None
        self.error = None

        prepend = kwargs["global_args"] if "global_args" in kwargs else []
        fail_on_error = kwargs.get("fail_on_error", True)

        if self.subprocess:
            p = sp.Popen(
                [spack.paths.spack_script] + prepend + [self.command_name] + list(argv),
                stdout=sp.PIPE,
                stderr=sp.STDOUT,
            )
            out, self.returncode = p.communicate()
            out = out.decode()
        else:
            command = self.parser.add_command(self.command_name)
            args, unknown = self.parser.parse_known_args(
                prepend + [self.command_name] + list(argv)
            )

            out = io.StringIO()
            try:
                with log_output(out, echo=True):
                    self.returncode = _invoke_command(command, self.parser, args, unknown)

            except SystemExit as e:
                self.returncode = e.code

            except BaseException as e:
                tty.debug(e)
                self.error = e
                if fail_on_error:
                    self._log_command_output(out)
                    raise
            out = out.getvalue()

        if fail_on_error and self.returncode not in (None, 0):
            self._log_command_output(out)
            raise SpackCommandError(
                "Command exited with code %d: %s(%s)"
                % (self.returncode, self.command_name, ", ".join("'%s'" % a for a in argv))
            )

        return out

    def _log_command_output(self, out):
        if tty.is_verbose():
            fmt = self.command_name + ": {0}"
            for ln in out.getvalue().split("\n"):
                if len(ln) > 0:
                    tty.verbose(fmt.format(ln.replace("==> ", "")))


def _profile_wrapper(command, parser, args, unknown_args):
    import cProfile

    try:
        nlines = int(args.lines)
    except ValueError:
        if args.lines != "all":
            tty.die("Invalid number for --lines: %s" % args.lines)
        nlines = -1

    # allow comma-separated list of fields
    sortby = ["time"]
    if args.sorted_profile:
        sortby = args.sorted_profile.split(",")
        for stat in sortby:
            if stat not in stat_names:
                tty.die("Invalid sort field: %s" % stat)

    try:
        # make a profiler and run the code.
        pr = cProfile.Profile()
        pr.enable()
        return _invoke_command(command, parser, args, unknown_args)

    finally:
        pr.disable()

        # print out profile stats.
        stats = pstats.Stats(pr, stream=sys.stderr)
        stats.sort_stats(*sortby)
        stats.print_stats(nlines)


@llnl.util.lang.memoized
def _compatible_sys_types():
    """Return a list of all the platform-os-target tuples compatible
    with the current host.
    """
    host_platform = spack.platforms.host()
    host_os = str(host_platform.operating_system("default_os"))
    host_target = archspec.cpu.host()
    compatible_targets = [host_target] + host_target.ancestors

    compatible_archs = [
        str(spack.spec.ArchSpec((str(host_platform), host_os, str(target))))
        for target in compatible_targets
    ]
    return compatible_archs


def print_setup_info(*info):
    """Print basic information needed by setup-env.[c]sh.

    Args:
        info (list): list of things to print: comma-separated list
            of 'csh', 'sh', or 'modules'

    This is in ``main.py`` to make it fast; the setup scripts need to
    invoke spack in login scripts, and it needs to be quick.
    """
    import spack.modules.common

    shell = "csh" if "csh" in info else "sh"

    def shell_set(var, value):
        if shell == "sh":
            print("%s='%s'" % (var, value))
        elif shell == "csh":
            print("set %s = '%s'" % (var, value))
        else:
            tty.die("shell must be sh or csh")

    # print sys type
    shell_set("_sp_sys_type", str(spack.spec.ArchSpec.default_arch()))
    shell_set("_sp_compatible_sys_types", ":".join(_compatible_sys_types()))
    # print roots for all module systems
    module_to_roots = {"tcl": list(), "lmod": list()}
    for name in module_to_roots.keys():
        path = spack.modules.common.root_path(name, "default")
        module_to_roots[name].append(path)

    other_spack_instances = spack.config.get("upstreams") or {}
    for install_properties in other_spack_instances.values():
        upstream_module_roots = install_properties.get("modules", {})
        upstream_module_roots = dict(
            (k, v) for k, v in upstream_module_roots.items() if k in module_to_roots
        )
        for module_type, root in upstream_module_roots.items():
            module_to_roots[module_type].append(root)

    for name, paths in module_to_roots.items():
        # Environment setup prepends paths, so the order is reversed here to
        # preserve the intended priority: the modules of the local Spack
        # instance are the highest-precedence.
        roots_val = ":".join(reversed(paths))
        shell_set("_sp_%s_roots" % name, roots_val)

    # print environment module system if available. This can be expensive
    # on clusters, so skip it if not needed.
    if "modules" in info:
        generic_arch = archspec.cpu.host().family
        module_spec = "environment-modules target={0}".format(generic_arch)
        specs = spack.store.STORE.db.query(module_spec)
        if specs:
            shell_set("_sp_module_prefix", specs[-1].prefix)
        else:
            shell_set("_sp_module_prefix", "not_installed")


def restore_macos_dyld_vars():
    """
    Spack mutates DYLD_* variables in `spack load` and `spack env activate`.
    Unlike Linux, macOS SIP clears these variables in new processes, meaning
    that os.environ["DYLD_*"] in our Python process is not the same as the user's
    shell. Therefore, we store the user's DYLD_* variables in SPACK_DYLD_* and
    restore them here.
    """
    if not sys.platform == "darwin":
        return

    for dyld_var in ("DYLD_LIBRARY_PATH", "DYLD_FALLBACK_LIBRARY_PATH"):
        stored_var_name = f"SPACK_{dyld_var}"
        if stored_var_name in os.environ:
            os.environ[dyld_var] = os.environ[stored_var_name]


def resolve_alias(cmd_name: str, cmd: List[str]) -> Tuple[str, List[str]]:
    """Resolves aliases in the given command.

    Args:
        cmd_name: command name.
        cmd: command line arguments.

    Returns:
        new command name and arguments.
    """
    all_commands = spack.cmd.all_commands()
    aliases = spack.config.get("config:aliases")

    if aliases:
        for key, value in aliases.items():
            if " " in key:
                tty.warn(
                    f"Alias '{key}' (mapping to '{value}') contains a space"
                    ", which is not supported."
                )
            if key in all_commands:
                tty.warn(
                    f"Alias '{key}' (mapping to '{value}') attempts to override"
                    " built-in command."
                )

    if cmd_name not in all_commands:
        alias = None

        if aliases:
            alias = aliases.get(cmd_name)

        if alias is not None:
            alias_parts = shlex.split(alias)
            cmd_name = alias_parts[0]
            cmd = alias_parts + cmd[1:]

    return cmd_name, cmd


def _main(argv=None):
    """Logic for the main entry point for the Spack command.

    ``main()`` calls ``_main()`` and catches any errors that emerge.

    ``_main()`` handles:

    1. Parsing arguments;
    2. Setting up configuration; and
    3. Finding and executing a Spack command.

    Args:
        argv (list or None): command line arguments, NOT including
            the executable name. If None, parses from ``sys.argv``.

    """
    # ------------------------------------------------------------------------
    # main() is tricky to get right, so be careful where you put things.
    #
    # Things in this first part of `main()` should *not* require any
    # configuration. This doesn't include much -- setting up th parser,
    # restoring some key environment variables, very simple CLI options, etc.
    # ------------------------------------------------------------------------

    # Create a parser with a simple positional argument first.  We'll
    # lazily load the subcommand(s) we need later. This allows us to
    # avoid loading all the modules from spack.cmd when we don't need
    # them, which reduces startup latency.
    parser = make_argument_parser()
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args, unknown = parser.parse_known_args(argv)

    # Just print help and exit if run with no arguments at all
    no_args = (len(sys.argv) == 1) if argv is None else (len(argv) == 0)
    if no_args:
        parser.print_help()
        return 1

    # version is special as it does not require a command or loading and additional infrastructure
    if args.version:
        print(spack.get_version())
        return 0

    # ------------------------------------------------------------------------
    # This part of the `main()` sets up Spack's configuration.
    #
    # We set command line options (like --debug), then command line config
    # scopes, then environment configuration here.
    # ------------------------------------------------------------------------

    # Make spack load / env activate work on macOS
    restore_macos_dyld_vars()

    # make spack.config aware of any command line configuration scopes
    if args.config_scopes:
        spack.config.COMMAND_LINE_SCOPES = args.config_scopes

    # ensure options on spack command come before everything
    setup_main_options(args)

    # activate an environment if one was specified on the command line
    env_format_error = None
    if not args.no_env:
        try:
            env = spack.cmd.find_environment(args)
            if env:
                ev.activate(env, args.use_env_repo)
        except spack.config.ConfigFormatError as e:
            # print the context but delay this exception so that commands like
            # `spack config edit` can still work with a bad environment.
            e.print_context()
            env_format_error = e

    # ------------------------------------------------------------------------
    # Things that require configuration should go below here
    # ------------------------------------------------------------------------
    if args.print_shell_vars:
        print_setup_info(*args.print_shell_vars.split(","))
        return 0

    # -h and -H are special as they do not require a command, but
    # all the other options do nothing without a command.
    if args.help:
        sys.stdout.write(parser.format_help(level=args.help))
        return 0

    # At this point we've considered all the options to spack itself, so we
    # need a command or we're done.
    if not args.command:
        parser.print_help()
        return 1

    # Try to load the particular command the caller asked for.
    cmd_name = args.command[0]
    cmd_name, args.command = resolve_alias(cmd_name, args.command)

    # set up a bootstrap context, if asked.
    # bootstrap context needs to include parsing the command, b/c things
    # like `ConstraintAction` and `ConfigSetAction` happen at parse time.
    bootstrap_context = llnl.util.lang.nullcontext()
    if args.bootstrap:
        import spack.bootstrap as bootstrap  # avoid circular imports

        bootstrap_context = bootstrap.ensure_bootstrap_configuration()

    with bootstrap_context:
        return finish_parse_and_run(parser, cmd_name, args, env_format_error)


def finish_parse_and_run(parser, cmd_name, main_args, env_format_error):
    """Finish parsing after we know the command to run."""
    # add the found command to the parser and re-run then re-parse
    command = parser.add_command(cmd_name)
    args, unknown = parser.parse_known_args(main_args.command)
    # we need to inherit verbose since the install command checks for it
    args.verbose = main_args.verbose

    # Now that we know what command this is and what its args are, determine
    # whether we can continue with a bad environment and raise if not.
    if env_format_error:
        subcommand = getattr(args, "config_command", None)
        if (cmd_name, subcommand) != ("config", "edit"):
            raise env_format_error

    # many operations will fail without a working directory.
    spack.paths.set_working_dir()

    # now we can actually execute the command.
    if main_args.spack_profile or main_args.sorted_profile:
        _profile_wrapper(command, parser, args, unknown)
    elif main_args.pdb:
        import pdb

        pdb.runctx("_invoke_command(command, parser, args, unknown)", globals(), locals())
        return 0
    else:
        return _invoke_command(command, parser, args, unknown)


def main(argv=None):
    """This is the entry point for the Spack command.

    ``main()`` itself is just an error handler -- it handles errors for
    everything in Spack that makes it to the top level.

    The logic is all in ``_main()``.

    Args:
        argv (list or None): command line arguments, NOT including
            the executable name. If None, parses from sys.argv.

    """
    try:
        return _main(argv)

    except SpackError as e:
        tty.debug(e)
        e.die()  # gracefully die on any SpackErrors

    except KeyboardInterrupt:
        if spack.config.get("config:debug") or SHOW_BACKTRACE:
            raise
        sys.stderr.write("\n")
        tty.error("Keyboard interrupt.")
        return signal.SIGINT.value

    except SystemExit as e:
        if spack.config.get("config:debug") or SHOW_BACKTRACE:
            traceback.print_exc()
        return e.code

    except Exception as e:
        if spack.config.get("config:debug") or SHOW_BACKTRACE:
            raise
        tty.error(e)
        return 3


class SpackCommandError(Exception):
    """Raised when SpackCommand execution fails."""
