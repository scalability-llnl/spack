# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import copy
import os
import re
import shlex
import sys
from argparse import ArgumentParser, Namespace
from typing import IO, Any, Callable, Dict, Iterable, List, Optional, Sequence, Set, Tuple, Union

import llnl.util.tty as tty
from llnl.util.argparsewriter import ArgparseRstWriter, ArgparseWriter, Command
from llnl.util.tty.colify import colify

import spack.cmd
import spack.config
import spack.main
import spack.paths
import spack.platforms
from spack.main import section_descriptions

description = "list available spack commands"
section = "developer"
level = "long"


#: list of command formatters
formatters: Dict[str, Callable[[Namespace, IO], None]] = {}


#: standard arguments for updating completion scripts
#: we iterate through these when called with --update-completion
update_completion_args: Dict[str, Dict[str, Any]] = {
    "bash": {
        "aliases": True,
        "format": "bash",
        "header": os.path.join(spack.paths.share_path, "bash", "spack-completion.bash"),
        "update": os.path.join(spack.paths.share_path, "spack-completion.bash"),
    },
    "fish": {
        "aliases": True,
        "format": "fish",
        "header": os.path.join(spack.paths.share_path, "fish", "spack-completion.fish"),
        "update": os.path.join(spack.paths.share_path, "spack-completion.fish"),
    },
}


def formatter(func: Callable[[Namespace, IO], None]) -> Callable[[Namespace, IO], None]:
    """Decorator used to register formatters.

    Args:
        func: Formatting function.

    Returns:
        The same function.
    """
    formatters[func.__name__] = func
    return func


def setup_parser(subparser: ArgumentParser) -> None:
    """Set up the argument parser.

    Args:
        subparser: Preliminary argument parser.
    """
    subparser.add_argument(
        "--update-completion",
        action="store_true",
        default=False,
        help="regenerate spack's tab completion scripts",
    )

    subparser.add_argument(
        "-a", "--aliases", action="store_true", default=False, help="include command aliases"
    )
    subparser.add_argument(
        "--format",
        default="names",
        choices=formatters,
        help="format to be used to print the output (default: names)",
    )
    subparser.add_argument(
        "--header",
        metavar="FILE",
        default=None,
        action="store",
        help="prepend contents of FILE to the output (useful for rst format)",
    )
    subparser.add_argument(
        "--update",
        metavar="FILE",
        default=None,
        action="store",
        help="write output to the specified file, if any command is newer",
    )
    subparser.add_argument(
        "rst_files",
        nargs=argparse.REMAINDER,
        help="list of rst files to search for `_cmd-spack-<cmd>` cross-refs",
    )


class SpackArgparseRstWriter(ArgparseRstWriter):
    """RST writer tailored for spack documentation."""

    def __init__(
        self,
        prog: str,
        out: IO = sys.stdout,
        aliases: bool = False,
        documented_commands: Set[str] = set(),
        rst_levels: Sequence[str] = ["-", "-", "^", "~", ":", "`"],
    ):
        """Initialize a new SpackArgparseRstWriter instance.

        Args:
            prog: Program name.
            out: File object to write to.
            aliases: Whether or not to include subparsers for aliases.
            documented_commands: Set of commands with additional documentation.
            rst_levels: List of characters for rst section headings.
        """
        super().__init__(prog, out, aliases, rst_levels)
        self.documented = documented_commands

    def usage(self, usage: str) -> str:
        """Example usage of a command.

        Args:
            usage: Command usage.

        Returns:
            Usage of a command.
        """
        string = super().usage(usage)

        cmd = self.parser.prog.replace(" ", "-")
        if cmd in self.documented:
            string = f"{string}\n:ref:`More documentation <cmd-{cmd}>`\n"

        return string


class SubcommandWriter(ArgparseWriter):
    """Write argparse output as a list of subcommands."""

    def format(self, cmd: Command) -> str:
        """Return the string representation of a single node in the parser tree.

        Args:
            cmd: Parsed information about a command or subcommand.

        Returns:
            String representation of this subcommand.
        """
        return "    " * self.level + cmd.prog + "\n"


_positional_to_subroutine: Dict[str, str] = {
    "package": "_all_packages",
    "spec": "_all_packages",
    "filter": "_all_packages",
    "installed": "_installed_packages",
    "compiler": "_installed_compilers",
    "section": "_config_sections",
    "env": "_environments",
    "extendable": "_extensions",
    "keys": "_keys",
    "help_command": "_subcommands",
    "mirror": "_mirrors",
    "virtual": "_providers",
    "namespace": "_repos",
    "hash": "_all_resource_hashes",
    "pytest": "_unit_tests",
}


