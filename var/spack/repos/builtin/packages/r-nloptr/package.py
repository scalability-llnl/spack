# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RNloptr(RPackage):
    """R Interface to NLopt

    Solve optimization problems using an R interface to NLopt. NLopt is a
    free/open-source library for nonlinear optimization, providing a common
    interface for a number of different free optimization routines available
    online as well as original implementations of various other algorithms. See
    <http://ab-initio.mit.edu/wiki/index.php/NLopt_Introduction> for more
    information on the available algorithms. During installation of nloptr on
    Unix-based systems, the installer checks whether the NLopt library is
    installed on the system. If the NLopt library cannot be found, the code is
    compiled using the NLopt source included in the nloptr package."""

    homepage = "https://cloud.r-project.org/package=nloptr"
    url      = "https://cloud.r-project.org/src/contrib/nloptr_1.0.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/nloptr"

    version('1.2.2.2', sha256='e80ea9619ac18f4bfe44812198b40b9ae5c0ddf3f9cc91778f9ccc82168d1372')
    version('1.2.1', sha256='1f86e33ecde6c3b0d2098c47591a9cd0fa41fb973ebf5145859677492730df97')
    version('1.0.4', sha256='84225b993cb1ef7854edda9629858662cc8592b0d1344baadea4177486ece1eb')

    depends_on('nlopt@2.4.0:')

    def configure_args(self):
        include_flags = self.spec['nlopt'].headers.include_flags
        libs = self.spec['nlopt'].libs.libraries[0]
        args = [
            '--with-nlopt-cflags={0}'.format(include_flags),
            '--with-nlopt-libs={0}'.format(libs)
        ]
        return args
