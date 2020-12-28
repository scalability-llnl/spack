# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMonty(PythonPackage):
    """Monty is the missing complement to Python."""

    homepage = "https://github.com/materialsvirtuallab/monty"
    url      = "https://pypi.io/packages/source/m/monty/monty-0.9.6.tar.gz"

    version('0.9.6', sha256='bbf05646c4e86731c2398a57b1044add7487fc4ad03122578599ddd9a8892780')

    depends_on('py-setuptools', type='build')
    depends_on('py-six',        type=('build', 'run'))
