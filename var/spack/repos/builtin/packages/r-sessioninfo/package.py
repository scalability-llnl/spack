# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSessioninfo(RPackage):
    """Query and print information about the current R session. It is similar
    to 'utils::sessionInfo()', but includes more information about packages,
    and where they were installed from."""

    homepage = "https://github.com/r-lib/sessioninfo#readme"
    url      = "https://cloud.r-project.org/src/contrib/sessioninfo_1.1.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/sessioninfo"

    version('1.1.1', sha256='166b04678448a7decd50f24afabe5e2ad613e3c55b180ef6e8dd7a870a1dae48')

    depends_on('r-cli', type=('build', 'run'))
    depends_on('r-withr', type=('build', 'run'))
