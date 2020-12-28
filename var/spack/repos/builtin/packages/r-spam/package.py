# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpam(RPackage):
    """spam: SPArse Matrix"""

    homepage = "https://www.math.uzh.ch/pages/spam/"
    url      = "https://cloud.r-project.org/src/contrib/spam_2.3-0.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/spam"

    version('2.3-0.2', sha256='848fa95c0a71ac82af6344539af7b1c33563c687f06ead42851a68b621fff533')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-dotcall64', type=('build', 'run'))