class BashCompletionWriter(ArgparseWriter):
    """Write argparse output as bash programmable tab completion."""

    def format(self, cmd: Command) -> str:
        """Return the string representation of a single node in the parser tree.

        Args:
            cmd: Parsed information about a command or subcommand.

        Returns:
            String representation of this subcommand.
        """

        assert cmd.optionals  # we should always at least have -h, --help
        assert not (cmd.positionals and cmd.subcommands)  # one or the other

        # We only care about the arguments/flags, not the help messages
        positionals: Tuple[str, ...] = ()
        if cmd.positionals:
            positionals, _, _, _ = zip(*cmd.positionals)
        optionals, _, _, _, _ = zip(*cmd.optionals)
        subcommands: Tuple[str, ...] = ()
        if cmd.subcommands:
            _, subcommands, _ = zip(*cmd.subcommands)

        # Flatten lists of lists
        optionals = [x for xx in optionals for x in xx]

        return (
            self.start_function(cmd.prog)
            + self.body(positionals, optionals, subcommands)
            + self.end_function(cmd.prog)
        )

    def start_function(self, prog: str) -> str:
        """Return the syntax needed to begin a function definition.

        Args:
            prog: Program name.

        Returns:
            Function definition beginning.
        """
        name = prog.replace("-", "_").replace(" ", "_")
        return "\n_{0}() {{".format(name)

    def end_function(self, prog: str) -> str:
        """Return the syntax needed to end a function definition.

        Args:
            prog: Program name

        Returns:
            Function definition ending.
        """
        return "}\n"

    def body(
        self, positionals: Sequence[str], optionals: Sequence[str], subcommands: Sequence[str]
    ) -> str:
        """Return the body of the function.

        Args:
            positionals: List of positional arguments.
            optionals: List of optional arguments.
            subcommands: List of subcommand parsers.

        Returns:
            Function body.
        """
        if positionals:
            return f"""
    if $list_options
    then
        {self.optionals(optionals)}
    else
        {self.positionals(positionals)}
    fi
"""
        elif subcommands:
            return f"""
    if $list_options
    then
        {self.optionals(optionals)}
    else
        {self.subcommands(subcommands)}
    fi
"""
        else:
            return f"""
    {self.optionals(optionals)}
"""

    def positionals(self, positionals: Sequence[str]) -> str:
        """Return the syntax for reporting positional arguments.

        Args:
            positionals: List of positional arguments.

        Returns:
            Syntax for positional arguments.
        """
        # If match found, return function name
        for positional in positionals:
            for key, value in _positional_to_subroutine.items():
                if positional.startswith(key):
                    return value

        # If no matches found, return empty list
        return 'SPACK_COMPREPLY=""'

    def optionals(self, optionals: Sequence[str]) -> str:
        """Return the syntax for reporting optional flags.

        Args:
            optionals: List of optional arguments.

        Returns:
            Syntax for optional flags.
        """
        return f'SPACK_COMPREPLY="{" ".join(optionals)}"'

    def subcommands(self, subcommands: Sequence[str]) -> str:
        """Return the syntax for reporting subcommands.

        Args:
            subcommands: List of subcommand parsers.

        Returns:
            Syntax for subcommand parsers
        """
        return f'SPACK_COMPREPLY="{" ".join(subcommands)}"'


