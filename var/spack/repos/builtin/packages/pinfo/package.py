# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pinfo(AutotoolsPackage):
    """Pinfo is user-friendly, console-based viewer for Info documents."""

    homepage = "https://github.com/baszoetekouw/pinfo"
    url = "https://github.com/baszoetekouw/pinfo/archive/v0.6.13.tar.gz"

    version("0.6.13", sha256="9dc5e848a7a86cb665a885bc5f0fdf6d09ad60e814d75e78019ae3accb42c217")
    version("0.6.12", sha256="82af48ba23b8c26b1f4e67b45f718142eb0f760326b782f80c765801d3532077")
    version("0.6.11", sha256="fd26017ac9db179d709b49e450c3097e7d6f99cd94de7b5da824ec757c6992b2")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("gettext", type="build")
    depends_on("texinfo", type="build")

    def configure_args(self):
        args = ["CFLAGS=-Wno-unused-parameter"]
        return args
