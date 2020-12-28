# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJplephem(PythonPackage):
    """This package can load and use a Jet Propulsion Laboratory (JPL)
    ephemeris for predicting the position and velocity of a planet or other
    Solar System body."""

    homepage = "https://pypi.org/project/jplephem/"
    url      = "https://pypi.io/packages/source/j/jplephem/jplephem-2.9.tar.gz"

    version('2.9', sha256='9dffb9f3d3f6d996ade875102431fe385e8ea422da25c8ba17b0508d9ca1282b')

    depends_on('py-numpy', type=('build', 'run'))
