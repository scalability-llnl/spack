# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class NcbiRmblastn(AutotoolsPackage):
    """RMBlast search engine for NCBI"""

    homepage = "http://www.repeatmasker.org/RMBlast.html"
    url      = "ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.9.0/ncbi-blast-2.9.0+-src.tar.gz"

    version('2.11.0', sha256='d88e1858ae7ce553545a795a2120e657a799a6d334f2a07ef0330cc3e74e1954')
    version('2.9.0', sha256='a390cc2d7a09422759fc178db84de9def822cbe485916bbb2ec0d215dacdc257')

    # There is a corresponding gzipped patch file associated with each version.
    # According to the documentation, http://www.repeatmasker.org/RMBlast.html,
    # Download NCBI Blast+ and rmblast patch file:
    #   ncbi-blast-2.11.0+-src.tar.gz
    #   isb-2.11.0+-rmblast.patch.gz
    # The patch is downloaded and unzipped in the ncbi-rmblastn Spack package
    # directory to make it available for the patch directive.
    patch('isb-2.11.0+-rmblast.patch', when="@2.11.0")
    patch('isb-2.9.0+-rmblast-p1.patch', when="@2.9.0")

    configure_directory = 'c++'

    def url_for_version(self, version):
        url = "ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/{0}/ncbi-blast-{1}+-src.tar.gz"
        return url.format(version, version)

    def configure_args(self):
        args = [
            "--with-mt",
            "--without-debug",
            "--without-krb5",
            "--without-openssl",
            "--with-projects=scripts/projects/rmblastn/project.lst"]
        return args
