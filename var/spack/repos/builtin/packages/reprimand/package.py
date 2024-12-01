# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Reprimand(MesonPackage):
    """RePrimAnd: Recovery of Primitives And EOS framework

    RePrimAnd is a support library for numerical simulations of general
    relativistic magnetohydrodynamics. It provides methods for recovering
    primitive variables like pressure and velocity from the variables evolved
    in quasi-conservative formulations. Further, it provides a general
    framework for handling matter equations of state."""

    homepage = "https://wokast.github.io/RePrimAnd/index.html"
    url = "https://github.com/wokast/RePrimAnd/archive/refs/tags/v1.3.tar.gz"

    maintainers("eschnett")

    license("CC-BY-NC-SA-4.0")

    version("develop", git="https://github.com/wokast/RePrimAnd", branch="public")
    version("1.5", sha256="bc71030c1ae337c3631cfc7e46270260b0663e4ad73129148bf443c9220afb86")
    version("1.4", sha256="260730696175fa21d35d1a92df2c68b69243bb617083c82616efcb4720d557e8")
    version("1.3", sha256="8e9f05b1f065a876d1405562285a9f64d1b31c4a436d5a6bb1f023212b40314e")

    depends_on("cxx", type="build")  # generated

    # Add missing #include statments; see
    # <https://github.com/wokast/RePrimAnd/issues/3>
    patch("include.patch", when="@1.3")

    variant("python", default=False, description="Enable Python bindings")
    variant("shared", default=True, description="Build shared library")

    depends_on("boost +json +math +test")
    depends_on("gsl")
    depends_on("hdf5")
    depends_on("python", when="+python")
    depends_on("py-matplotlib", when="+python")
    depends_on("py-pybind11 @2.6.0:", when="+python")

    extends("python", when="+python")

    def setup_build_environment(self, env):
        env.set("CXXFLAGS", self.compiler.cxx11_flag)
        env.set("BOOST_ROOT", self.spec["boost"].prefix)

    def meson_args(self):
        args = []
        if self.spec.satisfies("@:1.4"):
            args.extend(
                [
                    "-Dbuild_documentation=false",
                    "-Dbuild_python_api={0}".format(str("+python" in self.spec).lower()),
                ]
            )
        return args

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries("libRePrimAnd*", root=self.prefix, shared=shared, recursive=True)
