# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class GpuBurn(MakefilePackage, CudaPackage):
    """Multi-GPU CUDA stress test."""

    homepage = "http://wili.cc/blog/gpu-burn.html"
    url = "http://wili.cc/blog/entries/gpu-burn/gpu_burn-1.0.tar.gz"
    git = "https://github.com/wilicc/gpu-burn"

    version("master", branch="master")
    version("1.1", sha256="9876dbf7ab17b3072e9bc657034ab39bdedb219478f57c4e93314c78ae2d6376")
    version("1.0", sha256="d55994f0bee8dabf021966dbe574ef52be1e43386faeee91318dd4ebb36aa74a")

    depends_on("cxx", type="build")  # generated

    # This package uses CudaPackage to pick up the cuda_arch variant. A side
    # effect is that it also picks up the cuda variant, but cuda is required
    # for gpu-burn so is not really a variant.
    variant("cuda", default=True, description="Use CUDA; must be true")

    conflicts("~cuda", msg="gpu-burn requires cuda")
    conflicts("cuda_arch=none", msg="must select a CUDA architecture")

    def edit(self, spec, prefix):
        # update cuda architecture if necessary
        if self.spec.satisfies("+cuda"):
            cuda_arch = self.spec.variants["cuda_arch"].value
            archflag = " ".join(CudaPackage.cuda_flags(cuda_arch))
            with open("Makefile", "w") as fh:
                fh.write("drv:\n")
                fh.write("\tnvcc {0} -fatbin " "compare.cu -o compare.ptx\n".format(archflag))
                fh.write("\t{0} -O3 -c gpu_burn-drv.cpp\n".format(spack_cxx))
                fh.write(
                    "\t{0} -o gpu_burn gpu_burn-drv.o -O3 -lcuda "
                    "-lcublas -lcudart -o gpu_burn\n".format(spack_cxx)
                )

            filter_file(
                "compare.ptx",
                join_path(prefix.share, "compare.ptx"),
                "gpu_burn-drv.cpp",
                string=True,
            )

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.share)
        install("gpu_burn", prefix.bin)
        install("compare.ptx", prefix.share)
