# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This is the implementation of the Spack command line executable.

In a normal Spack installation, this is invoked from the bin/spack script
after the system path is set up.
"""
from __future__ import print_function

import sys
import re
import os
import os.path
import inspect
import pstats
import argparse
import traceback
import warnings
from six import StringIO

import llnl.util.cpu
import llnl.util.filesystem as fs
import llnl.util.tty as tty
import llnl.util.tty.color as color
from llnl.util.tty.log import log_output

import spack
import spack.architecture
import spack.config
import spack.cmd
import spack.environment as ev
import spack.paths
import spack.repo
import spack.store
import spack.util.debug
import spack.util.path
import spack.util.executable as exe
from spack.error import SpackError


#: names of profile statistics
stat_names = pstats.Stats.sort_arg_dict_default

#: top-level aliases for Spack commands
aliases = {
    'rm': 'remove'
}

#: help levels in order of detail (i.e., number of commands shown)
levels = ['short', 'long']

#: intro text for help at different levels
intro_by_level = {
    'short': 'These are common spack commands:',
    'long':  'Complete list of spack commands:',
}

#: control top-level spack options shown in basic vs. advanced help
options_by_level = {
    'short': ['h', 'k', 'V', 'color'],
    'long': 'all'
}

#: Longer text for each section, to show in help
section_descriptions = {
    'admin':       'administration',
    'basic':       'query packages',
    'build':       'build packages',
    'config':      'configuration',
    'developer':   'developer',
    'environment': 'environment',
    'extensions':  'extensions',
    'help':        'more help',
    'packaging':   'create packages',
    'system':      'system',
}

#: preferential command order for some sections (e.g., build pipeline is
#: in execution order, not alphabetical)
section_order = {
    'basic': ['list', 'info', 'find'],
    'build': ['fetch', 'stage', 'patch', 'configure', 'build', 'restage',
              'install', 'uninstall', 'clean'],
    'packaging': ['create', 'edit']
}

#: Properties that commands are required to set.
required_command_properties = ['level', 'section', 'description']

#: Recorded directory where spack command was originally invoked
spack_working_dir = None
spack_ld_library_path = os.environ.get('LD_LIBRARY_PATH', '')


def set_working_dir():
    """Change the working directory to getcwd, or spack prefix if no cwd."""
    global spack_working_dir
    try:
        spack_working_dir = os.getcwd()
    except OSError:
        os.chdir(spack.paths.prefix)
        spack_working_dir = spack.paths.prefix


def add_all_commands(parser):
    """Add all spack subcommands to the parser."""
    for cmd in spack.cmd.all_commands():
        parser.add_command(cmd)


def get_version():
    """Get a descriptive version of this instance of Spack.

    If this is a git repository, and if it is not on a release tag,
    return a string like:

        release_version-commits_since_release-commit

    If we *are* at a release tag, or if this is not a git repo, return
    the real spack release number (e.g., 0.13.3).

    """
    git_path = os.path.join(spack.paths.prefix, ".git")
    if os.path.exists(git_path):
        git = exe.which("git")
        if git:
            with fs.working_dir(spack.paths.prefix):
                desc = git(
                    "describe", "--tags", output=str, fail_on_error=False)

            if git.returncode == 0:
                match = re.match(r"v([^-]+)-([^-]+)-g([a-f\d]+)", desc)
                if match:
                    v, n, commit = match.groups()
                    return "%s-%s-%s" % (v, n, commit)

    return spack.spack_version


def index_commands():
    """create an index of commands by section for this help level"""
    index = {}
    for command in spack.cmd.all_commands():
        cmd_module = spack.cmd.get_module(command)

        # make sure command modules have required properties
        for p in required_command_properties:
            prop = getattr(cmd_module, p, None)
            if not prop:
                tty.die("Command doesn't define a property '%s': %s"
                        % (p, command))

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
        usage = super(
            SpackHelpFormatter, self)._format_actions_usage(actions, groups)

        # compress single-character flags that are not mutually exclusive
        # at the beginning of the usage string
        chars = ''.join(re.findall(r'\[-(.)\]', usage))
        usage = re.sub(r'\[-.\] ?', '', usage)
        if chars:
            return '[-%s] %s' % (chars, usage)
        else:
            return usage


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
        if not hasattr(self, 'actions'):
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
            cmds = dict((a.dest, a) for a in self.actions
                        if a.dest in cmd_set)

            # add commands to a group in order, and add the group
            group = argparse._ArgumentGroup(self, title=title)
            for name in commands:
                group._add_action(cmds[name])
                if name in remaining:
                    remaining.remove(name)
            add_group(group)

        # select only the options for the particular level we're showing.
        show_options = options_by_level[level]
        if show_options != 'all':
            opts = dict((opt.option_strings[0].strip('-'), opt)
                        for opt in self._optionals._group_actions)

            new_actions = [opts[letter] for letter in show_options]
            self._optionals._group_actions = new_actions

        # custom, more concise usage for top level
        help_options = self._optionals._group_actions
        help_options = help_options + [self._positionals._group_actions[-1]]
        formatter.add_usage(
            self.usage, help_options, self._mutually_exclusive_groups)

        # description
        formatter.add_text(self.description)

        # start subcommands
        formatter.add_text(intro_by_level[level])

        # add argument groups based on metadata in commands
        index = index_commands()
        sections = index[level]

        for section in sorted(sections):
            if section == 'help':
                continue   # Cover help in the epilog.

            group_description = section_descriptions.get(section, section)

            to_display = sections[section]
            commands = []

            # add commands whose order we care about first.
            if section in section_order:
                commands.extend(cmd for cmd in section_order[section]
                                if cmd in to_display)

            # add rest in alphabetical order.
            commands.extend(cmd for cmd in sorted(sections[section])
                            if cmd not in commands)

            # add the group to the parser
            add_subcommand_group(group_description, commands)

        # optionals
        add_group(self._optionals)

        # epilog
        formatter.add_text("""\
{help}:
  spack help --all       list all commands and options
  spack help <command>   help on a specific command
  spack help --spec      help on the package specification syntax
  spack docs             open http://spack.rtfd.io/ in a browser
