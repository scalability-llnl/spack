# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys
import argparse
import shutil
import tempfile

import llnl.util.tty as tty
import llnl.util.filesystem as fs
from llnl.util.tty.colify import colify
from llnl.util.tty.color import colorize

import spack.config
import spack.schema.env
import spack.cmd.install
import spack.cmd.uninstall
import spack.cmd.modules
import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.util.string as string

description = "manage virtual environments"
section = "environment"
level = "long"


#: List of subcommands of `spack env`
subcommands = [
    'create',
    'destroy',
    ['list', 'ls'],
    'add',
    ['remove', 'rm'],
    'upgrade',
    'concretize',
    ['status', 'st'],
    'loads',
    'relocate',
    'stage',
    'install',
    'uninstall',
]


#
# env create
#
def env_create_setup_parser(subparser):
    """create a new environment"""
    subparser.add_argument('env', help='name of environment to create')
    subparser.add_argument('envfile', nargs='?', default=None,
                           help='YAML initialization file (optional)')


def env_create(args):
    if args.envfile:
        with open(args.envfile) as f:
            _environment_create(args.env, f)
    else:
        _environment_create(args.env)


def _environment_create(name, env_yaml=None):
    """Create a new environment, with an optional yaml description.

    Arguments:
        name (str): name of the environment to create
        env_yaml (str or file): yaml text or file object containing
            configuration information.
    """
    if os.path.exists(ev.root(name)):
        tty.die("'%s': environment already exists" % name)

    env = ev.Environment(name, env_yaml)
    env.write()
    tty.msg("Created environment '%s' in %s" % (name, env.path))
    return env


#
# env remove
#
def env_destroy_setup_parser(subparser):
    """destroy an existing environment"""
    subparser.add_argument(
        'env', nargs='+', help='environment(s) to destroy')
    arguments.add_common_arguments(subparser, ['yes_to_all'])


def env_destroy(args):
    for env in args.env:
        if not ev.exists(ev.root(env)):
            tty.die("No such environment: '%s'" % env)
        elif not os.access(ev.root(env), os.W_OK):
            tty.die("insufficient permissions to modify environment: '%s'"
                    % args.env)

    if not args.yes_to_all:
        answer = tty.get_yes_or_no(
            'Really destroy %s %s?' % (
                string.plural(len(args.env), 'environment', show_n=False),
                string.comma_and(args.env)),
            default=False)
        if not answer:
            tty.die("Will not destroy any environments")

    for env in args.env:
        ev.Environment(env).destroy()
        tty.msg("Successfully destroyed environment '%s'" % env)


#
# env list
#
def env_list_setup_parser(subparser):
    """list available environments"""
    pass


def env_list(args):
    names = ev.list_environments()

    color_names = []
    for name in names:
        if ev.active and name == ev.active.name:
            name = colorize('@*g{%s}' % name)
        color_names.append(name)

    # say how many there are if writing to a tty
    if sys.stdout.isatty():
        if not names:
            tty.msg('No environments')
        else:
            tty.msg('%d environments' % len(names))

    colify(color_names, indent=4)


#
# env add
#
def env_add_setup_parser(subparser):
    """add a spec to an environment"""
    subparser.add_argument(
        '-e', '--env', help='add spec to environment with this name')
    subparser.add_argument(
        'specs', nargs=argparse.REMAINDER, help="spec of the package to add")


def env_add(args):
    if not args.env:
        tty.die('spack env unadd requires an active env or argument')

    env = ev.read(args.env)
    for spec in spack.cmd.parse_specs(args.specs):
        if not env.add(spec):
            tty.msg("Package {0} was already added to {1}"
                    .format(spec.name, env.name))
        else:
            tty.msg('Adding %s to environment %s' % (spec, env.name))
    env.write()


#
# env remove
#
def env_remove_setup_parser(subparser):
    """remove a spec from an environment"""
    subparser.add_argument(
        '-e', '--env', help='remove spec with this name from environment')
    subparser.add_argument(
        '-a', '--all', action='store_true', dest='all',
        help="Remove all specs from (clear) the environment")
    subparser.add_argument(
        'specs', nargs=argparse.REMAINDER, help="specs to be removed")


def env_remove(args):
    env = get_env(args, 'remove')

    if args.all:
        env.clear()
    else:
        for spec in spack.cmd.parse_specs(args.specs):
            tty.msg('Removing %s from environment %s' % (spec, env.name))
            env.remove(spec)
    env.write()


#
# env concretize
#
def env_concretize_setup_parser(subparser):
    """concretize user specs and write lockfile"""
    subparser.add_argument(
        'env', nargs='?', help='concretize all packages for this environment')
    subparser.add_argument(
        '-f', '--force', action='store_true',
        help="Re-concretize even if already concretized.")


