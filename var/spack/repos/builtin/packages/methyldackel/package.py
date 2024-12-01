# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Methyldackel(MakefilePackage):
    """MethylDackel (formerly named PileOMeth, which was a temporary name
    derived due to it using a PILEup to extract METHylation metrics) will
    process a coordinate-sorted and indexed BAM or CRAM file containing
    some form of BS-seq alignments and extract per-base methylation
    metrics from them.
    """

    homepage = "https://github.com/dpryan79/MethylDackel"
    url = "https://github.com/dpryan79/MethylDackel/archive/refs/tags/0.6.1.tar.gz"
    maintainers("snehring")

    license("MIT")

    version("0.6.1", sha256="eeb1da4c830bcd9f3e6663a764947d957c41337643069524a4b545812fcf4819")

    depends_on("c", type="build")  # generated

    depends_on("htslib@1.11:")
    depends_on("libbigwig")
    depends_on("curl")

    def edit(self, spec, prefix):
        filter_file(r"^prefix \?=.*$", "prefix = " + spec.prefix, "Makefile")
        filter_file(
            "$(LIBBIGWIG)",
            join_path(spec["libbigwig"].prefix.lib64, "libBigWig.a"),
            "Makefile",
            string=True,
        )
        filter_file(
            "-IlibBigWig",
            "-I" + spec["libbigwig"].prefix.include.libbigwig,
            "Makefile",
            string=True,
        )
