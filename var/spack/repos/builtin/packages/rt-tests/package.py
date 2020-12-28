# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RtTests(MakefilePackage):
    """
    Suite of real-time tests - cyclictest, hwlatdetect, pip_stress,
    pi_stress, pmqtest, ptsematest, rt-migrate-test, sendme, signaltest,
    sigwaittest, svsematest.
    """

    homepage = "https://git.kernel.org"
    url      = "https://git.kernel.org/pub/scm/utils/rt-tests/rt-tests.git/snapshot/rt-tests-1.2.tar.gz"

    version('1.2', sha256='7ccde036059c87681a4b00e7138678d9551b1232113441f6edda31ea45452426')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.share.man)
        make('install', 'prefix={0}'.format(prefix))
