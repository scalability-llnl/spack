# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.user_environment as uenv


def post_install(spec, explicit=None):
    """What this does
    
    Args:
        spec:
        explicit:
    """
    shell = os.environ.get("SPACK_SHELL")
    env_mods = uenv.environment_modifications_for_specs(spec)
    mods = env_mods.shell_modifications(shell)

    shell_script_path = os.path.join(spec.prefix, ".spack", f"{spec.name}_shell.{shell}")

    with open(shell_script_path, "w") as f:
        f.write(mods)
