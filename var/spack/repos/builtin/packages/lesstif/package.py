# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lesstif(AutotoolsPackage):
    """LessTif is the Hungry Programmers' version of OSF/Motif."""

    homepage = "https://sourceforge.net/projects/lesstif/"
    url = "https://sourceforge.net/projects/lesstif/files/lesstif/0.95.2/lesstif-0.95.2.tar.bz2/download"

    license("LGPL-2.0-only")

    version("0.95.2", sha256="eb4aa38858c29a4a3bcf605cfe7d91ca41f4522d78d770f69721e6e3a4ecf7e3")

    depends_on("c", type="build")  # generated

    variant("shared", default=True, description="Build shared libraries")
    variant("static", default=False, description="Build static libraries")

    depends_on("libice")
    depends_on("libsm")
    depends_on("libxt")
    depends_on("libxext")

    def patch(self):
        filter_file("ACLOCALDIR=.*", "ACLOCALDIR='${datarootdir}/aclocal'", "configure")

    def setup_build_environment(self, env):
        # 'sed' fails if LANG=en_US.UTF-8 as is often the case on Macs.
        # The configure script finds our superenv sed wrapper, sets
        # SED, but then doesn't use that variable.
        env.set("LANG", "C")

    def configure_args(self):
        spec = self.spec

        args = [
            "--disable-debug",
            "--enable-production",
            "--disable-dependency-tracking",
            "--enable-shared" if spec.satisfies("+shared") else "--disable-shared",
            "--enable-static" if spec.satisfies("+static") else "--disable-static",
        ]

        return args

    # LessTif won't install in parallel 'cause several parts of the
    # Makefile will try to make the same directory and `mkdir` will fail.
    def install(self, spec, prefix):
        make("install", parallel=False)
