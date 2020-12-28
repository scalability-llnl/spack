# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFasteners(PythonPackage):
    """A python package that provides useful locks."""

    homepage = "https://github.com/harlowja/fasteners"
    url      = "https://pypi.io/packages/source/f/fasteners/fasteners-0.14.1.tar.gz"

    version('0.14.1', sha256='427c76773fe036ddfa41e57d89086ea03111bbac57c55fc55f3006d027107e18')

    depends_on('py-setuptools',     type='build')
    depends_on('py-monotonic@0.1:', type=('build', 'run'))
    depends_on('py-six',            type=('build', 'run'))
