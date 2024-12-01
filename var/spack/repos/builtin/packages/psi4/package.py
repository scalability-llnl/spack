# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Psi4(CMakePackage):
    """Psi4 is an open-source suite of ab initio quantum chemistry
    programs designed for efficient, high-accuracy simulations of
    a variety of molecular properties."""

    homepage = "https://www.psicode.org/"
    url = "https://github.com/psi4/psi4/archive/v1.3.2.tar.gz"

    license("LGPL-3.0-only")

    version("1.3.2", sha256="ed76c67803b6420f35f57a6dd31c47108b9145b8c9fced5c94cdc179f6b5fbf3")

    depends_on("cxx", type="build")  # generated

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )

    # Required dependencies
    depends_on("blas")
    depends_on("lapack")
    depends_on("boost+chrono+filesystem+python+regex+serialization+system+timer+thread")
    depends_on("python")
    depends_on("cmake@3.3:", type="build")
    depends_on("py-numpy", type=("build", "run"))

    # Optional dependencies
    # TODO: add packages for these
    # depends_on('perl')
    # depends_on('erd')
    # depends_on('pcm-solver')
    # depends_on('chemps2')

    def cmake_args(self):
        spec = self.spec

        return [
            "-DBLAS_TYPE={0}".format(spec["blas"].name.upper()),
            "-DBLAS_LIBRARIES={0}".format(spec["blas"].libs.joined()),
            "-DLAPACK_TYPE={0}".format(spec["lapack"].name.upper()),
            "-DLAPACK_LIBRARIES={0}".format(spec["lapack"].libs.joined()),
            "-DBOOST_INCLUDEDIR={0}".format(spec["boost"].prefix.include),
            "-DBOOST_LIBRARYDIR={0}".format(spec["boost"].prefix.lib),
            "-DENABLE_CHEMPS2=OFF",
        ]

    @run_after("install")
    def filter_compilers(self):
        """Run after install to tell the configuration files to
        use the compilers that Spack built the package with.

        If this isn't done, they'll have PLUGIN_CXX set to
        Spack's generic cxx. We want it to be bound to
        whatever compiler it was built with."""

        spec = self.spec
        prefix = spec.prefix

        kwargs = {"ignore_absent": True, "backup": False, "string": True}

        cc_files = ["bin/psi4-config"]
        cxx_files = ["bin/psi4-config", "include/psi4/psiconfig.h"]
        template = "share/psi4/plugin/Makefile.template"

        for filename in cc_files:
            filter_file(
                os.environ["CC"], self.compiler.cc, os.path.join(prefix, filename), **kwargs
            )

        for filename in cxx_files:
            filter_file(
                os.environ["CXX"], self.compiler.cxx, os.path.join(prefix, filename), **kwargs
            )

        # The binary still keeps track of the compiler used to install Psi4
        # and uses it when creating a plugin template
        filter_file("@PLUGIN_CXX@", self.compiler.cxx, os.path.join(prefix, template), **kwargs)

        # The binary links to the build include directory instead of the
        # installation include directory:
        # https://github.com/psi4/psi4/issues/410
        filter_file(
            "@PLUGIN_INCLUDES@",
            "-I{0}".format(
                " -I".join(
                    [
                        os.path.join(spec["psi4"].prefix.include, "psi4"),
                        os.path.join(spec["boost"].prefix.include, "boost"),
                        os.path.join(spec["python"].headers.directories[0]),
                        spec["lapack"].prefix.include,
                        spec["blas"].prefix.include,
                        "/usr/include",
                    ]
                )
            ),
            os.path.join(prefix, template),
            **kwargs,
        )
