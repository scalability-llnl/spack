# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import llnl

import spack.compilers.mingw

class Mingww64(spack.compilers.gcc.Gcc):

    cc_names = ["mingw-w64-gcc"]
    cxx_names = ["mingw-w64-g++"]
    fc_names = ["mingw-w64-gfortran"]
    f77_names = ["mingw-w64-gfortran"]


    # Named wrapper links within build_env_path
    link_paths = {
        "cc": os.path.join("mingw-w64", "gcc"),
        "cxx": os.path.join("mingw-w64", "g++"),
        "f77": os.path.join("mingw-w64", "gfortran"),
        "fc": os.path.join("mingw-w64", "gfortran"),
    }


    @classmethod
    @llnl.util.lang.memoized
    def extract_version_from_output(cls, output):
        pass