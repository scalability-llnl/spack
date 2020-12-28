# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNloptr(RPackage):
    """nloptr is an R interface to NLopt. NLopt is a free/open-source
    library for nonlinear optimization, providing a common interface
    for a number of different free optimization routines available
    online as well as original implementations of various other
    algorithms. See http://ab-initio.mit.edu/wiki/index.php/NLopt
    _Introduction for more information on the available algorithms.
    During installation on Unix the NLopt code is downloaded and
    compiled from the NLopt website."""

    homepage = "https://cloud.r-project.org/package=nloptr"
    url      = "https://cloud.r-project.org/src/contrib/nloptr_1.0.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/nloptr"

    version('1.2.1', sha256='1f86e33ecde6c3b0d2098c47591a9cd0fa41fb973ebf5145859677492730df97')
    version('1.0.4', sha256='84225b993cb1ef7854edda9629858662cc8592b0d1344baadea4177486ece1eb')

    depends_on('nlopt')

    def configure_args(self):
        include_flags = self.spec['nlopt'].headers.include_flags
        libs = self.spec['nlopt'].libs.libraries[0]
        args = [
            '--with-nlopt-cflags={0}'.format(include_flags),
            '--with-nlopt-libs={0}'.format(libs)
        ]
        return args
