# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shlex
import shutil
import sys
import tempfile
from pathlib import Path
from typing import List, Optional, Set

import llnl.string as string
import llnl.util.filesystem as fs
import llnl.util.tty as tty
from llnl.util.symlink import islink, symlink
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
    "track",
    "untrack",
]


#
# env create
#
def env_create_setup_parser(subparser):
    """create a new environment

    create a new environment or, optionally, copy an existing environment

    a manifest file results in a new abstract environment while a lock file
    creates a new concrete environment
    """
    subparser.add_argument(
        "env_name", metavar="env", help="name or directory of the new environment"
    )
    subparser.add_argument(
        "-d", "--dir", action="store_true", help="create an environment in a specific directory"
    )
    subparser.add_argument(
        "--keep-relative",
        action="store_true",
        help="copy envfile's relative develop paths verbatim",
    )
    view_opts = subparser.add_mutually_exclusive_group()
    view_opts.add_argument(
        "--without-view", action="store_true", help="do not maintain a view for this environment"
    )
    view_opts.add_argument(
        "--with-view", help="maintain view at WITH_VIEW (vs. environment's directory)"
    )
    subparser.add_argument(
        "envfile",
        nargs="?",
        default=None,
        help="manifest or lock file (ends with '.json' or '.lock')",
    )
    subparser.add_argument(
        "--include-concrete",
        action="append",
        help="copy concrete specs from INCLUDE_CONCRETE's environment",
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
    """set the active environment"""
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
        "-v",
        "--with-view",
        metavar="name",
        help="set runtime environment variables for the named view",
    )
    view_options.add_argument(
        "-V",
        "--without-view",
        action="store_true",
        help="do not set runtime environment variables for any view",
    )

    subparser.add_argument(
        "-p",
        "--prompt",
        action="store_true",
        default=False,
        help="add the active environment to the command line prompt",
    )

    subparser.add_argument(
        "--temp",
        action="store_true",
        default=False,
        help="create and activate in a temporary directory",
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
        help="manifest or lock file (ends with '.json' or '.lock')",
    )
    subparser.add_argument(
        "--keep-relative",
        action="store_true",
        help="copy envfile's relative develop paths verbatim when create",
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
        help=("name or directory of the environment being activated"),
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
    """deactivate the active environment"""
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
# env track
#
def env_track_setup_parser(subparser):
    """track an environment from a directory in Spack"""
    subparser.add_argument("-n", "--name", help="custom environment name")
    subparser.add_argument("dir", help="path to environment")
    arguments.add_common_arguments(subparser, ["yes_to_all"])


def env_track(args):
    src_path = os.path.abspath(args.dir)
    if not ev.is_env_dir(src_path):
        tty.die("Cannot track environment. Path doesn't contain an environment")

    if args.name:
        name = args.name
    else:
        name = os.path.basename(src_path)

    try:
        dst_path = ev.environment_dir_from_name(name, exists_ok=False)
    except ev.SpackEnvironmentError:
        tty.die(
            f"An environment named {name} already exists. Set a name with:"
            "\n\n"
            f"        spack env track --name NAME {src_path}\n"
        )

    symlink(src_path, dst_path)

    tty.msg(f"Tracking environment in {src_path}")
    tty.msg(
        "You can now activate this environment with the following command:\n\n"
        f"        spack env activate {name}\n"
    )


#
# env remove & untrack helpers
#
def filter_managed_env_names(env_names: Set[str]) -> Set[str]:
    tracked_env_names = {e for e in env_names if islink(ev.environment_dir_from_name(e))}
    managed_env_names = env_names - set(tracked_env_names)

    num_managed_envs = len(managed_env_names)
    managed_envs_str = " ".join(managed_env_names)
    if num_managed_envs >= 2:
        tty.error(
            f"The following are not tracked environments. "
            "To remove them completely run,"
            "\n\n"
            f"        spack env rm {managed_envs_str}\n"
        )

    elif num_managed_envs > 0:
        tty.error(
            f"'{managed_envs_str}' is not a tracked env. "
            "To remove it completely run,"
            "\n\n"
            f"        spack env rm {managed_envs_str}\n"
        )

    return tracked_env_names


def get_valid_envs(env_names: Set[str]) -> Set[ev.Environment]:
    valid_envs = set()
    for env_name in env_names:
        try:
            env = ev.read(env_name)
            valid_envs.add(env)

        except (spack.config.ConfigFormatError, ev.SpackEnvironmentConfigError):
            pass

    return valid_envs


def _env_untrack_or_remove(
    env_names: List[str], remove: bool = False, force: bool = False, yes_to_all: bool = False
):
    all_env_names = set(ev.all_environment_names())
    known_env_names = set(env_names).intersection(all_env_names)
    unknown_env_names = set(env_names) - known_env_names

    # print error for unknown environments
    for env_name in unknown_env_names:
        tty.error(f"Environment '{env_name}' does not exist")

    # if only unlinking is allowed, remove all environments
    # which do not point internally at symlinks
    if not remove:
        env_names_to_remove = filter_managed_env_names(known_env_names)
    else:
        env_names_to_remove = known_env_names

    # initalize all environments with valid spack.yaml configs
    all_valid_envs = get_valid_envs(all_env_names)

    # build a task list of environments and bad env names to remove
    envs_to_remove = [e for e in all_valid_envs if e.name in env_names_to_remove]
    bad_env_names_to_remove = env_names_to_remove - {e.name for e in envs_to_remove}
    for remove_env in envs_to_remove:
        for env in all_valid_envs:
            # don't check if an environment is included to itself
            if env.name == remove_env.name:
                continue

            # check if an environment is included un another
            if remove_env.path in env.included_concrete_envs:
                msg = f"Environment '{remove_env.name}' is used by environment '{env.name}'"
                if force:
                    tty.warn(msg)
                else:
                    tty.error(msg)
                    envs_to_remove.remove(remove_env)

    # ask the user if they really want to remove the known environments
    # force should do the same as yes to all here following the symantics of rm
    if not (yes_to_all or force) and (envs_to_remove or bad_env_names_to_remove):
        environments = string.plural(len(env_names_to_remove), "environment", show_n=False)
        envs = string.comma_and(list(env_names_to_remove))
        answer = tty.get_yes_or_no(
            f"Really {'remove' if remove else 'untrack'} {environments} {envs}?", default=False
        )
        if not answer:
            tty.die("Will not remove any environments")

    # keep track of the environments we remove for later printing the exit code
    removed_env_names = []
    for env in envs_to_remove:
        name = env.name
        if not force and env.active:
            tty.error(
                f"Environment '{name}' can't be "
                f"{'removed' if remove else 'untracked'} while activated."
            )
            continue
        # Get path to check if environment is a tracked / symlinked environment
        if islink(env.path):
            real_env_path = os.path.realpath(env.path)
            os.unlink(env.path)
            tty.msg(
                f"Sucessfully untracked environment '{name}', "
                "but it can still be found at:\n\n"
                f"        {real_env_path}\n"
            )
        else:
            env.destroy()
            tty.msg(f"Successfully removed environment '{name}'")

        removed_env_names.append(env.name)

    for bad_env_name in bad_env_names_to_remove:
        shutil.rmtree(
            spack.environment.environment.environment_dir_from_name(bad_env_name, exists_ok=True)
        )
        tty.msg(f"Successfully removed environment '{bad_env_name}'")
        removed_env_names.append(env.name)

    # Following the design of linux rm we should exit with a status of 1
    # anytime we cannot delete every environment the user asks for.
    # However, we should still process all the environments we know about
    # and delete them instead of failing on the first unknown enviornment.
    if len(removed_env_names) < len(known_env_names):
        sys.exit(1)


#
# env untrack
#
def env_untrack_setup_parser(subparser):
    """track an environment from a directory in Spack"""
    subparser.add_argument("env", nargs="+", help="tracked environment name")
    subparser.add_argument(
        "-f", "--force", action="store_true", help="force unlink even when environment is active"
    )
    arguments.add_common_arguments(subparser, ["yes_to_all"])


def env_untrack(args):
    _env_untrack_or_remove(
        env_names=args.env, force=args.force, yes_to_all=args.yes_to_all, remove=False
    )


#
# env remove
#
def env_remove_setup_parser(subparser):
    """remove managed environment(s)

    remove existing environment(s) managed by Spack

    directory environments and manifests embedded in repositories must be
    removed manually
    """
    subparser.add_argument(
        "rm_env", metavar="env", nargs="+", help="name(s) of the environment(s) being removed"
    )
    arguments.add_common_arguments(subparser, ["yes_to_all"])
    subparser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="force removal even when included in other environment(s)",
    )


