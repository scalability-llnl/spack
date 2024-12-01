# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Pagmo(CMakePackage):
    """Parallel Global Multiobjective Optimizer (and its Python alter ego
    PyGMO) is a C++ / Python platform to perform parallel computations of
    optimisation tasks (global and local) via the asynchronous generalized
    island model."""

    # Multiple homepages:
    # C++    interface: https://esa.github.io/pagmo/
    # Python interface: https://esa.github.io/pygmo/

    homepage = "https://esa.github.io/pagmo/"
    url = "https://github.com/esa/pagmo/archive/1.1.7.tar.gz"

    license("GPL-3.0-or-later")

    version("1.1.7", sha256="6d8fab89ef9d5d5f30f148225bf9b84b2e5a38997f3d68b85547840e9fd95172")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("examples", default=False, description="Build examples")
    variant("cxx", default=True, description="Build the C++ interface")
    variant("python", default=True, description="Build Python bindings")
    variant("gsl", default=True, description="Enable support for GSL minimisers")
    variant("gtop", default=False, description="Build GTOP database problems")
    variant("ipopt", default=False, description="Enable support for IPOPT minimiser")
    variant("mpi", default=True, description="Enable support for MPI")
    variant("nlopt", default=False, description="Enable support for NLopt minimisers")
    variant("snopt", default=False, description="Enable support for SNOPT minimiser")
    variant("worhp", default=False, description="Enable support for WORHP minimiser")
    variant("headers", default=True, description="Installs the header files")
    variant("blas", default=True, description="Enable support for BLAS")
    variant("scipy", default=True, description="Enable support for scipy")
    variant("networkx", default=False, description="Enable support for networkx")
    variant("vpython", default=False, description="Enable support for vpython")
    variant("pykep", default=False, description="Enable support for pykep")

    extends("python", when="+python")

    # Concretization in Spack is currently broken
    # depends_on('boost+system+serialization+thread')
    # depends_on('boost+python',    when='+python')
    # depends_on('boost+date_time', when='+gtop')

    # Workaround for now
    depends_on("boost+system+serialization+thread", when="~python~gtop")
    depends_on("boost+system+serialization+thread+python", when="+python~gtop")
    depends_on("boost+system+serialization+thread+date_time", when="~python+gtop")
    depends_on("boost+system+serialization+thread+python+date_time", when="+python+gtop")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)

    depends_on("gsl@1.15:", when="+gsl")
    depends_on("ipopt", when="+ipopt")
    depends_on("mpi@1.2:", when="+mpi")
    depends_on("blas", when="+blas")
    depends_on("py-scipy", type=("build", "run"), when="+scipy")
    depends_on("py-networkx", type=("build", "run"), when="+networkx")

    # TODO: Add packages for missing dependencies
    # depends_on('nlopt+cxx', when='+nlopt')
    # depends_on('snopt',     when='+snopt')
    # depends_on('py-vpython',     type=('build', 'run'), when='+vpython')
    # depends_on('py-pykep@1.15:', type=('build', 'run'), when='+gtop')
    # depends_on('py-pykep@1.15:', type=('build', 'run'), when='+pykep')

    depends_on("cmake@2.8:", type="build")

    def variant_to_bool(self, variant):
        return "ON" if variant in self.spec else "OFF"

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define_from_variant("BUILD_EXAMPLES", "examples"),
            self.define_from_variant("BUILD_MAIN", "cxx"),
            self.define_from_variant("BUILD_PYGMO", "python"),
            self.define_from_variant("ENABLE_GSL", "gsl"),
            self.define_from_variant("ENABLE_GTOP_DATABASE", "gtop"),
            self.define_from_variant("ENABLE_IPOPT", "ipopt"),
            self.define_from_variant("ENABLE_MPI", "mpi"),
            self.define_from_variant("ENABLE_NLOPT", "nlopt"),
            self.define_from_variant("ENABLE_SNOPT", "snopt"),
            self.define_from_variant("ENABLE_WORHP", "worhp"),
            self.define_from_variant("INSTALL_HEADERS", "headers"),
            self.define("ENABLE_TESTS", self.run_tests),
        ]

        if "+python" in spec:
            args.extend(
                [
                    # By default installs to the python prefix not the pagmo prefix
                    "-DPYTHON_MODULES_DIR={0}".format(python_platlib)
                ]
            )

        return args
