# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shlex
import shutil
import sys
import tempfile
from pathlib import Path
from typing import List, Optional

import llnl.string as string
import llnl.util.filesystem as fs
import llnl.util.tty as tty
from llnl.util.tty.colify import colify
from llnl.util.tty.color import cescape, colorize

import spack.cmd
import spack.cmd.common
import spack.cmd.common.arguments
import spack.cmd.modules
import spack.config
import spack.environment as ev
import spack.environment.depfile as depfile
import spack.environment.environment
import spack.environment.shell
import spack.tengine
from spack.cmd.common import arguments
from spack.util.environment import EnvironmentModifications

description = "manage virtual environments"
section = "environments"
level = "short"


#: List of subcommands of `spack env`
subcommands = [
    "activate",
    "deactivate",
    "create",
    ["remove", "rm"],
    ["rename", "mv"],
    ["list", "ls"],
    ["status", "st"],
    "loads",
    "view",
    "update",
    "revert",
    "depfile",
]


#
# env create
#
def env_create_setup_parser(subparser):
    """create a new environment"""
    subparser.add_argument("env_name", metavar="env", help="name or directory of environment")
    subparser.add_argument(
        "-d", "--dir", action="store_true", help="create an environment in a specific directory"
    )
    subparser.add_argument(
        "--keep-relative",
        action="store_true",
        help="copy relative develop paths verbatim into the new environment"
        " when initializing from envfile",
    )
    view_opts = subparser.add_mutually_exclusive_group()
    view_opts.add_argument(
        "--without-view", action="store_true", help="do not maintain a view for this environment"
    )
    view_opts.add_argument(
        "--with-view",
        help="specify that this environment should maintain a view at the"
        " specified path (by default the view is maintained in the"
        " environment directory)",
    )
    subparser.add_argument(
        "envfile",
        nargs="?",
        default=None,
        help="either a lockfile (must end with '.json' or '.lock') or a manifest file",
    )
    subparser.add_argument(
        "--include-concrete", action="append", help="name of old environment to copy specs from"
    )


def env_create(args):
    if args.with_view:
        # Expand relative paths provided on the command line to the current working directory
        # This way we interpret `spack env create --with-view ./view --dir ./env` as
        # a view in $PWD/view, not $PWD/env/view. This is different from specifying a relative
        # path in the manifest, which is resolved relative to the manifest file's location.
        with_view = os.path.abspath(args.with_view)
    elif args.without_view:
        with_view = False
    else:
        # Note that 'None' means unspecified, in which case the Environment
        # object could choose to enable a view by default. False means that
        # the environment should not include a view.
        with_view = None

    include_concrete = None
    if hasattr(args, "include_concrete"):
        include_concrete = args.include_concrete

    env = _env_create(
        args.env_name,
        init_file=args.envfile,
        dir=args.dir or os.path.sep in args.env_name or args.env_name in (".", ".."),
        with_view=with_view,
        keep_relative=args.keep_relative,
        include_concrete=include_concrete,
    )

    # Generate views, only really useful for environments created from spack.lock files.
    env.regenerate_views()


def _env_create(
    name_or_path: str,
    *,
    init_file: Optional[str] = None,
    dir: bool = False,
    with_view: Optional[str] = None,
    keep_relative: bool = False,
    include_concrete: Optional[List[str]] = None,
):
    """Create a new environment, with an optional yaml description.

    Arguments:
        name_or_path (str): name of the environment to create, or path to it
        init_file (str or file): optional initialization file -- can be
            a JSON lockfile (*.lock, *.json) or YAML manifest file
        dir (bool): if True, create an environment in a directory instead
            of a named environment
        keep_relative (bool): if True, develop paths are copied verbatim into
            the new environment file, otherwise they may be made absolute if the
            new environment is in a different location
        include_concrete (list): list of the included concrete environments
    """
    if not dir:
        env = ev.create(
            name_or_path,
            init_file=init_file,
            with_view=with_view,
            keep_relative=keep_relative,
            include_concrete=include_concrete,
        )
        tty.msg(
            colorize(
                f"Created environment @c{{{cescape(name_or_path)}}} in: @c{{{cescape(env.path)}}}"
            )
        )
    else:
        env = ev.create_in_dir(
            name_or_path,
            init_file=init_file,
            with_view=with_view,
            keep_relative=keep_relative,
            include_concrete=include_concrete,
        )
        tty.msg(colorize(f"Created independent environment in: @c{{{cescape(env.path)}}}"))
    tty.msg(f"Activate with: {colorize(f'@c{{spack env activate {cescape(name_or_path)}}}')}")
    return env


