# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dlpack(Package):
    """DLPack is an RFC for common tensor and operator guidelines
    in deep learning systems."""

    homepage = "https://github.com/sjtuhpcc/dlpack"
    git      = "https://github.com/dmlc/dlpack.git"

    version('master', branch='master')

    def install(self, spec, prefix):
        install_tree('include', prefix.include)
