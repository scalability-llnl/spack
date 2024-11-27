# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kmod(AutotoolsPackage):
    """kmod is a set of tools to handle common tasks with Linux kernel modules
    like insert, remove, list, check properties, resolve dependencies and
    aliases."""

    homepage = "https://github.com/lucasdemarchi/kmod"
    url = "https://github.com/lucasdemarchi/kmod/archive/v27.tar.gz"

    license("GPL-2.0-or-later")

    version("27", sha256="969c4573b01f4c9e1d3e3c9d179bd16ec999bbb99dd55b7623f42551328478c3")
    version("26", sha256="f28bc40ead548dce4a8e956fccfc36fd80f2b40884d270b812f1bfbd886e858c")
    version("25", sha256="16a8bbd3ee321d0847847256ea2fd124f6250257c055c8cf97e78f18bf27559c")
    version("24", sha256="f7a5ee07d4901c87711880536604de7e31c182d85a72de7b8d7dd04d4ee0aa59")
    version("23", sha256="8f139543d82e8ccc2227dec4c016d6656e9789365a6dce73f90b620a53e62ee6")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("lzma")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("autogen.sh")

    def configure_args(self):
        args = [
            "--disable-manpages",
            "--with-bashcompletiondir="
            + join_path(self.spec["kmod"].prefix, "share", "bash-completion", "completions"),
        ]
        return args
