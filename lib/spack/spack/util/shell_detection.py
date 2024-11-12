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
                output = subprocess.run(
                    'powershell -Command "echo $PSVersionTable"', shell=True, check=True, text=True
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
            raise SpackError("No shell type detected for the Unix process")
