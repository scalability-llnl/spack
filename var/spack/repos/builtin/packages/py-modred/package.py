# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyModred(PythonPackage):
    """Modred is a parallelized library for finding
    modal decompositions and reduced-order models.
    """
    homepage = "http://github.com/belson17/modred"
    git      = "https://github.com/belson17/modred.git"

    version('2.0.4', tag='v2.0.4')
    version('2.0.3', tag='v2.0.3')
    version('2.0.2', tag='v2.0.2')
    version('2.0.1', tag='v2.0.1')
    version('2.0.0', tag='v2.0.0')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type='run')

    patch('v2x-setuptools-8.0.patch', when='@2: ^py-setuptools@8.0:')
