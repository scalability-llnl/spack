# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Rsync(AutotoolsPackage):
    """An open source utility that provides fast incremental file transfer."""

    homepage = "https://rsync.samba.org"
    url = "https://download.samba.org/pub/rsync/src/rsync-3.2.4.tar.gz"

    license("GPL-3.0-or-later")

    version("3.3.0", sha256="7399e9a6708c32d678a72a63219e96f23be0be2336e50fd1348498d07041df90")
    version("3.2.7", sha256="4e7d9d3f6ed10878c58c5fb724a67dacf4b6aac7340b13e488fb2dc41346f2bb")
    version("3.2.6", sha256="fb3365bab27837d41feaf42e967c57bd3a47bc8f10765a3671efd6a3835454d3")
    version("3.2.5", sha256="2ac4d21635cdf791867bc377c35ca6dda7f50d919a58be45057fd51600c69aba")
    version("3.2.4", sha256="6f761838d08052b0b6579cf7f6737d93e47f01f4da04c5d24d3447b7f2a5fad1")
    version("3.2.3", sha256="becc3c504ceea499f4167a260040ccf4d9f2ef9499ad5683c179a697146ce50e")
    version("3.2.2", sha256="644bd3841779507665211fd7db8359c8a10670c57e305b4aab61b4e40037afa8")
    version("3.1.3", sha256="55cc554efec5fdaad70de921cd5a5eeb6c29a95524c715f3bbf849235b0800c0")
    version("3.1.2", sha256="ecfa62a7fa3c4c18b9eccd8c16eaddee4bd308a76ea50b5c02a5840f09c0a1c2")
    version("3.1.1", sha256="7de4364fcf5fe42f3bdb514417f1c40d10bbca896abe7e7f2c581c6ea08a2621")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")
    depends_on("popt")
    depends_on("openssl", when="@3.2:")
    depends_on("xxhash", when="@3.2:")
    depends_on("zstd", when="@3.2:")
    depends_on("lz4", when="@3.2:")

    conflicts("%nvhpc")

    executables = ["^rsync$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"rsync\s+version\s+(\S+)", output)
        return match.group(1) if match else None

    def configure_args(self):
        return ["--with-included-zlib=no"]
