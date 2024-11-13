# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re

from spack.package import *


class Which(AutotoolsPackage):
    """GNU which - is a utility that is used to find which executable (or
    alias or shell function) is executed when entered on the shell prompt."""

    homepage = "https://savannah.gnu.org/projects/which/"
    url = "https://ftp.gnu.org/gnu/which/which-2.21.tar.gz"

    license("GPL-3.0")

    version("2.21", sha256="f4a245b94124b377d8b49646bf421f9155d36aa7614b6ebf83705d3ffc76eaad")

    depends_on("c", type="build")  # generated

    executables = ["which"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"GNU which v(\d+.\d+)", output)
        return match.group(1) if match else None
