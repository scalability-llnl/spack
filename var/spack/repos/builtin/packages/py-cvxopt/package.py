# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCvxopt(PythonPackage):
    """CVXOPT is a free software package for convex optimization based on the
    Python programming language."""

    homepage = "https://cvxopt.org/"
    pypi = "cvxopt/cvxopt-1.1.9.tar.gz"

    license("GPL-3.0-only")

    version("1.2.5", sha256="94ec8c36bd6628a11de9014346692daeeef99b3b7bae28cef30c7490bbcb2d72")

    depends_on("c", type="build")  # generated

    variant(
        "gsl",
        default=False,
        description="Use GSL random number generators for constructing random matrices",
    )
    variant("fftw", default=False, description="Install the cvxopt.fftw interface to FFTW")
    variant(
        "glpk", default=False, description="Enable support for the linear programming solver GLPK"
    )
    # variant(
    #     'mosek',
    #     default=False,
    #     description=(
    #         'Enable support for the linear, second-order cone, and quadratic '
    #         'programming solvers in MOSEK'
    #     ),
    # )
    variant(
        "dsdp",
        default=False,
        description="Enable support for the semidefinite programming solver DSDP",
    )

    # Required dependencies
    depends_on("python@2.7:", type=("build", "link", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("blas")
    depends_on("lapack")
    depends_on("suite-sparse")

    # Optional dependencies
    depends_on("gsl", when="+gsl")
    depends_on("fftw", when="+fftw")
    depends_on("glpk", when="+glpk")
    # depends_on('mosek@8:',  when='+mosek')
    depends_on("dsdp@5.8:", when="+dsdp")

    def setup_build_environment(self, env):
        spec = self.spec

        # BLAS/LAPACK Libraries

        # Default names of BLAS and LAPACK libraries
        env.set("CVXOPT_BLAS_LIB", ";".join(spec["blas"].libs.names))
        env.set("CVXOPT_LAPACK_LIB", ";".join(spec["lapack"].libs.names))

        # Directory containing BLAS and LAPACK libraries
        env.set("CVXOPT_BLAS_LIB_DIR", spec["blas"].libs.directories[0])

        # SuiteSparse Libraries

        # Directory containing SuiteSparse libraries
        env.set("CVXOPT_SUITESPARSE_LIB_DIR", spec["suite-sparse"].libs.directories[0])

        # Directory containing SuiteSparse header files
        env.set("CVXOPT_SUITESPARSE_INC_DIR", spec["suite-sparse"].headers.directories[0])

        # GSL Libraries

        if "+gsl" in spec:
            env.set("CVXOPT_BUILD_GSL", 1)

            # Directory containing libgsl
            env.set("CVXOPT_GSL_LIB_DIR", spec["gsl"].libs.directories[0])

            # Directory containing the GSL header files
            env.set("CVXOPT_GSL_INC_DIR", spec["gsl"].headers.directories[0])
        else:
            env.set("CVXOPT_BUILD_GSL", 0)

        # FFTW Libraries

        if "+fftw" in spec:
            env.set("CVXOPT_BUILD_FFTW", 1)

            # Directory containing libfftw3
            env.set("CVXOPT_FFTW_LIB_DIR", spec["fftw"].libs.directories[0])

            # Directory containing fftw.h
            env.set("CVXOPT_FFTW_INC_DIR", spec["fftw"].headers.directories[0])
        else:
            env.set("CVXOPT_BUILD_FFTW", 0)

        # GLPK Libraries

        if "+glpk" in spec:
            env.set("CVXOPT_BUILD_GLPK", 1)

            # Directory containing libglpk
            env.set("CVXOPT_GLPK_LIB_DIR", spec["glpk"].libs.directories[0])

            # Directory containing glpk.h
            env.set("CVXOPT_GLPK_INC_DIR", spec["glpk"].headers.directories[0])
        else:
            env.set("CVXOPT_BUILD_GLPK", 0)

        # DSDP Libraries

        if "+dsdp" in spec:
            env.set("CVXOPT_BUILD_DSDP", 1)

            # Directory containing libdsdp
            env.set("CVXOPT_DSDP_LIB_DIR", spec["dsdp"].libs.directories[0])

            # Directory containing dsdp5.h
            env.set("CVXOPT_DSDP_INC_DIR", spec["dsdp"].headers.directories[0])

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        """Test that the installation was successful."""
        python("-m", "unittest", "discover", "-s", "tests")
