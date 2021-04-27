# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Sse2neon(Package):
    """A C/C++ header file that converts Intel SSE intrinsics to Arm/Aarch64
    NEON intrinsics."""

    homepage = "https://github.com/DLTcollab/sse2neon"
    git      = "https://github.com/DLTcollab/sse2neon.git"

    version('master', branch='master')

    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install('*.h', prefix.include)
