# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
import sys
from collections import namedtuple

import llnl.util.tty as tty
import llnl.util.filesystem as fs
from llnl.util.tty.colify import colify
from llnl.util.tty.color import colorize

import spack.config
import spack.schema.env
import spack.cmd.common.arguments
import spack.cmd.install
import spack.cmd.uninstall
import spack.cmd.modules
import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.util.string as string


description = "manage virtual environments"
section = "environments"
level = "short"


#: List of subcommands of `spack env`
subcommands = [
    'activate',
    'deactivate',
    'create',
    ['remove', 'rm'],
    ['list', 'ls'],
    ['status', 'st'],
    'loads',
    'view',
    'update',
    'revert'
]


#
# env activate
#
def env_activate_setup_parser(subparser):
    """set the current environment"""
    shells = subparser.add_mutually_exclusive_group()
    shells.add_argument(
        '--sh', action='store_const', dest='shell', const='sh',
        help="print sh commands to activate the environment")
    shells.add_argument(
        '--csh', action='store_const', dest='shell', const='csh',
        help="print csh commands to activate the environment")
    shells.add_argument(
        '--fish', action='store_const', dest='shell', const='fish',
        help="print fish commands to activate the environment")

    view_options = subparser.add_mutually_exclusive_group()
    view_options.add_argument(
        '-v', '--with-view', action='store_const', dest='with_view',
        const=True, default=True,
        help="update PATH etc. with associated view")
    view_options.add_argument(
        '-V', '--without-view', action='store_const', dest='with_view',
        const=False, default=True,
        help="do not update PATH etc. with associated view")

    subparser.add_argument(
        '-d', '--dir', action='store_true', default=False,
        help="force spack to treat env as a directory, not a name")
    subparser.add_argument(
        '-p', '--prompt', action='store_true', default=False,
        help="decorate the command line prompt when activating")
    subparser.add_argument(
        metavar='env', dest='activate_env',
        help='name of environment to activate')


def env_activate(args):
    env = args.activate_env
    if not args.shell:
        spack.cmd.common.shell_init_instructions(
            "spack env activate",
            "    eval `spack env activate {sh_arg} %s`" % env,
        )
        return 1

    if ev.exists(env) and not args.dir:
        spack_env = ev.root(env)
        short_name = env
        env_prompt = '[%s]' % env

    elif ev.is_env_dir(env):
        spack_env = os.path.abspath(env)
        short_name = os.path.basename(os.path.abspath(env))
        env_prompt = '[%s]' % short_name

    else:
        tty.die("No such environment: '%s'" % env)

    if spack_env == os.environ.get('SPACK_ENV'):
        tty.die("Environment %s is already active" % args.activate_env)

    active_env = ev.get_env(namedtuple('args', ['env'])(env),
                            'activate')
    cmds = ev.activate(
        active_env, add_view=args.with_view, shell=args.shell,
        prompt=env_prompt if args.prompt else None
    )
    sys.stdout.write(cmds)


#
# env deactivate
#
def env_deactivate_setup_parser(subparser):
    """deactivate any active environment in the shell"""
    shells = subparser.add_mutually_exclusive_group()
    shells.add_argument(
        '--sh', action='store_const', dest='shell', const='sh',
        help="print sh commands to deactivate the environment")
    shells.add_argument(
        '--csh', action='store_const', dest='shell', const='csh',
        help="print csh commands to deactivate the environment")
    shells.add_argument(
        '--fish', action='store_const', dest='shell', const='fish',
        help="print fish commands to activate the environment")


def env_deactivate(args):
    if not args.shell:
        spack.cmd.common.shell_init_instructions(
            "spack env deactivate",
            "    eval `spack env deactivate {sh_arg}`",
        )
        return 1

    if 'SPACK_ENV' not in os.environ:
        tty.die('No environment is currently active.')

    cmds = ev.deactivate(shell=args.shell)
    sys.stdout.write(cmds)


#
# env create
#
def env_create_setup_parser(subparser):
    """create a new environment"""
    subparser.add_argument(
        'create_env', metavar='env', help='name of environment to create')
    subparser.add_argument(
        '-d', '--dir', action='store_true',
        help='create an environment in a specific directory')
    subparser.add_argument(
        '--keep-relative', action='store_true',
        help='copy relative develop paths verbatim into the new environment'
             ' when initializing from envfile')
    view_opts = subparser.add_mutually_exclusive_group()
    view_opts.add_argument(
        '--without-view', action='store_true',
        help='do not maintain a view for this environment')
    view_opts.add_argument(
        '--with-view',
        help='specify that this environment should maintain a view at the'
             ' specified path (by default the view is maintained in the'
             ' environment directory)')
    subparser.add_argument(
        'envfile', nargs='?', default=None,
        help='optional init file; can be spack.yaml or spack.lock')


