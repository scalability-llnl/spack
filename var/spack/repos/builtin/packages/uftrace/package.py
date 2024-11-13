# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *


class Uftrace(AutotoolsPackage):
    """Dynamic function graph tracer for Linux which demangles C, C++ and Rust calls"""

    homepage = "https://uftrace.github.io/slide/"
    url = "https://github.com/namhyung/uftrace/archive/v0.16.tar.gz"
    git = "https://github.com/namhyung/uftrace.git"
    executables = ["^uftrace$"]
    maintainers("bernhardkaindl")
    tags = ["trace-tools"]

    license("GPL-2.0-or-later")

    # The build process uses 'git describe --tags' to get the package version
    version("master", branch="master", get_full_repo=True)
    version("0.16", sha256="dd0549f610d186b6f25fa2334a5e82b6ddc232ec6ca088dbb41b3fe66961d6bb")

    depends_on("c", type="build")
    depends_on("cxx", type="build")  # full demangler support with libstdc++
    variant("doc", default=False, description="Build uftrace's documentation")
    variant("python2", default=False, description="Build uftrace with python2 support")
    variant("python3", default=True, description="Build uftrace with python3 support")

    depends_on("pandoc", when="+doc", type="build")
    depends_on("capstone")
    depends_on("elfutils")
    depends_on("lsof", type="test")
    depends_on("pkgconfig", type="build")
    depends_on("libunwind")
    depends_on("libtraceevent")
    depends_on("ncurses")
    depends_on("python@2.7:", when="+python2")
    depends_on("python@3.5:", when="+python3")
    depends_on("lua-luajit")

    def check(self):
        make("test", *["V=1", "-j{0}".format(max(int(make_jobs), 20))])
        # In certain cases, tests using TCP/IP can hang. Ensure that spack can continue:
        os.system("kill -9 `lsof -t ./uftrace` 2>/dev/null")

    def install(self, spec, prefix):
        make("install", *["V=1"])

    def installcheck(self):
        pass

    def test_uftrace(self):
        """Perform stand-alone/smoke tests using the installed package."""
        uftrace = which(self.prefix.bin.uftrace)
        options = (["-A", ".", "-R", ".", "-P", "main", uftrace, "-V"],)
        expected = [
            r"dwarf",
            r"luajit",
            r"tui",
            r"sched",
            r"dynamic",
            r"main\(2, ",
            r"  getopt_long\(2, ",
            r"  .*printf.*\(",
            r"} = 0; /\* main \*/",
        ]
        out = uftrace(*options, output=str.split, error=str.split)
        check_outputs(expected, out)

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"uftrace v(\S+)", output)
        return match.group(1) if match else "None"
