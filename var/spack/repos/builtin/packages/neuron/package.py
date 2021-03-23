# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Neuron(CMakePackage):
    """NEURON is a simulation environment for single and networks of neurons.

    NEURON is a simulation environment for modeling individual and networks of
    neurons. NEURON models individual neurons via the use of sections that are
    automatically subdivided into individual compartments, instead of
    requiring the user to manually create compartments.
    """

    homepage = "https://www.neuron.yale.edu/"
    url      = "https://neuron.yale.edu/ftp/neuron/versions/v7.7/nrn-7.7.tar.gz"
    git      = "https://github.com/neuronsimulator/nrn"
    maintainers = ['pramodk', 'nrnhines', 'iomaganaris', 'alexsavulescu']

    version('develop', branch='master', submodules='True')
    version("7.8.2", tag="7.8.2", submodules='True')
    version("7.8.1", tag="7.8.1", submodules='True')

    variant("coreneuron",    default=False, description="Enable CoreNEURON as submodule")
    variant("cross-compile", default=False, description="Build for cross-compile environment")
    variant("interviews",    default=False, description="Enable GUI with INTERVIEWS")
    variant("legacy-unit",   default=False, description="Enable legacy units")
    variant("mpi",           default=True,  description="Enable MPI parallelism")
    variant("python",        default=True,  description="Enable python")
    variant("rx3d",          default=False,  description="Enable cython translated 3-d rxd")
    variant("tests",         default=False, description="Enable unit tests")

    depends_on("bison",     type="build")
    depends_on("flex",      type="build")
    depends_on("py-cython", when="+rx3d", type="build")

    depends_on("gettext")
    depends_on("mpi",         when="+mpi")
    depends_on("ncurses")
    depends_on("python@2.7:", when="+python")
    depends_on("py-pytest",   when="+python+tests")
    depends_on("readline")

    conflicts("+rx3d",        when="~python")

    patch("patch-v782-git-cmake-avx512.patch", when="@7.8.2")

    def cmake_args(self):
        spec = self.spec

        def cmake_options(spec_options):
            value = "TRUE" if spec_options in spec else "FALSE"
            cmake_name = spec_options[1:].upper().replace("-", "_")
            return "-DNRN_ENABLE_" + cmake_name + ":BOOL=" + value

        args = [cmake_options(variant) for variant in ["+coreneuron",
                                                       "+interviews",
                                                       "+mpi",
                                                       "+python",
                                                       "+rx3d",
                                                       "+coreneuron",
                                                       "+tests"]]
        args.append("-DNRN_ENABLE_BINARY_SPECIAL=ON")

        if "~mpi" in spec and '+coreneuron' in spec:
            args.append("-DCORENRN_ENABLE_MPI=OFF")

        if "+python" in spec:
            args.append("-DPYTHON_EXECUTABLE:FILEPATH="
                        + spec["python"].command.path)

        if spec.variants['build_type'].value == 'Debug':
            args.append("-DCMAKE_C_FLAGS=-g -O0")
            args.append("-DCMAKE_CXX_FLAGS=-g -O0")
            args.append("-DCMAKE_BUILD_TYPE=Custom")

        if "+legacy-unit" in spec:
            args.append('-DNRN_DYNAMIC_UNITS_USE_LEGACY=ON')

        return args

    @run_after("install")
    def filter_compilers(self):
        """run after install to avoid spack compiler wrappers
        getting embded into nrnivmodl script"""

        spec = self.spec

        if "cray" in spec.architecture:
            cc_compiler = "cc"
            cxx_compiler = "CC"
        elif spec.satisfies("+mpi"):
            cc_compiler = spec["mpi"].mpicc
            cxx_compiler = spec["mpi"].mpicxx
        else:
            cc_compiler = self.compiler.cc
            cxx_compiler = self.compiler.cxx

        kwargs = {"backup": False, "string": True}
        nrnmech_makefile = join_path(self.prefix,
                                     "./bin/nrnmech_makefile")

        # assign_operator is changed to fix wheel support
        if self.spec.satisfies("@:7.99"):
            assign_operator = "?="
        else:
            assign_operator = "="

        filter_file("CC {0} {1}".format(assign_operator, env["CC"]),
                    "CC = {0}".format(cc_compiler),
                    nrnmech_makefile,
                    **kwargs)
        filter_file("CXX {0} {1}".format(assign_operator, env["CXX"]),
                    "CXX = {0}".format(cxx_compiler),
                    nrnmech_makefile,
                    **kwargs)

        if spec.satisfies("+coreneuron"):
            corenrn_makefile = join_path(self.prefix,
                                         "share/coreneuron/nrnivmodl_core_makefile")
            filter_file(env["CXX"], cxx_compiler, corenrn_makefile, **kwargs)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", join_path(self.prefix, "bin"))
        env.prepend_path("LD_LIBRARY_PATH", join_path(self.prefix, "lib"))
        if self.spec.satisfies("+python"):
            env.prepend_path("PYTHONPATH", self.spec.prefix.lib.python)
