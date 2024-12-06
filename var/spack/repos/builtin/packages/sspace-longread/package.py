# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class SspaceLongread(Package):
    """SSPACE-LongRead is a stand-alone program for scaffolding pre-assembled
    contigs using long reads

    Note: A manual download is required for SSPACE-LongRead.
    Spack will search your current directory for the download file.
    Alternatively, add this file to a mirror so that Spack can find it.
    For instructions on how to set up a mirror, see
    https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://www.baseclear.com/genomics/bioinformatics/basetools/SSPACE-longread"
    manual_download = True

    version("1.1", md5="0bb5d8603d7ead4ff1596135a520cc26")

    depends_on("perl", type=("build", "run"))

    def url_for_version(self, version):
        return "file://{0}/40SSPACE-LongRead_v{1}.tar.gz".format(os.getcwd(), version.dashed)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("blasr", prefix.bin)
        install("SSPACE-LongRead.pl", prefix.bin)