# Map argument destination names to their complete commands
# Earlier items in the list have higher precedence
_dest_to_fish_complete = {
    ("activate", "view"): "-f -a '(__fish_complete_directories)'",
    ("bootstrap root", "path"): "-f -a '(__fish_complete_directories)'",
    ("mirror add", "mirror"): "-f",
    ("repo add", "path"): "-f -a '(__fish_complete_directories)'",
    ("test find", "filter"): "-f -a '(__fish_spack_tests)'",
    ("bootstrap", "name"): "-f -a '(__fish_spack_bootstrap_names)'",
    ("buildcache create", "key"): "-f -a '(__fish_spack_gpg_keys)'",
    ("build-env", r"spec \[--\].*"): "-f -a '(__fish_spack_build_env_spec)'",
    ("checksum", "package"): "-f -a '(__fish_spack_packages)'",
    (
        "checksum",
        "versions",
    ): "-f -a '(__fish_spack_package_versions $__fish_spack_argparse_argv[1])'",
    ("config", "path"): "-f -a '(__fish_spack_colon_path)'",
    ("config", "section"): "-f -a '(__fish_spack_config_sections)'",
    ("develop", "specs?"): "-f -k -a '(__fish_spack_specs_or_id)'",
    ("diff", "specs?"): "-f -a '(__fish_spack_installed_specs)'",
    ("gpg sign", "output"): "-f -a '(__fish_complete_directories)'",
    ("gpg", "keys?"): "-f -a '(__fish_spack_gpg_keys)'",
    ("graph", "specs?"): "-f -k -a '(__fish_spack_specs_or_id)'",
    ("help", "help_command"): "-f -a '(__fish_spack_commands)'",
    ("list", "filter"): "-f -a '(__fish_spack_packages)'",
    ("mirror", "mirror"): "-f -a '(__fish_spack_mirrors)'",
    ("pkg", "package"): "-f -a '(__fish_spack_pkg_packages)'",
    ("remove", "specs?"): "-f -a '(__fish_spack_installed_specs)'",
    ("repo", "namespace_or_path"): "$__fish_spack_force_files -a '(__fish_spack_repos)'",
    ("restage", "specs?"): "-f -k -a '(__fish_spack_specs_or_id)'",
    ("rm", "specs?"): "-f -a '(__fish_spack_installed_specs)'",
    ("solve", "specs?"): "-f -k -a '(__fish_spack_specs_or_id)'",
    ("spec", "specs?"): "-f -k -a '(__fish_spack_specs_or_id)'",
    ("stage", "specs?"): "-f -k -a '(__fish_spack_specs_or_id)'",
    ("test-env", r"spec \[--\].*"): "-f -a '(__fish_spack_build_env_spec)'",
    ("test", r"\[?name.*"): "-f -a '(__fish_spack_tests)'",
    ("undevelop", "specs?"): "-f -k -a '(__fish_spack_specs_or_id)'",
    ("verify", "specs_or_files"): "$__fish_spack_force_files -a '(__fish_spack_installed_specs)'",
    ("view", "path"): "-f -a '(__fish_complete_directories)'",
    ("", "comment"): "-f",
    ("", "compiler_spec"): "-f -a '(__fish_spack_installed_compilers)'",
    ("", "config_scopes"): "-f -a '(__fish_complete_directories)'",
    ("", "extendable"): "-f -a '(__fish_spack_extensions)'",
    ("", "installed_specs?"): "-f -a '(__fish_spack_installed_specs)'",
    ("", "job_url"): "-f",
    ("", "location_env"): "-f -a '(__fish_complete_directories)'",
    ("", "pytest_args"): "-f -a '(__fish_spack_unit_tests)'",
    ("", "package_or_file"): "$__fish_spack_force_files -a '(__fish_spack_packages)'",
    ("", "package_or_user"): "-f -a '(__fish_spack_packages)'",
    ("", "package"): "-f -a '(__fish_spack_packages)'",
    ("", "PKG"): "-f -a '(__fish_spack_packages)'",
    ("", "prefix"): "-f -a '(__fish_complete_directories)'",
    ("", r"rev\d?"): "-f -a '(__fish_spack_git_rev)'",
    ("", "specs?"): "-f -k -a '(__fish_spack_specs)'",
    ("", "tags?"): "-f -a '(__fish_spack_tags)'",
    ("", "virtual_package"): "-f -a '(__fish_spack_providers)'",
    ("", "working_dir"): "-f -a '(__fish_complete_directories)'",
    ("", r"(\w*_)?env"): "-f -a '(__fish_spack_environments)'",
    ("", r"(\w*_)?dir(ectory)?"): "-f -a '(__fish_spack_environments)'",
    ("", r"(\w*_)?mirror_name"): "-f -a '(__fish_spack_mirrors)'",
}


def _fish_dest_get_complete(prog: str, dest: str) -> Optional[str]:
    """Map from subcommand to autocompletion argument.

    Args:
        prog: Program name.
        dest: Destination.

    Returns:
        Autocompletion argument.
    """
    s = prog.split(None, 1)
    subcmd = s[1] if len(s) == 2 else ""

    for (prog_key, pos_key), value in _dest_to_fish_complete.items():
        if subcmd.startswith(prog_key) and re.match(f"^{pos_key}$", dest):
            return value
    return None