#
# env activate
#
def env_activate_setup_parser(subparser):
    """set the current environment"""
    shells = subparser.add_mutually_exclusive_group()
    shells.add_argument(
        "--sh",
        action="store_const",
        dest="shell",
        const="sh",
        help="print sh commands to activate the environment",
    )
    shells.add_argument(
        "--csh",
        action="store_const",
        dest="shell",
        const="csh",
        help="print csh commands to activate the environment",
    )
    shells.add_argument(
        "--fish",
        action="store_const",
        dest="shell",
        const="fish",
        help="print fish commands to activate the environment",
    )
    shells.add_argument(
        "--bat",
        action="store_const",
        dest="shell",
        const="bat",
        help="print bat commands to activate the environment",
    )
    shells.add_argument(
        "--pwsh",
        action="store_const",
        dest="shell",
        const="pwsh",
        help="print powershell commands to activate environment",
    )

    view_options = subparser.add_mutually_exclusive_group()
    view_options.add_argument(
        "--with-view",
        "-v",
        metavar="name",
        help="set runtime environment variables for specific view",
    )
    view_options.add_argument(
        "--without-view",
        "-V",
        action="store_true",
        help="do not set runtime environment variables for any view",
    )

    subparser.add_argument(
        "-p",
        "--prompt",
        action="store_true",
        default=False,
        help="decorate the command line prompt when activating",
    )

    subparser.add_argument(
        "--temp",
        action="store_true",
        default=False,
        help="create and activate an environment in a temporary directory",
    )
    subparser.add_argument(
        "--create",
        action="store_true",
        default=False,
        help="create and activate the environment if it doesn't exist",
    )
    subparser.add_argument(
        "--envfile",
        nargs="?",
        default=None,
        help="either a lockfile (must end with '.json' or '.lock') or a manifest file",
    )
    subparser.add_argument(
        "--keep-relative",
        action="store_true",
        help="copy relative develop paths verbatim into the new environment"
        " when initializing from envfile",
    )
    subparser.add_argument(
        "-d",
        "--dir",
        default=False,
        action="store_true",
        help="activate environment based on the directory supplied",
    )
    subparser.add_argument(
        metavar="env",
        dest="env_name",
        nargs="?",
        default=None,
        help=(
            "name of managed environment or directory of the independent env"
            " (when using --dir/-d) to activate"
        ),
    )


def create_temp_env_directory():
    """
    Returns the path of a temporary directory in which to
    create an environment
    """
    return tempfile.mkdtemp(prefix="spack-")


def _tty_info(msg):
    """tty.info like function that prints the equivalent printf statement for eval."""
    decorated = f'{colorize("@*b{==>}")} {msg}\n'
    executor = "echo" if sys.platform == "win32" else "printf"
    print(f"{executor} {shlex.quote(decorated)};")


