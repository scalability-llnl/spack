# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class N2p2(MakefilePackage):
    """N2p2 (The neural network potential package) provides ready-to-use
       software for high-dimensional neural network potentials
       in computational physics and chemistry."""

    homepage = "https://github.com/CompPhysVienna/n2p2"
    url = "https://github.com/CompPhysVienna/n2p2/archive/v2.1.0.tar.gz"

    version(
        "2.1.1",
        sha256="90fbc0756132984d0d7e6d92d2f53358c120e75f148910d90c027158163251b9",
    )
    version(
        "2.1.0",
        sha256="283c00e9a5b964f4c84a70c5f1cef7167e9b881080b50a221da08799e5ede400",
    )

    variant("doc", default=False, description="build documentation with Doxygen")

    patch("interface-makefile.patch", when="@2.1.0")
    patch("interface-makefile211.patch", when="@2.1.1")
    patch("libnnp-makefile.patch")
    patch("nnp_test.h.patch")

    depends_on("mpi")
    depends_on("blas")
    depends_on("gsl", type=("build", "run", "link"))
    depends_on("eigen", type=("build", "run", "link"))
    depends_on("doxygen", type="build", when="+doc")
    depends_on("texlive", type="build", when="+doc")
    depends_on("py-cython", type=("build", "run"))
    depends_on("py-breathe", type="build", when="+doc")
    depends_on("py-sphinx", type="build", when="+doc")
    depends_on("py-sphinx-rtd-theme", type="build", when="+doc")

    depends_on("boost", type="link")
    depends_on("lcov", type=("build", "run"))
    depends_on("py-pytest", type=("build", "run"))
    depends_on("py-pytest-cov", type="run")
    depends_on("py-coverage@4.5.4", type="run")
    depends_on("py-packaging", type="run")
    depends_on("python", type=("build", "run"))

    test_requires_compiler = True

    def edit(self, spec, prefix):
        makefile = FileFilter(join_path("src", "makefile.gnu"))
        blas_libs = self.spec["blas"].libs
        makefile.filter("PROJECT_CC=.*", "PROJECT_CC={0}".format(spack_cxx))
        makefile.filter(
            "PROJECT_MPICC=.*", "PROJECT_MPICC={0}".format(self.spec["mpi"].mpicxx)
        )
        makefile.filter(
            "PROJECT_CFLAGS=.*", "PROJECT_CFLAGS={0}".format(self.compiler.cxx11_flag)
        )
        makefile.filter(
            "PROJECT_LDFLAGS_BLAS.*",
            "PROJECT_LDFLAGS_BLAS={0} -lgsl -lgslcblas".format(blas_libs.ld_flags),
        )

    def build(self, spec, prefix):
        with working_dir("src"):
            make()
            make("lammps-nnp")
            make("pynnp")
            if "+doc" in self.spec:
                make("doc")

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        if "+doc" in self.spec:
            install_tree("doc", prefix.doc)
        install_tree("examples", prefix.examples)
        install_tree("include", prefix.include)
        install_tree("lib", prefix.lib)
        install_tree("tools", prefix.tools)

    @run_after("install")
    def setup_build_tests(self):
        """Copy the build test files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources(".")

    def test(self):
        with working_dir(join_path(self.install_test_root, "test"), create=False):
            make("clean")

        with working_dir(join_path(self.install_test_root, "src"), create=False):
            make("clean")
            make(
                "MODE=test",
                "PROJECT_GSL={0}".format(self.spec["gsl"].prefix.include),
                "PROJECT_EIGEN={0}".format(self.spec["eigen"].prefix.include.eigen3),
            )
            make(
                "MODE=test",
                "lammps-nnp",
                "PROJECT_GSL={0}".format(self.spec["gsl"].prefix.include),
                "PROJECT_EIGEN={0}".format(self.spec["eigen"].prefix.include.eigen3),
            )
            make("pynnp", "MODE=test")

        with working_dir(join_path(self.install_test_root, "test"), create=False):
            if self.spec.satisfies("%fj"):
                f = FileFilter(join_path("cpp", "nnp_test.h"))
                f.filter(
                    "(example.co",
                    '("{0} -n 1 " + example.co'.format(
                        self.spec["mpi"].prefix.bin.mpirun
                    ),
                    string=True,
                )

            f = FileFilter(join_path("cpp", "makefile"))
            f.filter(
                "log_level=.*", "log_level=$(LOG_LEVEL) 2>&1 | tee -a ../output_cpp.txt"
            )

            f = FileFilter(join_path("python", "makefile"))
            f.filter("term\\s-v.*", "term -v | tee -a ../output_python.txt")

            make("cpp", parallel=False)
            make("python", parallel=False)

            test_dir = self.test_suite.current_test_data_dir
            expected_file = join_path(
                test_dir, "expected-result-{0}.txt".format(self.version)
            )
            check_n2p2 = Executable(join_path(test_dir, "result-check.sh"))
            check_n2p2("./output_cpp.txt", "./output_python.txt", expected_file)
