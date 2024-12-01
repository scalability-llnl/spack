# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tbl2asn(Package):
    """Tbl2asn is a command-line program that automates the creation of
    sequence records for submission to GenBank."""

    homepage = "https://www.ncbi.nlm.nih.gov/genbank/tbl2asn2/"
    maintainers("snehring")

    version(
        "2022-04-26", sha256="c76481700e196ebd98a83f4174e0146569db9d6fe5753ac18691e9836d5c6a75"
    )
    version(
        "2020-03-01",
        sha256="7cc1119d3cfcbbffdbd4ecf33cef8bbdd44fc5625c72976bee08b1157625377e",
        deprecated=True,
    )

    depends_on("libidn@1.34", type="run")

    def url_for_version(self, ver):
        return "https://ftp.ncbi.nih.gov/toolbox/ncbi_tools/converters/by_program/tbl2asn/linux64.tbl2asn.gz"

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        if spec.satisfies("@2020-03-01"):
            install("../linux.tbl2asn", prefix.bin.tbl2asn)
        else:
            install("linux64.tbl2asn", prefix.bin.tbl2asn)
        set_executable(prefix.bin.tbl2asn)
