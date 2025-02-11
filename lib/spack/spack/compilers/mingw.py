# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import re

from llnl.util.filesystem import ancestor

import spack.compiler


class Mingw(spack.compiler.Compiler):
    cc_names = ["gcc"]
    cxx_names = ["g++"]
    f77_names = ["gfortran"]
    fc_names = ["gfortran"]

    # Named wrapper links within build_env_path
    link_paths = {
        "cc": os.path.join("mingw", "gcc"),
        "cxx": os.path.join("mingw", "g++"),
        "f77": os.path.join("mingw", "gfortran"),
        "fc": os.path.join("mingw", "gfortran"),
    }


