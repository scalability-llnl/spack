# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Graphblast(MakefilePackage, CudaPackage):
    """High-Performance Linear Algebra-based Graph Primitives on GPUs"""

    homepage = "https://github.com/gunrock/graphblast"
    git = "https://github.com/gunrock/graphblast.git"

    license("Apache-2.0")

    version("master", submodules=True)
    version(
        "2020-05-07",
        submodules=True,
        commit="1a052558a71f2cd67f5d6fe9db3b274c303ef8f6",
        preferred=True,
    )

    depends_on("cxx", type="build")  # generated

    variant("cuda", default=True, description="Build with Cuda support")

    depends_on("boost +program_options")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)

    # This package is confirmed to compile with:
    #   gcc@:5.4.0,7.5.0 , boost@1.58.0:1.60.0 , cuda@9:

    # TODO: the package doesn't compile as CMakePackage
    # once that is fixed it should be converted to a CMakePackage type.

    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg='Must specify CUDA compute capabilities of your GPU. \
See "spack info graphblast"',
    )

    def install(self, spec, prefix):
        install_tree(self.build_directory, self.prefix)

    def patch(self):
        cuda_arch_list = self.spec.variants["cuda_arch"].value
        arches = "ARCH = "
        for i in cuda_arch_list:
            arches = arches + " -gencode arch=compute_{0},code=compute_{0}".format(i)
        makefile = FileFilter("common.mk")
        makefile.filter(r"^ARCH =.*", arches)
