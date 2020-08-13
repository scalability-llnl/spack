# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RocmCmake(CMakePackage):
    """ROCM cmake modules provides cmake modules for common build
    tasks needed for the ROCM software stack."""

    homepage = "https://github.com/RadeonOpenCompute/rocm-cmake"
    url = "https://github.com/RadeonOpenCompute/rocm-cmake/archive/rocm-3.5.0.tar.gz"

    version('3.5.0', '5fc09e168879823160f5fdf4fd1ace2702d36545bf733e8005ed4ca18c3e910f')
