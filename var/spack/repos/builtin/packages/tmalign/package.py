# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tmalign(Package):
    """TM-align is an algorithm for sequence-order independent protein
       structure comparisons."""

    homepage = "http://zhanglab.ccmb.med.umich.edu/TM-align"
    url      = "http://zhanglab.ccmb.med.umich.edu/TM-align/TM-align-C/TMalignc.tar.gz"

    version('2016-05-25', sha256='ce7f68289f3766d525afb0a58e3acfc28ae05f538d152bd33d57f8708c60e2af')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('TMalign', prefix.bin)
