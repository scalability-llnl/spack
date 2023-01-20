# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class File(AutotoolsPackage):
    """The file command is "a file type guesser", that is, a command-line
    tool that tells you in words what kind of data a file contains"""

    homepage = "https://www.darwinsys.com/file/"
    url = "https://astron.com/pub/file/file-5.37.tar.gz"

    maintainers = ["sethrj"]

    version("5.44", sha256="3751c7fba8dbc831cb8d7cc8aff21035459b8ce5155ef8b0880a27d028475f3b")
    version("5.43", sha256="8c8015e91ae0e8d0321d94c78239892ef9dbc70c4ade0008c0e95894abfb1991")
    version("5.42", sha256="c076fb4d029c74073f15c43361ef572cfb868407d347190ba834af3b1639b0e4")
    version("5.41", sha256="13e532c7b364f7d57e23dfeea3147103150cb90593a57af86c10e4f6e411603f")
    version("5.40", sha256="167321f43c148a553f68a0ea7f579821ef3b11c27b8cbe158e4df897e4a5dd57")
    version("5.39", sha256="f05d286a76d9556243d0cb05814929c2ecf3a5ba07963f8f70bfaaa70517fad1")
    version("5.38", sha256="593c2ffc2ab349c5aea0f55fedfe4d681737b6b62376a9b3ad1e77b2cc19fa34")
    version("5.37", sha256="e9c13967f7dd339a3c241b7710ba093560b9a33013491318e88e6b8b57bae07f")

    executables = ["^file$"]

    variant("static", default=True, description="Also build static libraries")

    depends_on("bzip2")
    depends_on("xz")
    depends_on("zlib")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"file-(\S+)", output)
        return match.group(1) if match else None

    def configure_args(self):
        args = [
            "--disable-dependency-tracking",
            "--enable-fsect-man5",
            "--enable-zlib",
            "--enable-bzlib",
            "--enable-xzlib",
        ]
        args += self.enable_or_disable("static")
        return args
