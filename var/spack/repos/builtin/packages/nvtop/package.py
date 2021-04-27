# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Nvtop(CMakePackage, CudaPackage):
    """Nvtop stands for NVidia TOP, a (h)top like task monitor for NVIDIA GPUs.
    It can handle multiple GPUs and print information about them
    in a htop familiar way."""

    homepage = "https://github.com/Syllo/nvtop"
    url      = "https://github.com/Syllo/nvtop/archive/1.1.0.tar.gz"

    version('1.1.0', sha256='00470cde8fc48d5a5ed7c96402607e474414d94b562b21189bdde1dbe6b1d1f3')

    depends_on('ncurses')

    def cmake_args(self):
        return [self.define('NVML_RETRIEVE_HEADER_ONLINE', True)]
