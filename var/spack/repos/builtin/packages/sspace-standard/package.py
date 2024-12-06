# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class SspaceStandard(Package):
    """SSPACE standard is a stand-alone program for scaffolding pre-assembled
    contigs using NGS paired-read data

    Note: A manual download is required for SSPACE-Standard.
    Spack will search your current directory for the download file.
    Alternatively, add this file to a mirror so that Spack can find it.
    For instructions on how to set up a mirror, see
    https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://www.baseclear.com/genomics/bioinformatics/basetools/SSPACE"
    url = "file://{0}/41SSPACE-STANDARD-3.0_linux-x86_64.tar.gz".format(os.getcwd())
    manual_download = True

    version("3.0", md5="7e171b4861b9d514e80aafc3d9cdf554")

    depends_on("perl+threads", type=("build", "run"))
    depends_on("perl-perl4-corelibs", type=("build", "run"))

    def install(self, spec, prefix):
        rootscript = "SSPACE_Standard_v{0}.pl".format(self.version)

        scripts = [rootscript]
        scripts.extend(glob.glob("tools/*.pl"))
        scripts.extend(glob.glob("bwa/*.pl"))

        for s in scripts:
            filter_file("/usr/bin/perl", "/usr/bin/env perl", s, string=True)
            filter_file('require "getopts.pl";', "use Getopt::Std;", s, string=True)
            filter_file("&Getopts(", "getopts(", s, string=True)

        install_tree("bin", prefix.bin)
        install_tree("bowtie", prefix.bowtie)
        install_tree("bwa", prefix.bwa)
        install_tree("dotlib", prefix.dotlib)
        install_tree("tools", prefix.tools)
        install(rootscript, prefix)

    def setup_run_environment(self, env):
        env.set("SSPACE_HOME", self.prefix)
        env.prepend_path("PATH", self.prefix)
