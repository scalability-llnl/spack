# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class Expect(AutotoolsPackage):
    """Expect is a tool for automating interactive applications such as
    telnet, ftp, passwd, fsck, rlogin, tip, etc."""

    homepage = "https://expect.sourceforge.net/"
    url = (
        "https://sourceforge.net/projects/expect/files/Expect/5.45.4/expect5.45.4.tar.gz/download"
    )

    license("NIST-PD")

    version("5.45.4", sha256="49a7da83b0bdd9f46d04a04deec19c7767bb9a323e40c4781f89caf760b92c34")
    version("5.45.3", sha256="c520717b7195944a69ce1492ec82ca0ac3f3baf060804e6c5ee6d505ea512be9")
    version("5.45", sha256="b28dca90428a3b30e650525cdc16255d76bb6ccd65d448be53e620d95d5cc040")

    depends_on("c", type="build")  # generated

    depends_on("tcl")

    depends_on("automake", type="build")
    depends_on("autoconf", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    force_autoreconf = True

    patch("xcode_12.patch", when="%apple-clang@12:")
    patch("expect_detect_tcl_private_header_os_x_mountain_lion.patch", when="@5.45:5.45.0")

    def configure_args(self):
        spec = self.spec

        args = [
            # Without this, expect binary and library are not installed
            "--exec-prefix={0}".format(self.prefix),
            "--enable-threads",
            "--enable-shared",
            "--enable-64bit",
            "--with-tcl={0}".format(spec["tcl"].libs.directories[0]),
            "--with-tclinclude={0}".format(spec["tcl"].headers.directories[0]),
        ]

        return args

    @run_after("install")
    def symlink_library(self):
        """Expect installs libraries into:

        lib/expect5.45/libexpect5.45.so

        Create a symlink so that the library can be found in lib."""

        target = join_path(self.prefix.lib, "expect*", "libexpect*")
        target = glob.glob(target)[0]

        link_name = os.path.basename(target)
        link_name = join_path(self.prefix.lib, link_name)

        symlink(target, link_name)

    @run_after("install")
    def darwin_fix(self):
        # The shared library is not installed correctly on Darwin; fix this
        if self.spec.satisfies("platform=darwin"):
            fix_darwin_install_name(join_path(self.prefix.lib, "expect{0}".format(self.version)))

            old = "libexpect{0}.dylib".format(self.version)
            new = glob.glob(join_path(self.prefix.lib, "expect*", "libexpect*"))[0]
            install_name_tool = Executable("install_name_tool")
            install_name_tool("-change", old, new, self.prefix.bin.expect)
