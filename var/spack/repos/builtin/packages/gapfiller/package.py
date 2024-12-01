# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class Gapfiller(Package):
    """GapFiller is a stand-alone program for closing gaps within
    pre-assembled scaffolds.

    Note: A manual download is required for GapFiller.
    Spack will search your current directory for the download file.
    Alternatively, add this file to a mirror so that Spack can find it.
    For instructions on how to set up a mirror, see
    https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://www.baseclear.com/genomics/bioinformatics/basetools/gapfiller"
    manual_download = True

    version("1.10", md5="54d5e2ada131a1305a66e41c0d380382")

    def url_for_version(self, version):
        return "file://{0}/39GapFiller_v{1}_linux-x86_64.tar.gz".format(
            os.getcwd(), version.dashed
        )

    depends_on("perl+threads", type=("build", "run"))

    def patch(self):
        with working_dir("."):
            files = glob.glob("*.pl") + glob.glob("bwa/*.pl")
            for file in files:
                change = FileFilter(file)
                change.filter("usr/bin/perl", "usr/bin/env perl")
                change.filter('require "getopts.pl";', "use Getopt::Std;")
                change.filter("&Getopts", "getopts")
                change.filter("\r", "")
                set_executable(file)

    def install(self, spec, prefix):
        install_tree("bowtie", prefix.bin.bowtie)
        install_tree("bwa", prefix.bin.bwa)
        install("GapFiller.pl", prefix.bin)
