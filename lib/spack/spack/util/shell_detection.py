# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform
import subprocess

from spack.error import SpackError


def active_shell_type(env=os.environ):
    if platform.system() == "Windows":
        if "POWERSHELL" in env:
            return "ps1"
        else:
            try:
                output = subprocess.check_output(
                    'powershell -Command "echo $PSVersionTable"', universal_newlines=True
                )
                if "PSVersion" in output:
                    return "ps1"
                else:
                    pass
            except subprocess.CalledProcessError:
                pass
            raise SpackError("Unknown shell type being used on Windows")
    else:
        shell = env.get("SHELL", None)
        if shell:
            return shell
        else:
            # assume it is a bourne shell
            return "sh"
