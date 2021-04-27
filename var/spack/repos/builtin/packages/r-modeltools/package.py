# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RModeltools(RPackage):
    """Tools and Classes for Statistical Models

    A collection of tools to deal with statistical models.  The functionality
    is experimental and the user interface is likely to change in the future.
    The documentation is rather terse, but packages `coin' and `party' have
    some working examples. However, if you find the implemented ideas
    interesting we would be very interested in a discussion of this proposal.
    Contributions are more than welcome!"""

    homepage = "https://cloud.r-project.org/package=modeltools"
    url      = "https://cloud.r-project.org/src/contrib/modeltools_0.2-21.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/modeltools"

    version('0.2-23', sha256='6b3e8d5af1a039db5c178498dbf354ed1c5627a8cea9229726644053443210ef')
    version('0.2-22', sha256='256a088fc80b0d9182f984f9bd3d6207fb7c1e743f72e2ecb480e6c1d4ac34e9')
    version('0.2-21', sha256='07b331475625674ab00e6ddfc479cbdbf0b22d5d237e8c25d83ddf3e0ad1cd7a')
