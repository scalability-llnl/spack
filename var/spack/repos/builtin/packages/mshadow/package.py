# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mshadow(Package):
    """MShadow is a lightweight CPU/GPU Matrix/Tensor C++ Template Library.
    in C++/CUDA."""

    homepage = "https://github.com/dmlc/mshadow"
    git      = "https://github.com/dmlc/mshadow.git"

    version('master', branch='master')
    version('20170721', commit='20b54f068c1035f0319fa5e5bbfb129c450a5256')

    def install(self, spec, prefix):
        install_tree('mshadow', prefix.include.mshadow)
        install_tree('make', prefix.make)
