# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Isaac(CMakePackage):
    """In Situ Animation of Accelerated Computations: Header-Only Library"""

    homepage = "https://computationalradiationphysics.github.io/isaac/"
    url = "https://github.com/ComputationalRadiationPhysics/isaac/archive/v1.3.0.tar.gz"
    git = "https://github.com/ComputationalRadiationPhysics/isaac.git"

    maintainers("ax3l")

    license("LGPL-3.0-only")

    version("develop", branch="dev")
    version("master", branch="master")
    version("1.5.2", sha256="9cedd72bea06f387b697b17a0db076e50fb3b85b74f21d3a6d99ed0d664a9ef2")
    version("1.5.1", sha256="f62d53aa6e1c28e51437dbf3d1ac0daa2f98d28660f09feaabcc953ff01b076e")
    version("1.5.0", sha256="4d5a150dfe064289d760da368102172f84e9e8851a177c8125a56e151db58dce")
    version("1.4.0", sha256="6cbd4cc54a22de5e5a3427e44141db6e7b80b33fe7a0c707390a113655bf344e")
    version("1.3.3", sha256="92a972d05d315ad66546671c047b7edf8ed0e05d64d2b8d77ababb5bb9b93d8e")
    version("1.3.2", sha256="e6eedc641de5b0a7c5ea5cda6b11e9b6d4a78dfac8be90302147b26d09859a68")
    version("1.3.1", sha256="7dead8f3d5467cbd2cde8187e7b860a4ab7796348895d18291f97a76e28757cf")
    version("1.3.0", sha256="fcf10f4738e7790ef6604e1e2cdd052a129ba4e53a439deaafa9fb2a70585574")

    depends_on("cxx", type="build")  # generated

    variant("cuda", default=True, description="Generate CUDA kernels for Nvidia GPUs")
    # variant('alpaka', default=False,
    #         description='Generate kernels via Alpaka, for CPUs or GPUs')

    depends_on("cmake@3.3:", type="build")
    depends_on("jpeg", type="link")
    depends_on("jansson", type="link")
    depends_on("boost@1.56.0:", type="link")
    depends_on("boost@1.65.1:", type="link", when="^cuda@9:")
    depends_on("cuda@7.0:", type="link", when="+cuda")
    # depends_on('alpaka@0.3', when='+alpaka')
    depends_on("icet", type="link")
    depends_on("mpi", type="link")

    root_cmakelists_dir = "lib"
