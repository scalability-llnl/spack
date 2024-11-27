# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.compilers.xl


class XlR(spack.compilers.xl.Xl):
    # Named wrapper links within build_env_path
    link_paths = {
        "cc": os.path.join("xl_r", "xlc_r"),
        "cxx": os.path.join("xl_r", "xlc++_r"),
        "f77": os.path.join("xl_r", "xlf_r"),
        "fc": os.path.join("xl_r", "xlf90_r"),
    }
