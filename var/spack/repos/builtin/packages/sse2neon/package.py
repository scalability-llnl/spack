# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Sse2neon(Package):
    """A C/C++ header file that converts Intel SSE intrinsics to ARN NEON
    intrinsics."""

    homepage = "https://github.com/jratcliff63367/sse2neon"
    git      = "https://github.com/jratcliff63367/sse2neon.git"

    version('master', branch='master')

    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install('*.h', prefix.include)
