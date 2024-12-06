# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Mpi(Package):
    """Virtual package for the Message Passing Interface."""

    homepage = "https://www.mpi-forum.org/"
    virtual = True

    def test_mpi_hello(self):
        """build and run mpi hello world"""
        for lang in ("c", "f"):
            filename = self.test_suite.current_test_data_dir.join("mpi_hello." + lang)

            compiler_var = "MPICC" if lang == "c" else "MPIF90"
            compiler = which(os.environ[compiler_var])
            mpirun = which(self.prefix.bin.mpirun)

            exe_name = "mpi_hello_%s" % lang

            with test_part(self, f"test_mpi_hello_{lang}", purpose=f"build and run {filename}"):
                compiler("-o", exe_name, filename)
                out = mpirun("-np", "1", exe_name, output=str.split, error=str.split)
                expected = [r"Hello world! From rank \s*0 of \s*1"]
                check_outputs(expected, out)
