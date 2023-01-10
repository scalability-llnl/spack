# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from pathlib import PurePath

import spack.compilers.xl


class XlR(spack.compilers.xl.Xl):
    # Subclasses use possible names of C compiler
    cc_names = ["xlc_r"]

    # Subclasses use possible names of C++ compiler
    cxx_names = ["xlC_r", "xlc++_r"]

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ["xlf_r"]

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ["xlf90_r", "xlf95_r", "xlf2003_r", "xlf2008_r"]

    # Named wrapper links within build_env_path
    link_paths = {
        "cc": PurePath("xl_r", "xlc_r"),
        "cxx": PurePath("xl_r", "xlc++_r"),
        "f77": PurePath("xl_r", "xlf_r"),
        "fc": PurePath("xl_r", "xlf90_r"),
    }
