# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Miniamr(MakefilePackage):
    """Proxy Application. 3D stencil calculation with
    Adaptive Mesh Refinement (AMR)
    """

    homepage = "https://mantevo.org"
    git = "https://github.com/Mantevo/miniAMR.git"
    url = "https://github.com/Mantevo/miniAMR/archive/v1.4.0.tar.gz"

    tags = ["proxy-app", "ecp-proxy-app"]

    license("LGPL-3.0-only")

    version("master", branch="master")
    version("1.7.0", sha256="f11aee04bc59f46c6894a07d365c9c3006c58739ac6abd2d9663843c01a8b62b")
    version("1.6.6", sha256="a7f79fae49e433ef8350cbd34cbf57c486089cf7ac0d1f1f3b23c820d3e5bb9f")
    version("1.6.5", sha256="c70f0f648c73ea4497817ceee158334eeb901fc5c32cf804deef3226cd9cf26a")
    version("1.6.4", sha256="807d50608b69fb1a61924718964be96c0a2f9fa2e37fdc027bc3f0f116544732")
    version("1.4.4", sha256="b83f438ff351481b4310c46ddf63b9fffc7f29f916a5717377e72919a5b788b6")
    version("1.4.3", sha256="4c3fbc1662ae3e139669fb3844134486a7488a0b6e085c3b24bebcc8d12d3ac6")
    version("1.4.2", sha256="d2347e0e22a8e79aa0dc3316b67dd7c40dded39d82f6e068e6fb8c9f0766566b")
    version("1.4.1", sha256="dd8e8d9fd0768cb4f2c5d7fe6989dfa6bb95a8461f04deaccdbb50b0dd51e97a")
    version("1.4.0", sha256="f0b959c90416288c5ab51ed86b6ba49bc8a319006c2a74a070c94133267edc6f")

    depends_on("c", type="build")  # generated

    depends_on("mpi")

    @property
    def build_targets(self):
        targets = []
        targets.append(f"CC={self.spec['mpi'].mpicc}")
        targets.append(f"LD={self.spec['mpi'].mpicc}")
        targets.append("LDLIBS=-lm")
        targets.append("--directory=ref")

        return targets

    def install(self, spec, prefix):
        # Manual installation
        mkdir(prefix.bin)
        mkdir(prefix.docs)

        if spec.satisfies("@1.6.4:"):
            install("ref/miniAMR.x", prefix.bin)
        else:
            install("ref/ma.x", prefix.bin)
        # Install Support Documents
        install("ref/README", prefix.docs)
