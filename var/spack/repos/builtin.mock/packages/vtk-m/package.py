# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class VtkM(CMakePackage):
    """This is a fake vtk-m package used to demonstrate virtual package providers
    with dependencies."""

    homepage = "http://www.spack-fake-vtk-m.org"
    url = "http://www.spack-fake-vtk-m.org/downloads/vtk-m-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    variant("cuda", default=False, description="Build with CUDA")
    variant(
        "cuda_arch",
        description="CUDA architecture",
        default="none",
        values=("70", "none"),
        multi=False,
        when="+cuda",
    )

    variant("rocm", default=False, description="Enable ROCm support")
    variant(
        "amdgpu_target",
        default="none",
        description="AMD GPU architecture",
        values=("gfx900", "none"),
        multi=False,
        when="+rocm",
    )
    depends_on("cmake@3.18:")
