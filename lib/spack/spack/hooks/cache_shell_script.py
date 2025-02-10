# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

import spack.user_environment as uenv


def path_to_load_shell_script(spec, shell):
    """Returns to path to the shell script to load the specified spec for the shell that
    the user is running

    Args:
        spec: The spec whose shell script we are returning the path of
        shell: The shell that the user is running on
    """

    return os.path.join(spec.prefix, ".spack", f"load.{shell}")


def path_to_unload_shell_script(spec, shell):
    """Returns to path to the shell script to unload the specified spec for the shell that
    the user is running

    Args:
        spec: The spec whose shell script we are returning the path of
        shell: The shell that the user is running
    """

    return os.path.join(spec.prefix, ".spack", f"unload.{shell}")


def post_install(spec, explicit=None):
    """Creates and writes a cached shell script in for all available shells

    Args:
        spec: The spec the requires the shell scripts
        explicit: TODO: because I have no idea
    """

    if spec.external:
        return

    shells_avail = ["sh", "csh", "fish"]

    if sys.platform == "win32":
        shells_avail.extend(["bat", "pwsh"])

    # Load TODO: Write better comment
    env_mods = uenv.environment_modifications_for_specs(spec)

    for shell in shells_avail:
        mods = env_mods.shell_modifications(shell)

        shell_script_path = path_to_load_shell_script(spec, shell)

        with open(shell_script_path, "w") as f:
            f.write(mods)

    # Unload TODO: Write better comment
    env_mods = uenv.environment_modifications_for_specs(spec).reversed()

    for shell in shells_avail:
        mods = env_mods.shell_modifications(shell)

        shell_script_path = path_to_unload_shell_script(spec, shell)

        with open(shell_script_path, "w") as f:
            f.write(mods)
