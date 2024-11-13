# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Biobambam2(AutotoolsPackage):
    """Tools for early stage alignment file processing"""

    homepage = "https://gitlab.com/german.tischler/biobambam2"
    url = "https://gitlab.com/german.tischler/biobambam2/-/archive/2.0.177-release-20201112105453/biobambam2-2.0.177-release-20201112105453.tar.gz"

    version(
        "2.0.177",
        sha256="ad0a418fb49a31996a105a1a275c0d1dfc8b84aa91d48fa1efb6ff4fe1e74181",
        url="https://gitlab.com/german.tischler/biobambam2/-/archive/2.0.177-release-20201112105453/biobambam2-2.0.177-release-20201112105453.tar.gz",
    )

    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("libmaus2")

    test_src_dir = "test"

    def configure_args(self):
        args = [f"--with-libmaus2={self.spec['libmaus2'].prefix}"]
        return args

    @run_after("install")
    def cache_test_sources(self):
        """Copy the test source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, self.test_src_dir)

        # Fix test scripts to run installed binaries
        scripts_dir = join_path(install_test_root(self), self.test_src_dir)
        for path in os.listdir(scripts_dir):
            if path.endswith(".sh"):
                filter_file(r"../src/", r"", join_path(scripts_dir, path))

    def test_short_sort(self):
        """run testshortsort.sh to check alignments sorted by coordinate"""
        test_dir = join_path(self.test_suite.current_test_cache_dir, self.test_src_dir)
        with working_dir(test_dir):
            sh = which("sh")
            out = sh("testshortsort.sh", output=str.split, error=str.split)
            assert "Alignments sorted by coordinate." in out
