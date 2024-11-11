# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.util.environment import EnvironmentModifications


class AoclDa(CMakePackage):
    """
    The AOCL Data Analytics Library (AOCL-DA) is a data analytics library
    providing optimized building blocks for data analysis. It is written with a
    C-compatible interface to make it as seamless as possible to integrate
    with the library from whichever programming language you are using.
    The intended workflow for using the library is as follows:
    • load data from memory by reading CSV files or using the in-built
    da_datastore object
    • preprocess the data by removing missing values, standardizing, and
    selecting certain subsets of the data, before extracting contiguous
    arrays of data from the da_datastore objects
    • data processing (e.g. principal component analysis, linear model
    fitting, etc.)
    C++ example programs can be found in the examples folder of your
    installation.
    """

    _name = "aocl-da"
    homepage = "https://www.amd.com/en/developer/aocl/data-analytics.html"
    git = "https://github.com/amd/aocl-data-analytics"
    url = "https://github.com/amd/aocl-data-analytics/archive/5.0.tar.gz"

    maintainers("amd-toolchain-support")

    version("5.0", sha256="3458adc7be39c78a08232c887f32838633149df0a69ccea024327c3edc5a5c1d")

    variant("examples", default=True, description="Build examples")
    variant("gtest", default=False, description="Build and install Googletest")
    variant("ilp64", default=False, description="Build with ILP64 support")
    variant(
        "openmp",
        default=True,
        description="Build using OpenMP and link to threaded BLAS and LAPACK",
    )
    variant("shared", default=True, description="Build shared libraries")
    variant("python", default=True, description="Build with Python bindings")

    # Fix to enable cmake to be configured with examples off but gtest on
    patch(
        "0001-Fix-to-enable-cmake-to-be-configured-with-examples-o.patch",
        sha256="65be59e99d52816cb77d3e887cd4816870576b46748b53073658caa9ca07d127",
        when="@5.0",
    )

    depends_on("cmake@3.22:", type="build")
    for vers in ["5.0"]:
        with when(f"@={vers}"):
            depends_on(f"aocl-utils@={vers} +shared", when="+shared")
            depends_on(f"aocl-utils@={vers} ~shared", when="~shared")
            depends_on(f"amdblis@={vers} libs=shared", when="+shared")
            depends_on(f"amdblis@={vers} libs=static", when="~shared")
            depends_on(f"amdlibflame@={vers} +shared", when="+shared")
            depends_on(f"amdlibflame@={vers} ~shared", when="~shared")
            depends_on(f"aocl-sparse@={vers} +shared", when="+shared")
            depends_on(f"aocl-sparse@={vers} ~shared", when="~shared")

    depends_on("amdblis threads=openmp", when="+openmp")
    depends_on("amdlibflame threads=openmp", when="+openmp")
    depends_on("amdblis threads=none", when="~openmp")
    depends_on("amdlibflame threads=none", when="~openmp")
    depends_on("aocl-sparse +openmp", when="+openmp")
    depends_on("aocl-sparse ~openmp", when="~openmp")

    with when("+python"):
        depends_on("python", type=("build", "run"))
        depends_on("py-wheel", type=("build", "run"))
        depends_on("py-setuptools", type=("build", "run"))
        depends_on("py-pybind11", type=("build", "link", "run"))
        depends_on("py-numpy", type=("build", "run"))
        depends_on("py-pip", type=("build", "run"))
        depends_on("patchelf", type="build")
        depends_on("py-pytest", type="test")
        depends_on("py-scikit-learn", type=("test", "run"))

    def setup_build_environment(self, env):
        if self.spec.satisfies("%aocc"):
            cc = self.compiler.cc
            compiler_install_dir = os.path.dirname(os.path.dirname(cc))
            env.append_path("LD_LIBRARY_PATH", join_path(compiler_install_dir, "lib"))

    def setup_run_environment(self, env):
        env.prepend_path("PYTHONPATH", join_path(self.prefix, "python_package"))

    def cmake_args(self):
        """Runs ``cmake`` in the build directory"""
        spec = self.spec
        args = []
        args.append(f"-DUTILS_LIB={spec['aocl-utils'].libs}")
        args.append(f"-DUTILS_CPUID_LIB={spec['aocl-utils'].libs}")
        args.append(f"-DUTILS_CORE_LIB={spec['aocl-utils'].libs}")
        args.append(f"-DBLAS_LIB={spec['amdblis'].libs}")
        args.append("-DBLAS_INCLUDE_DIR={0}/blis".format(spec["amdblis"].prefix.include))
        args.append(f"-DLAPACK_LIB={spec['amdlibflame'].libs}")
        args.append("-DLAPACK_INCLUDE_DIR={0}".format(spec["amdlibflame"].prefix.include))
        args.append(f"-DSPARSE_LIB={spec['aocl-sparse'].libs}")
        args.append("-DSPARSE_INCLUDE_DIR={0}".format(spec["aocl-sparse"].prefix.include))
        args.append(self.define_from_variant("BUILD_EXAMPLES", "examples"))
        args.append(self.define_from_variant("BUILD_GTEST", "gtest"))
        args.append(self.define_from_variant("BUILD_ILP64", "ilp64"))
        args.append(self.define_from_variant("BUILD_SMP", "openmp"))
        args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))
        args.append(self.define_from_variant("BUILD_PYTHON", "python"))

        return args

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test_python(self):
        """Perform smoke tests on the installed package."""
        pytest = which("pytest")
        envmod = EnvironmentModifications()
        envmod.append_path("PYTHONPATH", join_path(self.prefix, "python_package"))
        pytest.add_default_envmod(envmod)
        pytest(
            join_path(
                install_test_root(self), join_path(self.stage.source_path, "python_interface")
            )
        )
