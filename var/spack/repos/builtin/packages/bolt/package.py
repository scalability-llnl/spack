# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Bolt(CMakePackage):
    """BOLT targets a high-performing OpenMP implementation,
    especially specialized for fine-grain parallelism. Unlike other
    OpenMP implementations, BOLT utilizes a lightweight threading
    model for its underlying threading mechanism. It currently adopts
    Argobots, a new holistic, low-level threading and tasking runtime,
    in order to overcome shortcomings of conventional OS-level
    threads. The current BOLT implementation is based on the OpenMP
    runtime in LLVM, and thus it can be used with LLVM/Clang, Intel
    OpenMP compiler, and GCC."""

    homepage = "https://www.bolt-omp.org/"
    url = "https://github.com/pmodels/bolt/releases/download/v1.0b1/bolt-1.0b1.tar.gz"
    git = "https://github.com/pmodels/bolt.git"
    maintainers("shintaro-iwasaki")

    test_requires_compiler = True

    tags = ["e4s"]

    license("LGPL-2.1-or-later")

    version("main", branch="main")
    version("2.0", sha256="f84b6a525953edbaa5d28748ef3ab172a3b6f6899b07092065ba7d1ccc6eb5ac")
    version("1.0.1", sha256="769e30dfc4042cee7ebbdadd23cf08796c03bcd8b335f516dc8cbc3f8adfa597")
    version("1.0", sha256="1c0d2f75597485ca36335d313a73736594e75c8a36123c5a6f54d01b5ba5c384")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("argobots")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    def cmake_args(self):
        spec = self.spec
        options = [
            "-DLIBOMP_USE_ARGOBOTS=on",
            "-DLIBOMP_ARGOBOTS_INSTALL_DIR=" + spec["argobots"].prefix,
        ]

        return options

    @run_after("install")
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, ["examples"])

    def test_sample_nested_example(self):
        """build and run sample_nested"""

        exe = "sample_nested"
        source_file = "{0}.c".format(exe)

        path = find_required_file(
            self.test_suite.current_test_cache_dir, source_file, expected=1, recursive=True
        )

        test_dir = os.path.dirname(path)
        with working_dir(test_dir):
            cxx = which(os.environ["CXX"])
            cxx(
                "-L{0}".format(self.prefix.lib),
                "-I{0}".format(self.prefix.include),
                "{0}".format(join_path(test_dir, source_file)),
                "-o",
                exe,
                "-lomp",
                "-lbolt",
            )

            sample_nested = which(exe)
            sample_nested()
