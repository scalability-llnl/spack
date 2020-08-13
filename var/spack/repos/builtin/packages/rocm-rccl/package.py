# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RocmRccl(CMakePackage):
    """RCCL (pronounced "Rickle") is a stand-alone library of standard
    collective communication routines for GPUs, implementing
    all-reduce, all-gather, reduce, broadcast, reduce-scatter, gather,
    scatter, and all-to-all. There is also initial support for direct
    GPU-to-GPU send and receive operations. It has been optimized to
    achieve high bandwidth on platforms using PCIe, xGMI as well as
    networking using InfiniBand Verbs or TCP/IP sockets. RCCL supports
    an arbitrary number of GPUs installed in a single node or multiple
    nodes, and can be used in either single- or multi-process (e.g.,
    MPI) applications."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rccl"
    url = "https://github.com/ROCmSoftwarePlatform/rccl/archive/rocm-3.5.0.tar.gz"

    version('3.5.0', '290b57a66758dce47d0bfff3f5f8317df24764e858af67f60ddcdcadb9337253')
    depends_on('rocm-hip')
    depends_on('rocm-cmake')

    def cmake_args(self):
        cmake_args = [
            "-DCMAKE_CXX_COMPILER=hipcc",
        ]
        return cmake_args