def env_concretize(args):
    if not args.env:
        tty.die('spack env status requires an active env or argument')
    environment = ev.read(args.env)
    _environment_concretize(
        environment, use_repo=bool(args.exact_env), force=args.force)


def _environment_concretize(environment, use_repo=False, force=False):
    """Function body separated out to aid in testing."""
    new_specs = environment.concretize(force=force)
    environment.write(dump_packages=new_specs)


# REMOVE
# env install
#
def env_install_setup_parser(subparser):
    """install all concretized specs in an environment"""
    subparser.add_argument(
        'env', nargs='?', help='install all packages in this environment')
    spack.cmd.install.add_common_arguments(subparser)


def env_install(args):
    if not args.env:
        tty.die('spack env status requires an active env or argument')

    env = ev.read(args.env)
    env.install(args)


# REMOVE
# env uninstall
#
def env_uninstall_setup_parser(subparser):
    """uninstall packages from an environment"""
    subparser.add_argument(
        'env', nargs='?', help='uninstall all packages in this environment')
    spack.cmd.uninstall.add_common_arguments(subparser)


def env_uninstall(args):
    if not args.env:
        tty.die('spack env uninstall requires an active env or argument')

    environment = ev.read(args.env)
    environment.uninstall(args)


#
# env relocate
#
def env_relocate_setup_parser(subparser):
    """reconcretize environment with new OS and/or compiler"""
    subparser.add_argument('--compiler', help="Compiler spec to use")


def env_relocate(args):
    environment = ev.read(args.env)
    environment.reset_os_and_compiler(compiler=args.compiler)
    environment.write()


#
# env status
#
def env_status_setup_parser(subparser):
    """get install status of specs in an environment"""
    subparser.add_argument(
        'env', nargs='?', help='name of environment to show status for')
    arguments.add_common_arguments(
        subparser,
        ['recurse_dependencies', 'long', 'very_long', 'install_status'])


def env_status(args):
    if not args.env:
        tty.die('spack env status requires an active env or argument')

    # TODO? option to show packages w/ multiple instances?
    environment = ev.read(args.env)
    environment.status(
        sys.stdout, recurse_dependencies=args.recurse_dependencies,
        hashes=args.long or args.very_long,
        hashlen=None if args.very_long else 7,
        install_status=args.install_status)


#
# env stage
#
def env_stage_setup_parser(subparser):
    """download all source files for all packages in an environment"""
    subparser.add_argument(
        'env', nargs='?', help='name of env to generate loads file for')


def env_stage(args):
    if not args.env:
        tty.die('spack env loads requires an active env or argument')

    environment = ev.read(args.env)
    for spec in environment.specs_by_hash.values():
        for dep in spec.traverse():
            dep.package.do_stage()


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
    if not args.env:
        tty.die('spack env loads requires an active env or argument')

    # Set the module types that have been selected
    module_type = args.module_type
    if module_type is None:
        # If no selection has been made select all of them
        module_type = 'tcl'

    environment = ev.read(args.env)
    recurse_dependencies = args.recurse_dependencies
    args.recurse_dependencies = False

    loads_file = fs.join_path(environment.path, 'loads')
    with open(loads_file, 'w') as f:
        specs = environment._get_environment_specs(
            recurse_dependencies=recurse_dependencies)

        spack.cmd.modules.loads(module_type, specs, args, f)

    print('To load this environment, type:')
    print('   source %s' % loads_file)


#
# env upgrade
#
def env_upgrade_setup_parser(subparser):
    """upgrade a dependency package in an environment to the latest version"""
    subparser.add_argument('dep_name', help='Dependency package to upgrade')
    subparser.add_argument('--dry-run', action='store_true', dest='dry_run',
                           help="Just show the updates that would take place")


def env_upgrade(args):
    env = ev.read(args.env)

    if os.path.exists(env.repos_path):
        repo_stage = tempfile.mkdtemp()
        new_repos_path = os.path.join_path(repo_stage, 'repos')
        shutil.copytree(env.repos_path, new_repos_path)

        repo = spack.environment.make_repo_path(new_repos_path)
        if args.dep_name in repo:
            shutil.rmtree(repo.dirname_for_package_name(args.dep_name))
        spack.repo.path.put_first(repo)

    new_dep = env.upgrade_dependency(args.dep_name, args.dry_run)
    if not args.dry_run and new_dep:
        env.write(new_dep)


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


def env(parser, args, **kwargs):
    """Look for a function called environment_<name> and call it."""
    action = subcommand_functions[args.env_command]
    action(args)