def env_remove(args):
    """remove existing environment(s)"""
    _env_untrack_or_remove(
        env_names=args.rm_env, remove=True, force=args.force, yes_to_all=args.yes_to_all
    )


#
# env rename
#
def env_rename_setup_parser(subparser):
    """rename an existing environment

    rename a managed environment or move an independent/directory environment

    operation cannot be performed to or from an active environment
    """
    subparser.add_argument(
        "mv_from", metavar="from", help="current name or directory of the environment"
    )
    subparser.add_argument("mv_to", metavar="to", help="new name or directory for the environment")
    subparser.add_argument(
        "-d",
        "--dir",
        action="store_true",
        help="positional arguments are environment directory paths",
    )
    subparser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="force renaming even if overwriting an existing environment",
    )


def env_rename(args):
    """rename or move an existing environment"""

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
    """list all managed environments"""


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
    """manage the environment's view

    provide the path when enabling a view with a non-default path
    """
    subparser.add_argument(
        "action", choices=ViewAction.actions(), help="action to take for the environment's view"
    )
    subparser.add_argument("view_path", nargs="?", help="view's non-default path when enabling it")


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
    """print active environment status"""


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
    with open(loads_file, "w", encoding="utf-8") as f:
        specs = env._get_environment_specs(recurse_dependencies=recurse_dependencies)

        spack.cmd.modules.loads(module_type, specs, args, f)

    print("To load this environment, type:")
    print("   source %s" % loads_file)