""".format(help=section_descriptions['help']))

        # determine help from format above
        return formatter.format_help()

    def add_subparsers(self, **kwargs):
        """Ensure that sensible defaults are propagated to subparsers"""
        kwargs.setdefault('metavar', 'SUBCOMMAND')
        sp = super(SpackArgumentParser, self).add_subparsers(**kwargs)
        old_add_parser = sp.add_parser

        def add_parser(name, **kwargs):
            kwargs.setdefault('formatter_class', SpackHelpFormatter)
            return old_add_parser(name, **kwargs)
        sp.add_parser = add_parser
        return sp

    def add_command(self, cmd_name):
        """Add one subcommand to this parser."""
        # lazily initialize any subparsers
        if not hasattr(self, 'subparsers'):
            # remove the dummy "command" argument.
            if self._actions[-1].dest == 'command':
                self._remove_action(self._actions[-1])
            self.subparsers = self.add_subparsers(metavar='COMMAND',
                                                  dest="command")

        # each command module implements a parser() function, to which we
        # pass its subparser for setup.
        module = spack.cmd.get_module(cmd_name)

        # build a list of aliases
        alias_list = [k for k, v in aliases.items() if v == cmd_name]

        subparser = self.subparsers.add_parser(
            cmd_name, aliases=alias_list,
            help=module.description, description=module.description)
        module.setup_parser(subparser)

        # return the callable function for the command
        return spack.cmd.get_command(cmd_name)

    def format_help(self, level='short'):
        if self.prog == 'spack':
            # use format_help_sections for the main spack parser, but not
            # for subparsers
            return self.format_help_sections(level)
        else:
            # in subparsers, self.prog is, e.g., 'spack install'
            return super(SpackArgumentParser, self).format_help()


def make_argument_parser(**kwargs):
    """Create an basic argument parser without any subcommands added."""
    parser = SpackArgumentParser(
        formatter_class=SpackHelpFormatter, add_help=False,
        description=(
            "A flexible package manager that supports multiple versions,\n"
            "configurations, platforms, and compilers."),
        **kwargs)

    # stat names in groups of 7, for nice wrapping.
    stat_lines = list(zip(*(iter(stat_names),) * 7))

    parser.add_argument(
        '-h', '--help',
        dest='help', action='store_const', const='short', default=None,
        help="show this help message and exit")
    parser.add_argument(
        '-H', '--all-help',
        dest='help', action='store_const', const='long', default=None,
        help="show help for all commands (same as spack help --all)")
    parser.add_argument(
        '--color', action='store', default='auto',
        choices=('always', 'never', 'auto'),
        help="when to colorize output (default: auto)")
    parser.add_argument(
        '-C', '--config-scope', dest='config_scopes', action='append',
        metavar='DIR', help="add a custom configuration scope")
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help="write out debug logs during compile")
    parser.add_argument(
        '--timestamp', action='store_true',
        help="Add a timestamp to tty output")
    parser.add_argument(
        '--pdb', action='store_true',
        help="run spack under the pdb debugger")

    env_group = parser.add_mutually_exclusive_group()
    env_group.add_argument(
        '-e', '--env', dest='env', metavar='ENV', action='store',
        help="run with a specific environment (see spack env)")
    env_group.add_argument(
        '-D', '--env-dir', dest='env_dir', metavar='DIR', action='store',
        help="run with an environment directory (ignore named environments)")
    env_group.add_argument(
        '-E', '--no-env', dest='no_env', action='store_true',
        help="run without any environments activated (see spack env)")
    parser.add_argument(
        '--use-env-repo', action='store_true',
        help="when running in an environment, use its package repository")

    parser.add_argument(
        '-k', '--insecure', action='store_true',
        help="do not check ssl certificates when downloading")
    parser.add_argument(
        '-l', '--enable-locks', action='store_true', dest='locks',
        default=None, help="use filesystem locking (default)")
    parser.add_argument(
        '-L', '--disable-locks', action='store_false', dest='locks',
        help="do not use filesystem locking (unsafe)")
    parser.add_argument(
        '-m', '--mock', action='store_true',
        help="use mock packages instead of real ones")
    parser.add_argument(
        '-p', '--profile', action='store_true', dest='spack_profile',
        help="profile execution using cProfile")
    parser.add_argument(
        '--sorted-profile', default=None, metavar="STAT",
        help="profile and sort by one or more of:\n[%s]" %
        ',\n '.join([', '.join(line) for line in stat_lines]))
    parser.add_argument(
        '--lines', default=20, action='store',
        help="lines of profile output or 'all' (default: 20)")
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help="print additional output during builds")
    parser.add_argument(
        '--stacktrace', action='store_true',
        help="add stacktraces to all printed statements")
    parser.add_argument(
        '-V', '--version', action='store_true',
        help='show version number and exit')
    parser.add_argument(
        '--print-shell-vars', action='store',
        help="print info needed by setup-env.[c]sh")

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

    # debug must be set first so that it can even affect behvaior of
    # errors raised by spack.config.
    if args.debug:
        spack.error.debug = True
        spack.util.debug.register_interrupt_handler()
        spack.config.set('config:debug', True, scope='command_line')

    if args.timestamp:
        tty.set_timestamp(True)

    # override lock configuration if passed on command line
    if args.locks is not None:
        spack.util.lock.check_lock_safety(spack.paths.prefix)
        spack.config.set('config:locks', False, scope='command_line')

    if args.mock:
        rp = spack.repo.RepoPath(spack.paths.mock_packages_path)
        spack.repo.set_path(rp)

    # If the user asked for it, don't check ssl certs.
    if args.insecure:
        tty.warn("You asked for --insecure. Will NOT check SSL certificates.")
        spack.config.set('config:verify_ssl', False, scope='command_line')

    # when to use color (takes always, auto, or never)
    color.set_color_when(args.color)


def allows_unknown_args(command):
    """Implements really simple argument injection for unknown arguments.

    Commands may add an optional argument called "unknown args" to
    indicate they can handle unknonwn args, and we'll pass the unknown
    args in.
    """
    info = dict(inspect.getmembers(command))
    varnames = info['__code__'].co_varnames
    argcount = info['__code__'].co_argcount
    return (argcount == 3 and varnames[2] == 'unknown_args')


def _invoke_command(command, parser, args, unknown_args):
    """Run a spack command *without* setting spack global options."""
    if allows_unknown_args(command):
        return_val = command(parser, args, unknown_args)
    else:
        if unknown_args:
            tty.die('unrecognized arguments: %s' % ' '.join(unknown_args))
        return_val = command(parser, args)

    # Allow commands to return and error code if they want
    return 0 if return_val is None else return_val


class SpackCommand(object):
    """Callable object that invokes a spack command (for testing).

    Example usage::

        install = SpackCommand('install')
        install('-v', 'mpich')

    Use this to invoke Spack commands directly from Python and check
    their output.
    """
    def __init__(self, command_name):
        """Create a new SpackCommand that invokes ``command_name`` when called.

        Args:
            command_name (str): name of the command to invoke
        """
        self.parser = make_argument_parser()
        self.command = self.parser.add_command(command_name)
        self.command_name = command_name

    def __call__(self, *argv, **kwargs):
        """Invoke this SpackCommand.

        Args:
            argv (list of str): command line arguments.

        Keyword Args:
            fail_on_error (optional bool): Don't raise an exception on error

        Returns:
            (str): combined output and error as a string

        On return, if ``fail_on_error`` is False, return value of command
        is set in ``returncode`` property, and the error is set in the
        ``error`` property.  Otherwise, raise an error.
        """
        # set these before every call to clear them out
        self.returncode = None
        self.error = None

        args, unknown = self.parser.parse_known_args(
            [self.command_name] + list(argv))

        fail_on_error = kwargs.get('fail_on_error', True)

        out = StringIO()
        try:
            with log_output(out):
                self.returncode = _invoke_command(
                    self.command, self.parser, args, unknown)

        except SystemExit as e:
            self.returncode = e.code

        except BaseException as e:
            tty.debug(e)
            self.error = e
            if fail_on_error:
                self._log_command_output(out)
                raise

        if fail_on_error and self.returncode not in (None, 0):
            self._log_command_output(out)
            raise SpackCommandError(
                "Command exited with code %d: %s(%s)" % (
                    self.returncode, self.command_name,
                    ', '.join("'%s'" % a for a in argv)))

        return out.getvalue()

    def _log_command_output(self, out):
        if tty.is_verbose():
            fmt = self.command_name + ': {0}'
            for ln in out.getvalue().split('\n'):
                if len(ln) > 0:
                    tty.verbose(fmt.format(ln.replace('==> ', '')))


def _profile_wrapper(command, parser, args, unknown_args):
    import cProfile

    try:
        nlines = int(args.lines)
    except ValueError:
        if args.lines != 'all':
            tty.die('Invalid number for --lines: %s' % args.lines)
        nlines = -1

    # allow comma-separated list of fields
    sortby = ['time']
    if args.sorted_profile:
        sortby = args.sorted_profile.split(',')
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
        stats = pstats.Stats(pr)
        stats.sort_stats(*sortby)
        stats.print_stats(nlines)


def print_setup_info(*info):
    """Print basic information needed by setup-env.[c]sh.

    Args:
        info (list of str): list of things to print: comma-separated list
            of 'csh', 'sh', or 'modules'

    This is in ``main.py`` to make it fast; the setup scripts need to
    invoke spack in login scripts, and it needs to be quick.

    """
    shell = 'csh' if 'csh' in info else 'sh'

    def shell_set(var, value):
        if shell == 'sh':
            print("%s='%s'" % (var, value))
        elif shell == 'csh':
            print("set %s = '%s'" % (var, value))
        else:
            tty.die('shell must be sh or csh')

    # print sys type
    shell_set('_sp_sys_type', spack.architecture.sys_type())
    shell_set('_sp_compatible_sys_types',
              ':'.join(spack.architecture.compatible_sys_types()))
    # print roots for all module systems
    module_to_roots = {
        'tcl': list(),
        'lmod': list()
    }
    module_roots = spack.config.get('config:module_roots')
    module_roots = dict(
        (k, v) for k, v in module_roots.items() if k in module_to_roots
    )
    for name, path in module_roots.items():
        path = spack.util.path.canonicalize_path(path)
        module_to_roots[name].append(path)

    other_spack_instances = spack.config.get(
        'upstreams') or {}

    for install_properties in other_spack_instances.values():
        upstream_module_roots = install_properties.get('modules', {})
        upstream_module_roots = dict(
            (k, v) for k, v in upstream_module_roots.items()
            if k in module_to_roots
        )
        for module_type, root in upstream_module_roots.items():
            module_to_roots[module_type].append(root)

    for name, paths in module_to_roots.items():
        # Environment setup prepends paths, so the order is reversed here to
        # preserve the intended priority: the modules of the local Spack
        # instance are the highest-precedence.
        roots_val = ':'.join(reversed(paths))
        shell_set('_sp_%s_roots' % name, roots_val)

    # print environment module system if available. This can be expensive
    # on clusters, so skip it if not needed.
    if 'modules' in info:
        generic_arch = llnl.util.cpu.host().family
        module_spec = 'environment-modules target={0}'.format(generic_arch)
        specs = spack.store.db.query(module_spec)
        if specs:
            shell_set('_sp_module_prefix', specs[-1].prefix)
        else:
            shell_set('_sp_module_prefix', 'not_installed')


def main(argv=None):
    """This is the entry point for the Spack command.

    Args:
        argv (list of str or None): command line arguments, NOT including
            the executable name. If None, parses from sys.argv.
    """
    # Create a parser with a simple positional argument first.  We'll
    # lazily load the subcommand(s) we need later. This allows us to
    # avoid loading all the modules from spack.cmd when we don't need
    # them, which reduces startup latency.
    parser = make_argument_parser()
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args, unknown = parser.parse_known_args(argv)

    # Recover stored LD_LIBRARY_PATH variables from spack shell function
    # This is necessary because MacOS System Integrity Protection clears
    # (DY?)LD_LIBRARY_PATH variables on process start.
    # Spack clears these variables before building and installing packages,
    # but needs to know the prior state for commands like `spack load` and
    # `spack env activate that modify the user environment.
    recovered_vars = (
        'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'DYLD_FALLBACK_LIBRARY_PATH'
    )
    for var in recovered_vars:
        stored_var_name = 'SPACK_%s' % var
        if stored_var_name in os.environ:
            os.environ[var] = os.environ[stored_var_name]

    # activate an environment if one was specified on the command line
    if not args.no_env:
        env = ev.find_environment(args)
        if env:
            ev.activate(env, args.use_env_repo)

    # make spack.config aware of any command line configuration scopes
    if args.config_scopes:
        spack.config.command_line_scopes = args.config_scopes

    if args.print_shell_vars:
        print_setup_info(*args.print_shell_vars.split(','))
        return 0

    # Just print help and exit if run with no arguments at all
    no_args = (len(sys.argv) == 1) if argv is None else (len(argv) == 0)
    if no_args:
        parser.print_help()
        return 1

    # -h, -H, and -V are special as they do not require a command, but
    # all the other options do nothing without a command.
    if args.version:
        print(get_version())
        return 0
    elif args.help:
        sys.stdout.write(parser.format_help(level=args.help))
        return 0
    elif not args.command:
        parser.print_help()
        return 1

    try:
        # ensure options on spack command come before everything
        setup_main_options(args)

        # Try to load the particular command the caller asked for.
        cmd_name = args.command[0]
        cmd_name = aliases.get(cmd_name, cmd_name)

        command = parser.add_command(cmd_name)

        # Re-parse with the proper sub-parser added.
        args, unknown = parser.parse_known_args()

        # many operations will fail without a working directory.
        set_working_dir()

        # now we can actually execute the command.
        if args.spack_profile or args.sorted_profile:
            _profile_wrapper(command, parser, args, unknown)
        elif args.pdb:
            import pdb
            pdb.runctx('_invoke_command(command, parser, args, unknown)',
                       globals(), locals())
            return 0
        else:
            return _invoke_command(command, parser, args, unknown)

    except SpackError as e:
        tty.debug(e)
        e.die()  # gracefully die on any SpackErrors

    except Exception as e:
        if spack.config.get('config:debug'):
            raise
        tty.die(e)

    except KeyboardInterrupt:
        if spack.config.get('config:debug'):
            raise
        sys.stderr.write('\n')
        tty.die("Keyboard interrupt.")

    except SystemExit as e:
        if spack.config.get('config:debug'):
            traceback.print_exc()
        return e.code


class SpackCommandError(Exception):
    """Raised when SpackCommand execution fails."""
