# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class Gaussian(Package):
    """Gaussian is a computer program for computational chemistry"""

    homepage = "http://www.gaussian.com/"
    manual_download = True

    maintainers("antoniokaust")

    version("16-B.01", sha256="0b2cf60aa85d2c8c8e7547446e60e8e8cb67eec20e5f13c4a3e4e7616dcdf122")
    version("09-D.01", sha256="ef14885b5e334b6ec44a93bfd7225c634247dc946416af3087ab055bf05f54cd")

    depends_on("tcsh")

    def patch(self):
        csh = join_path(self.spec["tcsh"].prefix.bin, "csh")
        tcsh = join_path(self.spec["tcsh"].prefix.bin, "tcsh")
        dirs = ["bsd", "tests"]
        for d in dirs:
            for f in next(os.walk(d))[2]:
                filter_file("^#!/bin/csh", "#!{0}".format(csh), join_path(d, f))
                filter_file("^#!/bin/tcsh", "#!{0}".format(tcsh), join_path(d, f))

    @property
    def ver(self):
        return self.version.string.split("-")[0]

    @property
    def g_root(self):
        return join_path(self.prefix, "g" + self.ver)

    @property
    def g_bsd(self):
        return join_path(self.g_root, "bsd")

    def url_for_version(self, version):
        return "file://{0}/g{1}.tgz".format(os.getcwd(), version)

    def install(self, spec, prefix):
        install_tree(".", self.g_root)

    @run_after("install")
    def bsd_install(self):
        with working_dir(self.g_root):
            bsd_install = Executable(join_path("bsd", "install"))
            bsd_install()

    def setup_run_environment(self, env):
        env.set("g" + self.ver + "root", self.prefix)

        env.prepend_path("GAUSS_EXEDIR", self.g_root)
        env.prepend_path("GAUSS_EXEDIR", self.g_bsd)

        env.prepend_path("PATH", self.g_root)
        env.prepend_path("PATH", self.g_bsd)

        env.set("GAUSS_LEXEDIR", join_path(self.g_root, "linda-exe"))
        env.set("GAUSS_ARCHDIR", join_path(self.g_root, "arch"))
        env.set("GAUSS_BSDDIR", self.g_bsd)
        env.set("G" + self.ver + "BASIS", join_path(self.g_root, "basis"))

        env.prepend_path("LD_LIBRARY_PATH", self.g_root)
        env.prepend_path("LD_LIBRARY_PATH", self.g_bsd)
