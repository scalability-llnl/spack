# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Cantera(SConsPackage):
    """Cantera is a suite of object-oriented software tools for problems
    involving chemical kinetics, thermodynamics, and/or transport processes."""

    homepage = "https://www.cantera.org/docs/sphinx/html/index.html"
    url = "https://github.com/Cantera/cantera/archive/v2.5.1.tar.gz"

    version("2.5.1", sha256="59f673cec686bc9b1eeccc1b1c9158a3978a3abe7491d00e8b355908c1c3be0a")
    version("2.4.0", sha256="0dc771693b657d8f4ba835dd229939e5b9cfd8348d2f5ba82775451a524365a5")
    version("2.3.0", sha256="06624f0f06bdd2acc9c0dba13443d945323ba40f68a9d422d95247c02e539b57")
    version("2.2.1", sha256="c7bca241848f541466f56e479402521c618410168e8983e2b54ae48888480e1e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("python", default=False, description="Build the Cantera Python module")
    variant("matlab", default=False, description="Build the Cantera Matlab toolbox")
    variant("sundials", default=True, description="Build with Sundials")

    # Required dependencies
    depends_on("fmt@3.0.0:3.0.2", when="@2.3.0:")
    depends_on("googletest+gmock", when="@2.3.0:")
    depends_on("eigen", when="@2.3.0:")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("sundials@:3.1.2+lapack", when="+sundials")  # must be compiled with -fPIC
    depends_on("blas")
    depends_on("lapack")
    depends_on("yaml-cpp")

    # Python module dependencies
    extends("python", when="+python")
    depends_on("py-cython", when="+python", type="build")
    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("py-scipy", when="+python", type=("build", "run"))
    depends_on("py-3to2", when="+python", type=("build", "run"))

    # Matlab toolbox dependencies
    extends("matlab", when="+matlab")

    conflicts("~sundials", when="@2.3.0:")

    def build_args(self, spec, prefix):
        # Valid args can be found by running `scons help`

        # Required args
        args = [
            "build",
            "prefix={0}".format(prefix),
            "VERBOSE=yes",
            "CC={0}".format(spack_cc),
            "CXX={0}".format(spack_cxx),
            "FORTRAN={0}".format(spack_fc),
            "cc_flags={0}".format(self.compiler.cc_pic_flag),
            # Allow Spack environment variables to propagate through to SCons
            "env_vars=all",
        ]

        if spec.satisfies("@:2.2.1"):
            args.append("F77={0}".format(spack_f77))

        # fmt support
        if spec.satisfies("@2.3.0:"):
            args.append("system_fmt=y")

        # Googletest support
        if spec.satisfies("@2.3.0:"):
            args.append("system_googletest=y")

        # Eigen support
        if spec.satisfies("@2.3.0:"):
            args.extend(
                [
                    "system_eigen=y",
                    "extra_inc_dirs={0}".format(
                        join_path(
                            spec["eigen"].prefix.include,
                            "eigen{0}".format(spec["eigen"].version.up_to(1)),
                        )
                    ),
                ]
            )

        # BLAS/LAPACK support
        lapack_blas = spec["lapack"].libs + spec["blas"].libs
        args.extend(
            [
                "blas_lapack_libs={0}".format(",".join(lapack_blas.names)),
                "blas_lapack_dir={0}".format(spec["lapack"].prefix.lib),
            ]
        )

        # Boost support
        if spec.satisfies("@2.3.0:"):
            args.append("boost_inc_dir={0}".format(spec["boost"].prefix.include))
        else:
            args.extend(
                [
                    "build_thread_safe=yes",
                    "boost_inc_dir={0}".format(spec["boost"].prefix.include),
                    "boost_lib_dir={0}".format(spec["boost"].prefix.lib),
                ]
            )

        # Sundials support
        if spec.satisfies("+sundials"):
            if spec.satisfies("@2.3.0:"):
                args.append("system_sundials=y")
            else:
                args.extend(
                    [
                        "use_sundials=y",
                        "sundials_license={0}".format(spec["sundials"].prefix.LICENSE),
                    ]
                )

            args.extend(
                [
                    "sundials_include={0}".format(spec["sundials"].prefix.include),
                    "sundials_libdir={0}".format(spec["sundials"].prefix.lib),
                ]
            )

        # Python module
        if spec.satisfies("+python"):
            args.extend(["python_package=full", "python_cmd={0}".format(python.path)])
            if spec["python"].satisfies("@3:"):
                args.extend(["python3_package=y", "python3_cmd={0}".format(python.path)])
            else:
                args.append("python3_package=n")
        else:
            args.append("python_package=none")
            args.append("python3_package=n")

        # Matlab toolbox
        if spec.satisfies("+matlab"):
            args.extend(["matlab_toolbox=y", "matlab_path={0}".format(spec["matlab"].prefix)])
        else:
            args.append("matlab_toolbox=n")

        return args

    def build_test(self):
        if self.spec.satisfies("+python"):
            # Tests will always fail if Python dependencies aren't built
            # In addition, 3 of the tests fail when run in parallel
            scons("test", parallel=False)

    @run_after("install")
    def filter_compilers(self):
        """Run after install to tell the Makefile and SConstruct files to use
        the compilers that Spack built the package with.

        If this isn't done, they'll have CC, CXX, F77, and FC set to Spack's
        generic cc, c++, f77, and f90. We want them to be bound to whatever
        compiler they were built with."""

        kwargs = {"ignore_absent": True, "backup": False, "string": True}
        dirname = os.path.join(self.prefix, "share/cantera/samples")

        cc_files = [
            "cxx/rankine/Makefile",
            "cxx/NASA_coeffs/Makefile",
            "cxx/kinetics1/Makefile",
            "cxx/flamespeed/Makefile",
            "cxx/combustor/Makefile",
            "f77/SConstruct",
        ]

        cxx_files = [
            "cxx/rankine/Makefile",
            "cxx/NASA_coeffs/Makefile",
            "cxx/kinetics1/Makefile",
            "cxx/flamespeed/Makefile",
            "cxx/combustor/Makefile",
        ]

        f77_files = ["f77/Makefile", "f77/SConstruct"]

        fc_files = ["f90/Makefile", "f90/SConstruct"]

        for filename in cc_files:
            filter_file(
                os.environ["CC"], self.compiler.cc, os.path.join(dirname, filename), **kwargs
            )

        for filename in cxx_files:
            filter_file(
                os.environ["CXX"], self.compiler.cxx, os.path.join(dirname, filename), **kwargs
            )

        for filename in f77_files:
            filter_file(
                os.environ["F77"], self.compiler.f77, os.path.join(dirname, filename), **kwargs
            )

        for filename in fc_files:
            filter_file(
                os.environ["FC"], self.compiler.fc, os.path.join(dirname, filename), **kwargs
            )