def env_activate(args):
    if not args.shell:
        spack.cmd.common.shell_init_instructions(
            "spack env activate", "    eval `spack env activate {sh_arg} [...]`"
        )
        return 1

    # Error out when -e, -E, -D flags are given, cause they are ambiguous.
    if args.env or args.no_env or args.env_dir:
        tty.die("Calling spack env activate with --env, --env-dir and --no-env is ambiguous")

    # special parser error handling relative to the --temp flag
    temp_conflicts = iter([args.keep_relative, args.dir, args.env_name, args.with_view])
    if args.temp and any(temp_conflicts):
        tty.die(
            "spack env activate --temp cannot be combined with managed environments, --with-view,"
            " --keep-relative, or --dir."
        )

    # When executing `spack env activate` without further arguments, activate
    # the default environment. It's created when it doesn't exist yet.
    if not args.env_name and not args.temp:
        short_name = "default"
        if not ev.exists(short_name):
            ev.create(short_name)
            action = "Created and activated"
        else:
            action = "Activated"
        env_path = ev.root(short_name)
        _tty_info(f"{action} default environment in {env_path}")

    # Temporary environment
    elif args.temp:
        env = create_temp_env_directory()
        env_path = os.path.abspath(env)
        short_name = os.path.basename(env_path)
        ev.create_in_dir(env).write(regenerate=False)
        _tty_info(f"Created and activated temporary environment in {env_path}")

    # Managed environment
    elif ev.exists(args.env_name) and not args.dir:
        env_path = ev.root(args.env_name)
        short_name = args.env_name

    # Environment directory
    elif ev.is_env_dir(args.env_name):
        env_path = os.path.abspath(args.env_name)
        short_name = os.path.basename(env_path)

    # create if user requested, and then recall recursively
    elif args.create:
        tty.set_msg_enabled(False)
        env_create(args)
        tty.set_msg_enabled(True)
        env_activate(args)
        return

    else:
        tty.die("No such environment: '%s'" % args.env_name)

    env_prompt = "[%s]" % short_name

    # We only support one active environment at a time, so deactivate the current one.
    if ev.active_environment() is None:
        cmds = ""
        env_mods = EnvironmentModifications()
    else:
        cmds = spack.environment.shell.deactivate_header(shell=args.shell)
        env_mods = spack.environment.shell.deactivate()

    # Activate new environment
    active_env = ev.Environment(env_path)

    # Check if runtime environment variables are requested, and if so, for what view.
    view: Optional[str] = None
    if args.with_view:
        view = args.with_view
        if not active_env.has_view(view):
            tty.die(f"The environment does not have a view named '{view}'")
    elif not args.without_view and active_env.has_view(ev.default_view_name):
        view = ev.default_view_name

    cmds += spack.environment.shell.activate_header(
        env=active_env, shell=args.shell, prompt=env_prompt if args.prompt else None, view=view
    )
    env_mods.extend(spack.environment.shell.activate(env=active_env, view=view))
    cmds += env_mods.shell_modifications(args.shell)
    sys.stdout.write(cmds)


#
# env deactivate
#
def env_deactivate_setup_parser(subparser):
    """deactivate any active environment in the shell"""
    shells = subparser.add_mutually_exclusive_group()
    shells.add_argument(
        "--sh",
        action="store_const",
        dest="shell",
        const="sh",
        help="print sh commands to deactivate the environment",
    )
    shells.add_argument(
        "--csh",
        action="store_const",
        dest="shell",
        const="csh",
        help="print csh commands to deactivate the environment",
    )
    shells.add_argument(
        "--fish",
        action="store_const",
        dest="shell",
        const="fish",
        help="print fish commands to activate the environment",
    )
    shells.add_argument(
        "--bat",
        action="store_const",
        dest="shell",
        const="bat",
        help="print bat commands to activate the environment",
    )
    shells.add_argument(
        "--pwsh",
        action="store_const",
        dest="shell",
        const="pwsh",
        help="print pwsh commands to activate the environment",
    )


def env_deactivate(args):
    if not args.shell:
        spack.cmd.common.shell_init_instructions(
            "spack env deactivate", "    eval `spack env deactivate {sh_arg}`"
        )
        return 1

    # Error out when -e, -E, -D flags are given, cause they are ambiguous.
    if args.env or args.no_env or args.env_dir:
        tty.die("Calling spack env deactivate with --env, --env-dir and --no-env is ambiguous")

    if ev.active_environment() is None:
        tty.die("No environment is currently active.")

    cmds = spack.environment.shell.deactivate_header(args.shell)
    env_mods = spack.environment.shell.deactivate()
    cmds += env_mods.shell_modifications(args.shell)
    sys.stdout.write(cmds)


#
# env remove
#
def env_remove_setup_parser(subparser):
    """remove an existing environment"""
    subparser.add_argument("rm_env", metavar="env", nargs="+", help="environment(s) to remove")
    arguments.add_common_arguments(subparser, ["yes_to_all"])
    subparser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="remove the environment even if it is included in another environment",
    )


