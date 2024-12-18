# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Mallocmc(CMakePackage):
    """mallocMC: Memory Allocator for Many Core Architectures.

    This project provides a framework for fast memory managers on
    many core accelerators. Currently, it supports NVIDIA GPUs of
    compute capability sm_20 or higher through the ScatterAlloc
    algorithm.

    mallocMC is header-only, but requires a few other C++ libraries
    to be available.
    """

    homepage = "https://github.com/ComputationalRadiationPhysics/mallocMC"
    url = "https://github.com/ComputationalRadiationPhysics/mallocMC/archive/2.2.0crp.tar.gz"
    git = "https://github.com/ComputationalRadiationPhysics/mallocMC.git"

    maintainers("ax3l")

    license("MIT")

    version("develop", branch="dev")
    version("master", branch="master")
    version("2.2.0crp", sha256="1b500ee7fcea45a67a81fc0e1c294b4b0c413cd1f76168522f35ade7d44be9b6")
    version("2.1.0crp", sha256="973c606624cf4e049518d0366d72fb164fa837ab0068c7a44df7e567b95ef9bf")
    version("2.0.1crp", sha256="85873355814be22310e22e214e4d8e9798aaab9001c19da8ec9dd29c04603e9e")
    version("2.0.0crp", sha256="1a6b5b4f9a890d4389703cb853868cc31a97457bfea3b62d6b3ae31e56d7bbd9")
    version("1.0.2crp", sha256="696c5bb7e90a75937a2479c40e7cfddcc876f8fc634dca04b61d132ab1243f12")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@2.8.12.2:", type="build")
    depends_on("boost@1.48.0:", type="link")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, type="link")
    depends_on("cuda@5.0:", type="link")
