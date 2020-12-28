# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyBlessed(PythonPackage):
    """Blessed is a thin, practical wrapper around terminal capabilities in
    Python."""

    homepage = "https://github.com/jquast/blessed"
    url      = "https://pypi.io/packages/source/b/blessed/blessed-1.15.0.tar.gz"

    version('1.15.0', sha256='777b0b6b5ce51f3832e498c22bc6a093b6b5f99148c7cbf866d26e2dec51ef21')

    depends_on('py-setuptools', type='build')
    depends_on('py-wcwidth@0.1.4:', type=('build', 'run'))
    depends_on('py-six@1.9.0:', type=('build', 'run'))
