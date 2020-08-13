# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RocmDeviceLibs(CMakePackage):
    """This repository contains the sources and CMake build system for
    a set of AMD specific device-side language runtime libraries."""

    homepage = "https://github.com/RadeonOpenCompute/ROCm-Device-Libs"
    url = "https://github.com/RadeonOpenCompute/ROCm-Device-Libs/archive/rocm-3.5.0.tar.gz"

    version('3.5.0', 'dce3a4ba672c4a2da4c2260ee4dc96ff6dd51877f5e7e1993cb107372a35a378')
    depends_on('rocm-hip-clang')
    depends_on('rocm-rocr-runtime')
