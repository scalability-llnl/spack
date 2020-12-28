# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Usearch(Package):
    """USEARCH is a unique sequence analysis tool with thousands of users
       world-wide.

       Note: A manual download is required for USEARCH.
       Spack will search your current directory for the download file.
       Alternatively, add this file to a mirror so that Spack can find it.
       For instructions on how to set up a mirror, see
       http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "http://www.drive5.com/usearch/"
    manual_download = True

    version('10.0.240', '05192b6d5e291530c190a19a3cc82b53', expand=False)

    def url_for_version(self, version):
        return "file://{0}/usearch{1}_i86linux32".format(os.getcwd(), version)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('usearch{0}_i86linux32'.format(self.version),
                prefix.bin.usearch)
        chmod = which('chmod')
        chmod('+x', prefix.bin.usearch)
