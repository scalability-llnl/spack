# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NvptxTools(AutotoolsPackage):
    """nvptx-tools: A collection of tools for use with nvptx-none GCC
    toolchains. These tools are necessary when building a version
    of GCC that enables offloading of OpenMP/OpenACC code to NVIDIA
    GPUs."""

    homepage = "https://github.com/MentorEmbedded/nvptx-tools"
    git = "https://github.com/MentorEmbedded/nvptx-tools"

    version("2023-09-13", commit="c321f1a3573dd89a12e3291d690207685a34df6e")
    version("2021-05-21", commit="d0524fbdc86dfca068db5a21cc78ac255b335be5")
    version("2018-03-01", commit="5f6f343a302d620b0868edab376c00b15741e39e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("binutils")
    depends_on("cuda")

    def configure_args(self):
        cuda_dir = self.spec["cuda"].prefix

        config_args = [
            "--with-cuda-driver-include={0}".format(cuda_dir.include),
            "--with-cuda-driver-lib={0}".format(cuda_dir.lib64),
        ]

        return config_args
