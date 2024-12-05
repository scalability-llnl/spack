# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pindel(MakefilePackage):
    """Pindel can detect breakpoints from next-gen sequence data."""

    homepage = "https://gmt.genome.wustl.edu/packages/pindel/"
    url = "https://github.com/genome/pindel/archive/v0.2.5.tar.gz"

    license("GPL-3.0-or-later")

    version("0.2.5b8", sha256="7f21fda0b751d420831724d96e60873ce332139cfd24396e81c7f1ae2f707a19")
    version("0.2.5b6", sha256="fe19aabdcf6334b9efe92d4509b80f0f266e621f1cc8db017b301d7e32e2eeac")
    version("0.2.5b5", sha256="2ebe9d959d8c3862d9103d8a3768265dcc79eab547035857dca8ab8cfe2544e4")
    version("0.2.5b4", sha256="0f6afd6b83f6cceb31be5dbb686c6ff518c54135274931097a8b83b3f5d0372a")
    version("0.2.5b1", sha256="b626e23ddfb3590174cfe38458b537e96707eedc6c2b054504f72ca141ba306c")
    version("0.2.5a7", sha256="0a270483dee9ef617d422eb61d3478334ee8f55e952d0a439529c2b21fcf8fb4")
    version("0.2.5", sha256="9908940d090eff23d940c3b6f2f6b3fc2bb1fd3b7a2d553cc81eed240a23fd9f")

    depends_on("cxx", type="build")  # generated

    depends_on("htslib@1.7:")

    # GCC > 4.8 seems to dislike calling abs on an unsigned integer
    # replace ambiguous calls to abs() on the difference between two
    # unsigned ints with a one line funtion that returns the 'absolute
    # value' of the difference between two unsigned ints.
    patch("gcc-5-compat.patch", when="@0.2.5b8%gcc@5:")

    build_directory = "src"

    def edit(self, spec, prefix):
        filter_file("include ../Makefile.local", "", "src/Makefile")
        filter_file("Makefile.local", "", "src/Makefile")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("src/pindel", prefix.bin)
        install("src/pindel2vcf", prefix.bin)
        install("src/sam2pindel", prefix.bin)
        install("src/pindel2vcf4tcga", prefix.bin)
        install_tree("demo", prefix.doc)
