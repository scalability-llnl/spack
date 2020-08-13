# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RocmCompilersupport(CMakePackage):
    """The compiler support repository provides various Lightning
    Compiler related services. It currently contains one library, the
    Code Object Manager (Comgr) at lib/comgr."""

    homepage = "https://github.com/RadeonOpenCompute/ROCm-CompilerSupport"
    url = "https://github.com/RadeonOpenCompute/ROCm-CompilerSupport/archive/rocm-3.5.0.tar.gz"

    root_cmakelists_dir = 'lib/comgr'

    version('3.5.0', '25c963b46a82d76d55b2302e0e18aac8175362656a465549999ad13d07b689b9')
    depends_on('rocm-hip-clang')
    depends_on('rocm-device-libs')
