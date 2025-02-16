# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNloptr(RPackage):
    """R Interface to NLopt.

    Solve optimization problems using an R interface to NLopt. NLopt is a
    free/open-source library for nonlinear optimization, providing a common
    interface for a number of different free optimization routines available
    online as well as original implementations of various other algorithms. See
    <https://nlopt.readthedocs.io/en/latest/NLopt_Algorithms/> for more
    information on the available algorithms. Building from included sources
    requires 'CMake'. On Linux and 'macOS', if a suitable system build of
    NLopt (2.7.0 or later) is found, it is used; otherwise, it is built  from
    included sources via 'CMake'. On Windows, NLopt is obtained through
    'rwinlib' for 'R <= 4.1.x' or grabbed from the 'Rtools42 toolchain' for  'R
    >= 4.2.0'."""

    cran = "nloptr"

    license("LGPL-3.0-or-later")

    version("2.1.1", sha256="4cdaf55dfdeb090119f2c2ca77f617962524654da4511bacd650f62bb6dad8ea")
    version("2.0.3", sha256="7b26ac1246fd1bd890817b0c3a145456c11aec98458b8518de863650b99616d7")
    version("2.0.0", sha256="65ca3149cfc9ba15ac10a91f34b5d86b20f5fd693f44e3edf3e392402911619a")
    version("1.2.2.3", sha256="af08b74fd5e7b4cb455fe67ed759346cbb8f3b9a4178f5f117e0092e5c9af6ff")
    version("1.2.2.2", sha256="e80ea9619ac18f4bfe44812198b40b9ae5c0ddf3f9cc91778f9ccc82168d1372")
    version("1.2.1", sha256="1f86e33ecde6c3b0d2098c47591a9cd0fa41fb973ebf5145859677492730df97")
    version("1.0.4", sha256="84225b993cb1ef7854edda9629858662cc8592b0d1344baadea4177486ece1eb")

    depends_on("r-testthat", when="@2.0.0:2.1.0")
    depends_on("nlopt@2.4.0:")
    depends_on("nlopt@2.7.0:", when="@2.0.0:")

    def configure_args(self):
        include_flags = self.spec["nlopt"].headers.include_flags
        libs = self.spec["nlopt"].libs.libraries[0]
        args = [
            "--with-nlopt-cflags={0}".format(include_flags),
            "--with-nlopt-libs={0}".format(libs),
        ]
        return args