class FishCompletionWriter(ArgparseWriter):
    """Write argparse output as bash programmable tab completion."""

    def format(self, cmd: Command) -> str:
        """Return the string representation of a single node in the parser tree.

        Args:
            cmd: Parsed information about a command or subcommand.

        Returns:
            String representation of a node.
        """
        assert cmd.optionals  # we should always at least have -h, --help
        assert not (cmd.positionals and cmd.subcommands)  # one or the other

        # We also need help messages and how arguments are used
        # So we pass everything to completion writer
        positionals = cmd.positionals
        optionals = cmd.optionals
        subcommands = cmd.subcommands

        return (
            self.prog_comment(cmd.prog)
            + self.optspecs(cmd.prog, optionals)
            + self.complete(cmd.prog, positionals, optionals, subcommands)
        )

    def optspecs(
        self,
        prog: str,
        optionals: List[Tuple[Sequence[str], List[str], str, Union[int, str, None], str]],
    ) -> str:
        """Read the optionals and return the command to set optspec.

        Args:
            prog: Program name.
            optionals: List of optional arguments.

        Returns:
            Command to set optspec variable.
        """
        # Variables of optspecs
        optspec_var = "__fish_spack_optspecs_" + prog.replace(" ", "_").replace("-", "_")

        if optionals is None:
            return f"set -g {optspec_var}\n"

        # Build optspec by iterating over options
        args = []

        for flags, dest, _, nargs, _ in optionals:
            if len(flags) == 0:
                continue

            required = ""

            # Because nargs '?' is treated differently in fish, we treat it as required.
            # Because multi-argument options are not supported, we treat it like one argument.
            required = "="
            if nargs == 0:
                required = ""

            # Pair short options with long options

            # We need to do this because fish doesn't support multiple short
            # or long options.
            # However, since we are paring options only, this is fine

            short = [f[1:] for f in flags if f.startswith("-") and len(f) == 2]
            long = [f[2:] for f in flags if f.startswith("--")]

            while len(short) > 0 and len(long) > 0:
                arg = f"{short.pop()}/{long.pop()}{required}"
            while len(short) > 0:
                arg = f"{short.pop()}/{required}"
            while len(long) > 0:
                arg = f"{long.pop()}{required}"

            args.append(arg)

        # Even if there is no option, we still set variable.
        # In fish such variable is an empty array, we use it to
        # indicate that such subcommand exists.
        args = " ".join(args)

        return f"set -g {optspec_var} {args}\n"

    @staticmethod
    def complete_head(
        prog: str, index: Optional[int] = None, nargs: Optional[Union[int, str]] = None
    ) -> str:
        """Return the head of the completion command.

        Args:
            prog: Program name.
            index: Index of positional argument.
            nargs: Number of arguments.

        Returns:
            Head of the completion command.
        """
        # Split command and subcommand
        s = prog.split(None, 1)
        subcmd = s[1] if len(s) == 2 else ""

        if index is None:
            return f"complete -c {s[0]} -n '__fish_spack_using_command {subcmd}'"
        elif nargs in [argparse.ZERO_OR_MORE, argparse.ONE_OR_MORE, argparse.REMAINDER]:
            return (
                f"complete -c {s[0]} -n '__fish_spack_using_command_pos_remainder "
                f"{index} {subcmd}'"
            )
        else:
            return f"complete -c {s[0]} -n '__fish_spack_using_command_pos {index} {subcmd}'"

    def complete(
        self,
        prog: str,
        positionals: List[Tuple[str, Optional[Iterable[Any]], Union[int, str, None], str]],
        optionals: List[Tuple[Sequence[str], List[str], str, Union[int, str, None], str]],
        subcommands: List[Tuple[ArgumentParser, str, str]],
    ) -> str:
        """Return all the completion commands.

        Args:
            prog: Program name.
            positionals: List of positional arguments.
            optionals: List of optional arguments.
            subcommands: List of subcommand parsers.

        Returns:
            Completion command.
        """
        commands = []

        if positionals:
            commands.append(self.positionals(prog, positionals))

        if subcommands:
            commands.append(self.subcommands(prog, subcommands))

        if optionals:
            commands.append(self.optionals(prog, optionals))

        return "".join(commands)

    def positionals(
        self,
        prog: str,
        positionals: List[Tuple[str, Optional[Iterable[Any]], Union[int, str, None], str]],
    ) -> str:
        """Return the completion for positional arguments.

        Args:
            prog: Program name.
            positionals: List of positional arguments.

        Returns:
            Completion command.
        """
        commands = []

        for idx, (args, choices, nargs, help) in enumerate(positionals):
            # Make sure we always get same order of output
            if isinstance(choices, dict):
                choices = sorted(choices.keys())
            elif isinstance(choices, (set, frozenset)):
                choices = sorted(choices)

            # Remove platform-specific choices to avoid hard-coding the platform.
            if choices is not None:
                valid_choices = []
                for choice in choices:
                    if spack.platforms.host().name not in choice:
                        valid_choices.append(choice)
                choices = valid_choices

            head = self.complete_head(prog, idx, nargs)

            if choices is not None:
                # If there are choices, we provide a completion for all possible values.
                commands.append(f"{head} -f -a {shlex.quote(' '.join(choices))}")
            else:
                # Otherwise, we try to find a predefined completion for it
                value = _fish_dest_get_complete(prog, args)
                if value is not None:
                    commands.append(f"{head} {value}")

        return "\n".join(commands) + "\n"

    def prog_comment(self, prog: str) -> str:
        """Return a comment line for the command."""
        return f"\n# {prog}\n"

    def optionals(
        self,
        prog: str,
        optionals: List[Tuple[Sequence[str], List[str], str, Union[int, str, None], str]],
    ) -> str:
        """Return the completion for optional arguments.

        Args:
            prog: Program name.
            optionals: List of optional arguments.

        Returns:
            Completion command.
        """
        commands = []
        head = self.complete_head(prog)

        for flags, dest, _, nargs, help in optionals:
            # Make sure we always get same order of output
            if isinstance(dest, dict):
                dest = sorted(dest.keys())
            elif isinstance(dest, (set, frozenset)):
                dest = sorted(dest)

            # Remove platform-specific choices to avoid hard-coding the platform.
            if dest is not None:
                valid_choices = []
                for choice in dest:
                    if spack.platforms.host().name not in choice:
                        valid_choices.append(choice)
                dest = valid_choices

            # To provide description for optionals, and also possible values,
            # we need to use two split completion command.
            # Otherwise, each option will have same description.
            prefix = head

            # Add all flags to the completion
            for f in flags:
                if f.startswith("--"):
                    long = f[2:]
                    prefix = f"{prefix} -l {long}"
                elif f.startswith("-"):
                    short = f[1:]
                    assert len(short) == 1
                    prefix = f"{prefix} -s {short}"

            # Check if option require argument.
            # Currently multi-argument options are not supported, so we treat it like one argument.
            if nargs != 0:
                prefix = f"{prefix} -r"

            if dest is not None:
                # If there are choices, we provide a completion for all possible values.
                commands.append(f"{prefix} -f -a {shlex.quote(' '.join(dest))}")
            else:
                # Otherwise, we try to find a predefined completion for it
                value = _fish_dest_get_complete(prog, dest)
                if value is not None:
                    commands.append(f"{prefix} {value}")

            if help:
                commands.append(f"{prefix} -d {shlex.quote(help)}")

        return "\n".join(commands) + "\n"

    def subcommands(self, prog: str, subcommands: List[Tuple[ArgumentParser, str, str]]) -> str:
        """Return the completion for subcommands.

        Args:
            prog: Program name.
            subcommands: List of subcommand parsers.

        Returns:
            Completion command.
        """
        commands = []
        head = self.complete_head(prog, 0)

        for _, subcommand, help in subcommands:
            command = f"{head} -f -a {shlex.quote(subcommand)}"

            if help is not None and len(help) > 0:
                help = help.split("\n")[0]
                command = f"{command} -d {shlex.quote(help)}"

            commands.append(command)

        return "\n".join(commands) + "\n"


