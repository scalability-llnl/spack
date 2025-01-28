# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Masa(AutotoolsPackage):
    """MASA (Manufactured Analytical Solution Abstraction) is a library
    written in C++ (with C, python and Fortran90 interfaces) which
    provides a suite of manufactured solutions for the software
    verification of partial differential equation solvers in multiple
    dimensions."""

    homepage = "https://github.com/manufactured-solutions/MASA"
    git = "https://github.com/manufactured-solutions/MASA.git"

    license("LGPL-2.1-or-later")

    version("master", branch="master")
    version("0.51.0", tag="0.51.0")
    version("0.50.0", tag="0.50.0")
    version("0.44.0", tag="0.44.0")
    version("0.43.1", tag="0.43.1")
    version("0.43.0", tag="0.43.0")
    version("0.42.0", tag="0.42.0")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build", when="+fortran")

    variant("fortran", default=False, description="Compile with Fortran interfaces")
    variant("python", default=False, description="Compile with Python interfaces")

    depends_on("gettext")
    depends_on("metaphysicl")
    depends_on("python")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("swig", type="build", when="+python")

    def configure_args(self):
        options = []

        options.extend(["--with-metaphysicl=%s" % self.spec["metaphysicl"].prefix])

        if "+fortran" in self.spec:
            options.extend(["--enable-fortran-interfaces"])

        if "+python" in self.spec:
            options.extend(["--enable-python-interfaces"])

        return options

    def setup_build_environment(self, env):
        # Unfortunately can't use this because MASA overwrites it
        # env.set('CXXFLAGS', self.compiler.cxx11_flag)
        env.set("CXX", "{0} {1}".format(self.compiler.cxx, self.compiler.cxx11_flag))
        if self.spec.satisfies("%apple-clang"):
            env.set("CFLAGS", "-Wno-implicit-function-declaration")
