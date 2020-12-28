# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Units(AutotoolsPackage, GNUMirrorPackage):
    """GNU units converts between different systems of units"""

    homepage = "https://www.gnu.org/software/units/"
    gnu_mirror_path = "units/units-2.13.tar.gz"

    version('2.13', sha256='0ba5403111f8e5ea22be7d51ab74c8ccb576dc30ddfbf18a46cb51f9139790ab')

    depends_on('python', type=('build', 'run'))