@formatter
def subcommands(args: Namespace, out: IO) -> None:
    """Hierarchical tree of subcommands.

    args:
        args: Command-line arguments.
        out: File object to write to.
    """
    parser = spack.main.make_argument_parser()
    spack.main.add_all_commands(parser)
    writer = SubcommandWriter(parser.prog, out, args.aliases)
    writer.write(parser)


def rst_index(out: IO) -> None:
    """Generate an index of all commands.

    Args:
        out: File object to write to.
    """
    out.write("\n")

    index = spack.main.index_commands()
    sections = index["long"]

    dmax = max(len(section_descriptions.get(s, s)) for s in sections) + 2
    cmax = max(len(c) for _, c in sections.items()) + 60

    row = "%s  %s\n" % ("=" * dmax, "=" * cmax)
    line = "%%-%ds  %%s\n" % dmax

    out.write(row)
    out.write(line % (" Category ", " Commands "))
    out.write(row)
    for section, commands in sorted(sections.items()):
        description = section_descriptions.get(section, section)

        for i, cmd in enumerate(sorted(commands)):
            description = description.capitalize() if i == 0 else ""
            ref = f":ref:`{cmd} <spack-{cmd}>`"
            comma = "," if i != len(commands) - 1 else ""
            bar = "| " if i % 8 == 0 else "  "
            out.write(line % (description, bar + ref + comma))
    out.write(row)


