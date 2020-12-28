# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import chmod

from spack.package import *


class Tbl2asn(Package):
    """Tbl2asn is a command-line program that automates the creation of
       sequence records for submission to GenBank."""

    homepage = "https://www.ncbi.nlm.nih.gov/genbank/tbl2asn2/"

    version('2020-03-01', sha256='7cc1119d3cfcbbffdbd4ecf33cef8bbdd44fc5625c72976bee08b1157625377e')

    def url_for_version(self, ver):
        return "https://ftp.ncbi.nih.gov/toolbox/ncbi_tools/converters/by_program/tbl2asn/linux.tbl2asn.gz"

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('../linux.tbl2asn', prefix.bin.tbl2asn)
        chmod(prefix.bin.tbl2asn, 0o775)