def env_remove(args):
    """Remove a *named* environment.

    This removes an environment managed by Spack. Directory environments
    and manifests embedded in repositories should be removed manually.
    """
    remove_envs = []
    valid_envs = []
    bad_envs = []

    for env_name in ev.all_environment_names():
        try:
            env = ev.read(env_name)
            valid_envs.append(env)

            if env_name in args.rm_env:
                remove_envs.append(env)
        except (spack.config.ConfigFormatError, ev.SpackEnvironmentConfigError):
            if env_name in args.rm_env:
                bad_envs.append(env_name)

    # Check if remove_env is included from another env before trying to remove
    for env in valid_envs:
        for remove_env in remove_envs:
            # don't check if environment is included to itself
            if env.name == remove_env.name:
                continue

            if remove_env.path in env.included_concrete_envs:
                msg = f'Environment "{remove_env.name}" is being used by environment "{env.name}"'
                if args.force:
                    tty.warn(msg)
                else:
                    tty.die(msg)

    if not args.yes_to_all:
        environments = string.plural(len(args.rm_env), "environment", show_n=False)
        envs = string.comma_and(args.rm_env)
        answer = tty.get_yes_or_no(f"Really remove {environments} {envs}?", default=False)
        if not answer:
            tty.die("Will not remove any environments")

    for env in remove_envs:
        name = env.name
        if env.active:
            tty.die(f"Environment {name} can't be removed while activated.")
        env.destroy()
        tty.msg(f"Successfully removed environment '{name}'")

    for bad_env_name in bad_envs:
        shutil.rmtree(
            spack.environment.environment.environment_dir_from_name(bad_env_name, exists_ok=True)
        )
        tty.msg(f"Successfully removed environment '{bad_env_name}'")


#
# env rename
#
def env_rename_setup_parser(subparser):
    """rename an existing environment"""
    subparser.add_argument(
        "mv_from", metavar="from", help="name (or path) of existing environment"
    )
    subparser.add_argument(
        "mv_to", metavar="to", help="new name (or path) for existing environment"
    )
    subparser.add_argument(
        "-d",
        "--dir",
        action="store_true",
        help="the specified arguments correspond to directory paths",
    )
    subparser.add_argument(
        "-f", "--force", action="store_true", help="allow overwriting of an existing environment"
    )


def env_rename(args):
    """Rename an environment.

    This renames a managed environment or moves an independent environment.
    """

    # Directory option has been specified
    if args.dir:
        if not ev.is_env_dir(args.mv_from):
            tty.die("The specified path does not correspond to a valid spack environment")
        from_path = Path(args.mv_from)
        if not args.force:
            if ev.is_env_dir(args.mv_to):
                tty.die(
                    "The new path corresponds to an existing environment;"
                    " specify the --force flag to overwrite it."
                )
            if Path(args.mv_to).exists():
                tty.die("The new path already exists; specify the --force flag to overwrite it.")
        to_path = Path(args.mv_to)

    # Name option being used
    elif ev.exists(args.mv_from):
        from_path = ev.environment.environment_dir_from_name(args.mv_from)
        if not args.force and ev.exists(args.mv_to):
            tty.die(
                "The new name corresponds to an existing environment;"
                " specify the --force flag to overwrite it."
            )
        to_path = ev.environment.root(args.mv_to)

    # Neither
    else:
        tty.die("The specified name does not correspond to a managed spack environment")

    # Guard against renaming from or to an active environment
    active_env = ev.active_environment()
    if active_env:
        from_env = ev.Environment(from_path)
        if from_env.path == active_env.path:
            tty.die("Cannot rename active environment")
        if to_path == active_env.path:
            tty.die(f"{args.mv_to} is an active environment")

    shutil.rmtree(to_path, ignore_errors=True)
    fs.rename(from_path, to_path)
    tty.msg(f"Successfully renamed environment {args.mv_from} to {args.mv_to}")


#
# env list
#
def env_list_setup_parser(subparser):
    """list managed environments"""


def env_list(args):
    names = ev.all_environment_names()

    color_names = []
    for name in names:
        if ev.active(name):
            name = colorize("@*g{%s}" % name)
        color_names.append(name)

    # say how many there are if writing to a tty
    if sys.stdout.isatty():
        if not names:
            tty.msg("No environments")
        else:
            tty.msg("%d environments" % len(names))

    colify(color_names, indent=4)


class ViewAction:
    regenerate = "regenerate"
    enable = "enable"
    disable = "disable"

    @staticmethod
    def actions():
        return [ViewAction.regenerate, ViewAction.enable, ViewAction.disable]


