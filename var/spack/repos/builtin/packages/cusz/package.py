# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cusz(MakefilePackage):
    """cuSZ is a CUDA-based error-bounded lossy compressor for scientific
       data (floating point and integers).
    """

    homepage = "https://szcompressor.org"
    url      = "https://github.com/szcompressor/cuSZ/releases/download/v0.1.2/cuSZ-0.1.2.tar.gz"
    git      = "https://github.com/szcompressor/cuSZ"
    maintainers = ['dingwentao', 'jtian0']

    version('master', branch='master')
    version('0.1.2', sha256='c6e89a26b295724edefc8052f62653c5a315c78eaf6d5273299a8e11a5cf7363')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('bin/cusz', prefix.bin)
