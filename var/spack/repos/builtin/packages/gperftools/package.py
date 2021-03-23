# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gperftools(AutotoolsPackage):
    """Google's fast malloc/free implementation, especially for
       multi-threaded applications.  Contains tcmalloc, heap-checker,
       heap-profiler, and cpu-profiler.

    """
    homepage = "https://github.com/gperftools/gperftools"
    url      = "https://github.com/gperftools/gperftools/releases/download/gperftools-2.7/gperftools-2.7.tar.gz"

    version('2.8.1', sha256='12f07a8ba447f12a3ae15e6e3a6ad74de35163b787c0c7b76288d7395f2f74e0')
    version('2.7', sha256='1ee8c8699a0eff6b6a203e59b43330536b22bbcbe6448f54c7091e5efb0763c9')
    version('2.4', sha256='982a37226eb42f40714e26b8076815d5ea677a422fb52ff8bfca3704d9c30a2d')
    version('2.3', sha256='093452ad45d639093c144b4ec732a3417e8ee1f3744f2b0f8d45c996223385ce')

    depends_on("unwind")
