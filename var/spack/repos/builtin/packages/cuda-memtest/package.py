# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CudaMemtest(CMakePackage):
    """Maintained and updated fork of cuda_memtest.

    original homepage: http://sourceforge.net/projects/cudagpumemtest .

    This software tests GPU memory for hardware errors and soft errors
    using CUDA or OpenCL.
    """

    homepage = "https://github.com/ComputationalRadiationPhysics/cuda_memtest"
    git = "https://github.com/ComputationalRadiationPhysics/cuda_memtest.git"

    maintainers("ax3l")

    license("Unlicense")

    version("master", branch="dev")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@2.8.5:", type="build")
    # depends_on('nvml', when='+nvml')
    depends_on("cuda@5.0:")
