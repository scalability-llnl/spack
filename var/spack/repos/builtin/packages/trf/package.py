# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Trf(Package):
    """Tandem Repeats Finder is a program to locate and display tandem repeats
       in DNA sequences.

       Note: A manual download is required for TRF.
       Spack will search your current directory for the download file.
       Alternatively, add this file to a mirror so that Spack can find it.
       For instructions on how to set up a mirror, see
       http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://tandem.bu.edu/trf/trf.html"
    manual_download = True

    version('4.09', '0c594fe666e0332db1df9d160d7fabc8', expand=False,
            url='file://{0}/trf409.linux64'.format(os.getcwd()))
    version('4.07b', sha256='a3a760c7b74c9603fbc08d95e8fa696c00f35a2f179b0bd63b2b13757ad3b471', expand=False,
            url='file://{0}/trf407b.linux64'.format(os.getcwd()))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        trfname = 'trf{0}.linux64'.format(self.version.joined)

        install(trfname, prefix.bin)
        chmod = which('chmod')
        chmod('+x', os.path.join(prefix.bin, trfname))
        os.symlink(trfname, prefix.bin.trf)
