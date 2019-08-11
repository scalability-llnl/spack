# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RIrdisplay(RPackage):
    """An interface to the rich display capabilities of Jupyter front-ends
    (e.g. 'Jupyter Notebook') Designed to be used from a running IRkernel
    session"""

    homepage = "https://irkernel.github.io"
    url      = "https://cloud.r-project.org/src/contrib/IRdisplay_0.4.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/IRdisplay"

    version('0.7.0', sha256='91eac9acdb92ed0fdc58e5da284aa4bb957ada5eef504fd89bec136747999089')
    version('0.4.4', '5be672fb82185b90f23bd99ac1e1cdb6')

    depends_on('r-repr', type=('build', 'run'))