@formatter
def rst(args: Namespace, out: IO) -> None:
    """ReStructuredText documentation of subcommands.

    args:
        args: Command-line arguments.
        out: File object to write to.
    """
    # create a parser with all commands
    parser = spack.main.make_argument_parser()
    spack.main.add_all_commands(parser)

    # extract cross-refs of the form `_cmd-spack-<cmd>:` from rst files
    documented_commands: Set[str] = set()
    for filename in args.rst_files:
        with open(filename) as f:
            for line in f:
                match = re.match(r"\.\. _cmd-(spack-.*):", line)
                if match:
                    documented_commands.add(match.group(1).strip())

    # print an index to each command
    rst_index(out)
    out.write("\n")

    # print sections for each command and subcommand
    writer = SpackArgparseRstWriter(parser.prog, out, args.aliases, documented_commands)
    writer.write(parser)


@formatter
def names(args: Namespace, out: IO) -> None:
    """Simple list of top-level commands.

    args:
        args: Command-line arguments.
        out: File object to write to.
    """
    commands = copy.copy(spack.cmd.all_commands())

    if args.aliases:
        aliases = spack.config.get("config:aliases")
        if aliases:
            commands.extend(aliases.keys())

    colify(commands, output=out)


@formatter
def bash(args: Namespace, out: IO) -> None:
    """Bash tab-completion script.

    args:
        args: Command-line arguments.
        out: File object to write to.
    """
    parser = spack.main.make_argument_parser()
    spack.main.add_all_commands(parser)

    aliases_config = spack.config.get("config:aliases")
    if aliases_config:
        aliases = ";".join(f"{key}:{val}" for key, val in aliases_config.items())
        out.write(f'SPACK_ALIASES="{aliases}"\n\n')

    writer = BashCompletionWriter(parser.prog, out, args.aliases)
    writer.write(parser)


@formatter
def fish(args, out):
    parser = spack.main.make_argument_parser()
    spack.main.add_all_commands(parser)

    writer = FishCompletionWriter(parser.prog, out, args.aliases)
    writer.write(parser)


def prepend_header(args: Namespace, out: IO) -> None:
    """Prepend header text at the beginning of a file.

    Args:
        args: Command-line arguments.
        out: File object to write to.
    """
    if not args.header:
        return

    with open(args.header) as header:
        out.write(header.read())


def _commands(parser: ArgumentParser, args: Namespace) -> None:
    """This is the 'regular' command, which can be called multiple times.

    See ``commands()`` below for ``--update-completion`` handling.

    Args:
        parser: Argument parser.
        args: Command-line arguments.
    """
    formatter = formatters[args.format]

    # check header first so we don't open out files unnecessarily
    if args.header and not os.path.exists(args.header):
        tty.die(f"No such file: '{args.header}'")

    if args.update:
        tty.msg(f"Updating file: {args.update}")
        with open(args.update, "w") as f:
            prepend_header(args, f)
            formatter(args, f)

    else:
        prepend_header(args, sys.stdout)
        formatter(args, sys.stdout)


def update_completion(parser: ArgumentParser, args: Namespace) -> None:
    """Iterate through the shells and update the standard completion files.

    This is a convenience method to avoid calling this command many
    times, and to simplify completion update for developers.

    Args:
        parser: Argument parser.
        args: Command-line arguments.
    """
    for shell, shell_args in update_completion_args.items():
        for attr, value in shell_args.items():
            setattr(args, attr, value)
        _commands(parser, args)


def commands(parser: ArgumentParser, args: Namespace) -> None:
    """Main function that calls formatter functions.

    Args:
        parser: Argument parser.
        args: Command-line arguments.
    """
    if args.update_completion:
        if args.format != "names" or any([args.aliases, args.update, args.header]):
            tty.die("--update-completion can only be specified alone.")

        # this runs the command multiple times with different arguments
        update_completion(parser, args)

    else:
        # run commands normally
        _commands(parser, args)