#
# env view
#
def env_view_setup_parser(subparser):
    """manage a view associated with the environment"""
    subparser.add_argument(
        "action", choices=ViewAction.actions(), help="action to take for the environment's view"
    )
    subparser.add_argument(
        "view_path", nargs="?", help="when enabling a view, optionally set the path manually"
    )


def env_view(args):
    env = ev.active_environment()

    if not env:
        tty.msg("No active environment")
        return

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
        env.update_default_view(path_or_bool=False)
        env.write()


#
# env status
#
def env_status_setup_parser(subparser):
    """print whether there is an active environment"""


def env_status(args):
    env = ev.active_environment()
    if env:
        if env.path == os.getcwd():
            tty.msg("Using %s in current directory: %s" % (ev.manifest_name, env.path))
        else:
            tty.msg("In environment %s" % env.name)

        # Check if environment views can be safely activated
        env.check_views()
    else:
        tty.msg("No active environment")


#
# env loads
#
def env_loads_setup_parser(subparser):
    """list modules for an installed environment '(see spack module loads)'"""
    subparser.add_argument(
        "-n",
        "--module-set-name",
        default="default",
        help="module set for which to generate load operations",
    )
    subparser.add_argument(
        "-m",
        "--module-type",
        choices=("tcl", "lmod"),
        help="type of module system to generate loads for",
    )
    spack.cmd.modules.add_loads_arguments(subparser)


def env_loads(args):
    env = spack.cmd.require_active_env(cmd_name="env loads")

    # Set the module types that have been selected
    module_type = args.module_type
    if module_type is None:
        # If no selection has been made select all of them
        module_type = "tcl"

    recurse_dependencies = args.recurse_dependencies
    args.recurse_dependencies = False

    loads_file = fs.join_path(env.path, "loads")
    with open(loads_file, "w") as f:
        specs = env._get_environment_specs(recurse_dependencies=recurse_dependencies)

        spack.cmd.modules.loads(module_type, specs, args, f)

    print("To load this environment, type:")
    print("   source %s" % loads_file)


def env_update_setup_parser(subparser):
    """update environments to the latest format"""
    subparser.add_argument(
        metavar="env", dest="update_env", help="name or directory of the environment to activate"
    )
    spack.cmd.common.arguments.add_common_arguments(subparser, ["yes_to_all"])


def env_update(args):
    manifest_file = ev.manifest_file(args.update_env)
    backup_file = manifest_file + ".bkp"

    needs_update = not ev.is_latest_format(manifest_file)
    if not needs_update:
        tty.msg('No update needed for the environment "{0}"'.format(args.update_env))
        return

    proceed = True
    if not args.yes_to_all:
        msg = (
            'The environment "{0}" is going to be updated to the latest '
            "schema format.\nIf the environment is updated, versions of "
            "Spack that are older than this version may not be able to "
            "read it. Spack stores backups of the updated environment "
            'which can be retrieved with "spack env revert"'
        )
        tty.msg(msg.format(args.update_env))
        proceed = tty.get_yes_or_no("Do you want to proceed?", default=False)

    if not proceed:
        tty.die("Operation aborted.")

    ev.update_yaml(manifest_file, backup_file=backup_file)
    msg = 'Environment "{0}" has been updated [backup={1}]'
    tty.msg(msg.format(args.update_env, backup_file))


def env_revert_setup_parser(subparser):
    """restore environments to their state before update"""
    subparser.add_argument(
        metavar="env", dest="revert_env", help="name or directory of the environment to activate"
    )
    spack.cmd.common.arguments.add_common_arguments(subparser, ["yes_to_all"])


def env_revert(args):
    manifest_file = ev.manifest_file(args.revert_env)
    backup_file = manifest_file + ".bkp"

    # Check that both the spack.yaml and the backup exist, the inform user
    # on what is going to happen and ask for confirmation
    if not os.path.exists(manifest_file):
        msg = "cannot find the manifest file of the environment [file={0}]"
        tty.die(msg.format(manifest_file))
    if not os.path.exists(backup_file):
        msg = "cannot find the old manifest file to be restored [file={0}]"
        tty.die(msg.format(backup_file))

    proceed = True
    if not args.yes_to_all:
        msg = (
            "Spack is going to overwrite the current manifest file"
            " with a backup copy [manifest={0}, backup={1}]"
        )
        tty.msg(msg.format(manifest_file, backup_file))
        proceed = tty.get_yes_or_no("Do you want to proceed?", default=False)

    if not proceed:
        tty.die("Operation aborted.")

    shutil.copy(backup_file, manifest_file)
    os.remove(backup_file)
    msg = 'Environment "{0}" reverted to old state'
    tty.msg(msg.format(manifest_file))