def env_create(args):
    if args.with_view:
        with_view = args.with_view
    elif args.without_view:
        with_view = False
    else:
        # Note that 'None' means unspecified, in which case the Environment
        # object could choose to enable a view by default. False means that
        # the environment should not include a view.
        with_view = None
    if args.envfile:
        with open(args.envfile) as f:
            _env_create(args.create_env, f, args.dir,
                        with_view=with_view, keep_relative=args.keep_relative)
    else:
        _env_create(args.create_env, None, args.dir,
                    with_view=with_view)


def _env_create(name_or_path, init_file=None, dir=False, with_view=None,
                keep_relative=False):
    """Create a new environment, with an optional yaml description.

    Arguments:
        name_or_path (str): name of the environment to create, or path to it
        init_file (str or file): optional initialization file -- can be
            spack.yaml or spack.lock
        dir (bool): if True, create an environment in a directory instead
            of a named environment
        keep_relative (bool): if True, develop paths are copied verbatim into
            the new environment file, otherwise they may be made absolute if the
            new environment is in a different location
    """
    if dir:
        env = ev.Environment(name_or_path, init_file, with_view, keep_relative)
        env.write()
        tty.msg("Created environment in %s" % env.path)
        tty.msg("You can activate this environment with:")
        tty.msg("  spack env activate %s" % env.path)
    else:
        env = ev.create(name_or_path, init_file, with_view, keep_relative)
        env.write()
        tty.msg("Created environment '%s' in %s" % (name_or_path, env.path))
        tty.msg("You can activate this environment with:")
        tty.msg("  spack env activate %s" % (name_or_path))
    return env


#
# env remove
#
def env_remove_setup_parser(subparser):
    """remove an existing environment"""
    subparser.add_argument(
        'rm_env', metavar='env', nargs='+',
        help='environment(s) to remove')
    arguments.add_common_arguments(subparser, ['yes_to_all'])


def env_remove(args):
    """Remove a *named* environment.

    This removes an environment managed by Spack. Directory environments
    and `spack.yaml` files embedded in repositories should be removed
    manually.
    """
    read_envs = []
    for env_name in args.rm_env:
        env = ev.read(env_name)
        read_envs.append(env)

    if not args.yes_to_all:
        answer = tty.get_yes_or_no(
            'Really remove %s %s?' % (
                string.plural(len(args.rm_env), 'environment', show_n=False),
                string.comma_and(args.rm_env)),
            default=False)
        if not answer:
            tty.die("Will not remove any environments")

    for env in read_envs:
        if env.active:
            tty.die("Environment %s can't be removed while activated."
                    % env.name)

        env.destroy()
        tty.msg("Successfully removed environment '%s'" % env.name)


#
# env list
#
def env_list_setup_parser(subparser):
    """list available environments"""


def env_list(args):
    names = ev.all_environment_names()

    color_names = []
    for name in names:
        if ev.active(name):
            name = colorize('@*g{%s}' % name)
        color_names.append(name)

    # say how many there are if writing to a tty
    if sys.stdout.isatty():
        if not names:
            tty.msg('No environments')
        else:
            tty.msg('%d environments' % len(names))

    colify(color_names, indent=4)


class ViewAction(object):
    regenerate = 'regenerate'
    enable = 'enable'
    disable = 'disable'

    @staticmethod
    def actions():
        return [ViewAction.regenerate, ViewAction.enable, ViewAction.disable]


#
# env view
#
def env_view_setup_parser(subparser):
    """manage a view associated with the environment"""
    subparser.add_argument(
        'action', choices=ViewAction.actions(),
        help="action to take for the environment's view")
    subparser.add_argument(
        'view_path', nargs='?',
        help="when enabling a view, optionally set the path manually"
    )


def env_view(args):
    env = ev.get_env(args, 'env view')

    if env:
        if args.action == ViewAction.regenerate:
            env.regenerate_views()
        elif args.action == ViewAction.enable:
            if args.view_path:
                view_path = args.view_path
            else:
                view_path = env.view_path_default
            env.update_default_view(view_path)
            env.write()
        elif args.action == ViewAction.disable:
            env.update_default_view(None)
            env.write()
    else:
        tty.msg("No active environment")


#
# env status
#
def env_status_setup_parser(subparser):
    """print whether there is an active environment"""


def env_status(args):
    env = ev.get_env(args, 'env status')
    if env:
        if env.path == os.getcwd():
            tty.msg('Using %s in current directory: %s'
                    % (ev.manifest_name, env.path))
        else:
            tty.msg('In environment %s' % env.name)

        # Check if environment views can be safely activated
        env.check_views()
    else:
        tty.msg('No active environment')


