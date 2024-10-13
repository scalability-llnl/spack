# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Papyrus(CMakePackage):
    """Parallel Aggregate Persistent Storage"""

    homepage = "https://code.ornl.gov/eck/papyrus"
    url = "https://code.ornl.gov/eck/papyrus/repository/archive.tar.bz2?ref=v1.0.2"
    git = "https://code.ornl.gov/eck/papyrus.git"

    tags = ["e4s"]

    license("BSD-3-Clause")

    version("master", branch="master")
    version("1.0.2", sha256="b6cfcff99f73ded8e4ca4b165bc182cd5cac60f0c0cf4f93649b77d074445645")
    version("1.0.1", sha256="3772fd6f2c301faf78f18c5e4dc3dbac57eb361861b091579609b3fff9e0bb17")
    version("1.0.0", sha256="5d57c0bcc80de48951e42460785783b882087a5714195599d773a6eabde5c4c4")

    depends_on("mpi")

    test_requires_compiler = True

    def setup_run_environment(self, env):
        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib

        env.prepend_path("CPATH", self.prefix.include)
        env.prepend_path("LIBRARY_PATH", lib_dir)
        env.prepend_path("LD_LIBRARY_PATH", lib_dir)

    @run_after("install")
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, join_path("kv", "tests"))

    @property
    def _lib_dir(self):
        """Path to the installed library root."""
        return self.prefix.lib64 if os.path.isdir(self.prefix.lib64) else self.prefix.lib

    def _build_and_run_kv_test(self, test):
        """build and run a kv/tests test"""

        test_dir = join_path(self.test_suite.current_test_cache_dir.kv.tests, test)
        if not os.path.exists(test_dir):
            raise SkipTest(f"Example directory ({test_dir}) is missing")

        with working_dir(test_dir):
            options = [
                f"test{test}.c",
                f"-I{self.prefix.include}",
                f"-L{self._lib_dir}",
                "-lpapyruskv",
                "-g",
                "-o",
                test,
                "-lpthread",
                "-lm",
            ]

            mpicxx = which(self.spec["mpi"].mpicxx)
            mpicxx(*options)

            mpirun = which(self.spec["mpi"].prefix.bin.mpirun)
            mpirun("-np", "4", test)

    def test_01_open_close(self):
        """build and run test01_open_close"""
        self._build_and_run_kv_test("01_open_close")

    def test_02_put_get(self):
        """build and run test02_put_get"""
        self._build_and_run_kv_test("02_put_get")

    def test_03_barrier(self):
        """build and run test03_barrier"""
        self._build_and_run_kv_test("03_barrier")

    def test_04_delete(self):
        """build and run test 04_delete"""
        self._build_and_run_kv_test("04_delete")

    def test_05_fence(self):
        """build and run test05_fence"""
        self._build_and_run_kv_test("05_fence")

    def test_06_signal(self):
        """build and run test06_signal"""
        self._build_and_run_kv_test("06_signal")

    def test_07_consistency(self):
        """build and run test07_consistency"""
        self._build_and_run_kv_test("07_consistency")

    def test_08_protect(self):
        """build and run test08_protect"""
        self._build_and_run_kv_test("08_protect")

    def test_09_cache(self):
        """build and run test09_cache"""
        self._build_and_run_kv_test("09_cache")

    def test_10_checkpoint(self):
        """build and run test10_checkpoint"""
        self._build_and_run_kv_test("10_checkpoint")

    def test_11_restart(self):
        """build and run test11_restart"""
        self._build_and_run_kv_test("11_restart")

    def test_12_free(self):
        """build and run test12_free"""
        self._build_and_run_kv_test("12_free")
