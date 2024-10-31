# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hping(AutotoolsPackage):
    """hping is a command-line oriented TCP/IP packet assembler/analyzer."""

    homepage = "http://www.hping.org"
    git = "https://github.com/antirez/hping.git"

    license("GPL-2.0-only")

    version("master", commit="3547c7691742c6eaa31f8402e0ccbb81387c1b99")

    depends_on("c", type="build")  # generated

    patch("bpf.patch", sha256="99b9f91a308ffca306f69ccdb285e289ee3d280ec47ec7229e3a7669cca512f2")

    depends_on("libpcap")
    depends_on("tcl")

    def setup_build_environment(self, env):
        env.set("TCLSH", self.spec["tcl"].prefix.bin.tclsh)

    @run_before("configure")
    def filter_before_configure(self):
        makefileIn = FileFilter("Makefile.in")
        makefileIn.filter(r"/usr/sbin", self.prefix.sbin)
        configure = FileFilter("configure")
        configure.filter(r"/usr/local/include/tcl\${TCL_VER}", self.spec["tcl"].prefix.include)
        configure.filter(r"/usr/local/lib/", self.spec["tcl"].libs.directories[0])

    def install(self, spec, prefix):
        mkdirp(prefix.sbin)
        make("install")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
