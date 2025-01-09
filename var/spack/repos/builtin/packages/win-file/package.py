# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re
import shutil

from spack.package import *


class WinFile(Package):
    """File "file type guesser" system utility cross compiled for x86_64 Windows
    systems via the Mingw-w64 cross compiler and a custom Spack repository
    """

    homepage = "https://spack.github.io/windows-bootstrap-resources"
    url = (
        "https://spack.github.io/windows-bootstrap-resources/resources/file/5.45/file_5.45.tar.gz"
    )

    executables = ["^file$"]

    version("5.45", sha256="11b8f3abf647c711bc50ef8451c8d6e955f11c4afd8b0a98f2ac65e9b6e10d5e")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"file-(\S+)", output)
        return match.group(1) if match else None

    def install(self, spec, prefix):
        mkdirp(prefix)
        for subdir in os.listdir(self.stage.source_path):
            shutil.move(subdir, prefix)
