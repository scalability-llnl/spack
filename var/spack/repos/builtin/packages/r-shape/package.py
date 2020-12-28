# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RShape(RPackage):
    """Functions for plotting graphical shapes such as ellipses, circles,
       cylinders, arrows, ..."""

    homepage = "https://cloud.r-project.org/package=shape"
    url      = "https://cloud.r-project.org/src/contrib/shape_1.4.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/shape"

    version('1.4.4', sha256='f4cb1b7d7c84cf08d2fa97f712ea7eb53ed5fa16e5c7293b820bceabea984d41')
    version('1.4.3', sha256='720f6ca9c70a39a3900af9d074bff864b18ac58013b21d48b779047481b93ded')
    version('1.4.2', sha256='c6c08ba9cc2e90e5c9d3d5223529b57061a041f637886ad7665b9fa27465637a')

    depends_on('r@2.0.1:', type=('build', 'run'))
