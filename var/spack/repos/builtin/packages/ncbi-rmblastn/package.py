# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NcbiRmblastn(AutotoolsPackage):
    """RMBlast search engine for NCBI"""

    homepage = "http://www.repeatmasker.org/RMBlast.html"
    url      = "ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.9.0/ncbi-blast-2.9.0+-src.tar.gz"

    version('2.9.0', sha256='a390cc2d7a09422759fc178db84de9def822cbe485916bbb2ec0d215dacdc257')
    patch('isb-2.9.0+-rmblast-p1.patch', when="@2.9.0")

    configure_directory = 'c++'

    def configure_args(self):
        args = [
            "--with-mt",
            "--without-debug",
            "--without-krb5",
            "--without-openssl",
            "--with-projects=scripts/projects/rmblastn/project.lst"]
        return args
