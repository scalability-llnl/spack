# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rodinia(MakefilePackage, CudaPackage):
    """Rodinia: Accelerating Compute-Intensive Applications with
    Accelerators"""

    homepage = "https://rodinia.cs.virginia.edu/doku.php"
    url = "https://www.cs.virginia.edu/~kw5na/lava/Rodinia/Packages/Current/rodinia_3.1.tar.bz2"

    version("3.1", sha256="faebac7c11ed8f8fcf6bf2d7e85c3086fc2d11f72204d6dfc28dc5b2e8f2acfd")

    depends_on("cuda")
    depends_on("freeglut")
    depends_on("glew")
    depends_on("gl")
    depends_on("glu")

    conflicts("~cuda")

    build_targets = ["CUDA"]

    def edit(self, spec, prefix):
        # set cuda paths
        filter_file(
            "CUDA_DIR = /usr/local/cuda",
            "CUDA_DIR = {0}".format(self.spec["cuda"].prefix),
            "common/make.config",
            string=True,
        )

        filter_file(
            "SDK_DIR = /usr/local/cuda-5.5/samples/",
            "SDK_DIR = {0}/samples".format(self.spec["cuda"].prefix),
            "common/make.config",
            string=True,
        )

        # set cuda arch flags in various makefiles
        filter_file(
            "compute_20",
            "compute_{0}".format(spec.variants["cuda_arch"].value[0]),
            "cuda/cfd/Makefile",
            string=True,
        )

        makefiles = [
            "cuda/lavaMD/makefile",
            "cuda/particlefilter/Makefile",
            "cuda/hybridsort/Makefile",
            "cuda/dwt2d/Makefile",
            "cuda/hotspot3D/Makefile",
            "cuda/b+tree/Makefile",
        ]

        for makefile in makefiles:
            filter_file(
                "sm_[0-9]+", "sm_{0}".format(spec.variants["cuda_arch"].value[0]), makefile
            )

        # fix broken makefile rule
        filter_file("%.o: %.[ch]", "%.o: %.c", "cuda/kmeans/Makefile", string=True)

        # fix missing include for lseek(), read()
        filter_file(
            "#include <stdint.h>",
            "#include <stdint.h>\n#include <unistd.h>",
            "cuda/mummergpu/src/suffix-tree.cpp",
            string=True,
        )

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install_tree("bin/linux/cuda", prefix.bin)