def env_update_setup_parser(subparser):
    """update the environment manifest to the latest schema format

    update the environment to the latest schema format, which may not be
    readable by older versions of spack

    a backup copy of the manifest is retained in case there is a need to revert
    this operation
    """
    subparser.add_argument(
        metavar="env", dest="update_env", help="name or directory of the environment"
    )
    spack.cmd.common.arguments.add_common_arguments(subparser, ["yes_to_all"])


def env_update(args):
    """update the manifest to the latest format"""
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
    """restore the environment manifest to its previous format

    revert the environment's manifest to the schema format from its last
    'spack env update'

    the current manifest will be overwritten by the backup copy and the backup
    copy will be removed
    """
    subparser.add_argument(
        metavar="env", dest="revert_env", help="name or directory of the environment"
    )
    spack.cmd.common.arguments.add_common_arguments(subparser, ["yes_to_all"])


def env_revert(args):
    """restore the environment manifest to its previous format"""
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
    """generate a depfile to exploit parallel builds across specs

    requires the active environment to be concrete
    """
    subparser.add_argument(
        "--make-prefix",
        "--make-target-prefix",
        default=None,
        metavar="TARGET",
        help="prefix Makefile targets/variables with <TARGET>/<name>,\n"
        "which can be an empty string (--make-prefix '')\n"
        "defaults to the absolute path of the environment's makedeps\n"
        "environment metadata dir\n",
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
        help="use `only` to prune redundant build dependencies\n"
        "option is also passed to generated spack install commands",
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
        help="specify the depfile type (only supports `make`)",
    )
    subparser.add_argument(
        metavar="specs",
        dest="specs",
        nargs=argparse.REMAINDER,
        default=None,
        help="limit the generated file to matching specs",
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
        with open(args.output, "w", encoding="utf-8") as f:
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

        subsubparser = sp.add_parser(
            name,
            aliases=aliases,
            description=setup_parser_cmd.__doc__,
            help=spack.cmd.first_line(setup_parser_cmd.__doc__),
        )
        setup_parser_cmd(subsubparser)


def env(parser, args):
    """Look for a function called environment_<name> and call it."""
    action = subcommand_functions[args.env_command]
    action(args)