#
# env loads
#
def env_loads_setup_parser(subparser):
    """list modules for an installed environment '(see spack module loads)'"""
    subparser.add_argument(
        'env', nargs='?', help='name of env to generate loads file for')
    subparser.add_argument(
        '-m', '--module-type', choices=('tcl', 'lmod'),
        help='type of module system to generate loads for')
    spack.cmd.modules.add_loads_arguments(subparser)


def env_loads(args):
    env = ev.get_env(args, 'env loads', required=True)

    # Set the module types that have been selected
    module_type = args.module_type
    if module_type is None:
        # If no selection has been made select all of them
        module_type = 'tcl'

    recurse_dependencies = args.recurse_dependencies
    args.recurse_dependencies = False

    loads_file = fs.join_path(env.path, 'loads')
    with open(loads_file, 'w') as f:
        specs = env._get_environment_specs(
            recurse_dependencies=recurse_dependencies)

        spack.cmd.modules.loads(module_type, specs, args, f)

    print('To load this environment, type:')
    print('   source %s' % loads_file)


def env_update_setup_parser(subparser):
    """update environments to the latest format"""
    subparser.add_argument(
        metavar='env', dest='env',
        help='name or directory of the environment to activate'
    )
    spack.cmd.common.arguments.add_common_arguments(subparser, ['yes_to_all'])


def env_update(args):
    manifest_file = ev.manifest_file(args.env)
    backup_file = manifest_file + ".bkp"
    needs_update = not ev.is_latest_format(manifest_file)

    if not needs_update:
        tty.msg('No update needed for the environment "{0}"'.format(args.env))
        return

    proceed = True
    if not args.yes_to_all:
        msg = ('The environment "{0}" is going to be updated to the latest '
               'schema format.\nIf the environment is updated, versions of '
               'Spack that are older than this version may not be able to '
               'read it. Spack stores backups of the updated environment '
               'which can be retrieved with "spack env revert"')
        tty.msg(msg.format(args.env))
        proceed = tty.get_yes_or_no('Do you want to proceed?', default=False)

    if not proceed:
        tty.die('Operation aborted.')

    ev.update_yaml(manifest_file, backup_file=backup_file)
    msg = 'Environment "{0}" has been updated [backup={1}]'
    tty.msg(msg.format(args.env, backup_file))


def env_revert_setup_parser(subparser):
    """restore environments to their state before update"""
    subparser.add_argument(
        metavar='env', dest='env',
        help='name or directory of the environment to activate'
    )
    spack.cmd.common.arguments.add_common_arguments(subparser, ['yes_to_all'])


def env_revert(args):
    manifest_file = ev.manifest_file(args.env)
    backup_file = manifest_file + ".bkp"

    # Check that both the spack.yaml and the backup exist, the inform user
    # on what is going to happen and ask for confirmation
    if not os.path.exists(manifest_file):
        msg = 'cannot fine the manifest file of the environment [file={0}]'
        tty.die(msg.format(manifest_file))
    if not os.path.exists(backup_file):
        msg = 'cannot find the old manifest file to be restored [file={0}]'
        tty.die(msg.format(backup_file))

    proceed = True
    if not args.yes_to_all:
        msg = ('Spack is going to overwrite the current manifest file'
               ' with a backup copy [manifest={0}, backup={1}]')
        tty.msg(msg.format(manifest_file, backup_file))
        proceed = tty.get_yes_or_no('Do you want to proceed?', default=False)

    if not proceed:
        tty.die('Operation aborted.')

    shutil.copy(backup_file, manifest_file)
    os.remove(backup_file)
    msg = 'Environment "{0}" reverted to old state'
    tty.msg(msg.format(manifest_file))


#: Dictionary mapping subcommand names and aliases to functions
subcommand_functions = {}


#
# spack env
#
def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='env_command')

    for name in subcommands:
        if isinstance(name, (list, tuple)):
            name, aliases = name[0], name[1:]
        else:
            aliases = []

        # add commands to subcommands dict
        function_name = 'env_%s' % name
        function = globals()[function_name]
        for alias in [name] + aliases:
            subcommand_functions[alias] = function

        # make a subparser and run the command's setup function on it
        setup_parser_cmd_name = 'env_%s_setup_parser' % name
        setup_parser_cmd = globals()[setup_parser_cmd_name]

        subsubparser = sp.add_parser(
            name, aliases=aliases, help=setup_parser_cmd.__doc__)
        setup_parser_cmd(subsubparser)


def env(parser, args):
    """Look for a function called environment_<name> and call it."""
    action = subcommand_functions[args.env_command]
    action(args)