def env_depfile_setup_parser(subparser):
    """generate a depfile from the concrete environment specs"""
    subparser.add_argument(
        "--make-prefix",
        "--make-target-prefix",
        default=None,
        metavar="TARGET",
        help="prefix Makefile targets (and variables) with <TARGET>/<name>\n\nby default "
        "the absolute path to the directory makedeps under the environment metadata dir is "
        "used. can be set to an empty string --make-prefix ''",
    )
    subparser.add_argument(
        "--make-disable-jobserver",
        default=True,
        action="store_false",
        dest="jobserver",
        help="disable POSIX jobserver support",
    )
    subparser.add_argument(
        "--use-buildcache",
        dest="use_buildcache",
        type=arguments.use_buildcache,
        default="package:auto,dependencies:auto",
        metavar="[{auto,only,never},][package:{auto,only,never},][dependencies:{auto,only,never}]",
        help="when using `only`, redundant build dependencies are pruned from the DAG\n\n"
        "this flag is passed on to the generated spack install commands",
    )
    subparser.add_argument(
        "-o",
        "--output",
        default=None,
        metavar="FILE",
        help="write the depfile to FILE rather than to stdout",
    )
    subparser.add_argument(
        "-G",
        "--generator",
        default="make",
        choices=("make",),
        help="specify the depfile type\n\ncurrently only make is supported",
    )
    subparser.add_argument(
        metavar="specs",
        dest="specs",
        nargs=argparse.REMAINDER,
        default=None,
        help="generate a depfile only for matching specs in the environment",
    )


def env_depfile(args):
    # Currently only make is supported.
    spack.cmd.require_active_env(cmd_name="env depfile")

    env = ev.active_environment()

    # What things do we build when running make? By default, we build the
    # root specs. If specific specs are provided as input, we build those.
    filter_specs = spack.cmd.parse_specs(args.specs) if args.specs else None
    template = spack.tengine.make_environment().get_template(os.path.join("depfile", "Makefile"))
    model = depfile.MakefileModel.from_env(
        env,
        filter_specs=filter_specs,
        pkg_buildcache=depfile.UseBuildCache.from_string(args.use_buildcache[0]),
        dep_buildcache=depfile.UseBuildCache.from_string(args.use_buildcache[1]),
        make_prefix=args.make_prefix,
        jobserver=args.jobserver,
    )

    # Warn in case we're generating a depfile for an empty environment. We don't automatically
    # concretize; the user should do that explicitly. Could be changed in the future if requested.
    if model.empty:
        if not env.user_specs:
            tty.warn("no specs in the environment")
        elif filter_specs is not None:
            tty.warn("no concrete matching specs found in environment")
        else:
            tty.warn("environment is not concretized. Run `spack concretize` first")

    makefile = template.render(model.to_dict())

    # Finally write to stdout/file.
    if args.output:
        with open(args.output, "w") as f:
            f.write(makefile)
    else:
        sys.stdout.write(makefile)


#: Dictionary mapping subcommand names and aliases to functions
subcommand_functions = {}


#
# spack env
#
def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="env_command")

    for name in subcommands:
        if isinstance(name, (list, tuple)):
            name, aliases = name[0], name[1:]
        else:
            aliases = []

        # add commands to subcommands dict
        function_name = "env_%s" % name
        function = globals()[function_name]
        for alias in [name] + aliases:
            subcommand_functions[alias] = function

        # make a subparser and run the command's setup function on it
        setup_parser_cmd_name = "env_%s_setup_parser" % name
        setup_parser_cmd = globals()[setup_parser_cmd_name]

        subsubparser = sp.add_parser(name, aliases=aliases, help=setup_parser_cmd.__doc__)
        setup_parser_cmd(subsubparser)


def env(parser, args):
    """Look for a function called environment_<name> and call it."""
    action = subcommand_functions[args.env_command]
    action(args)
