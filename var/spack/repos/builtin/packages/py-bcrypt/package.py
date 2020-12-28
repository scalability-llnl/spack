# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBcrypt(PythonPackage):
    """Modern password hashing for your software and your servers"""

    homepage = "https://github.com/pyca/bcrypt/"
    url      = "https://github.com/pyca/bcrypt/archive/3.1.4.tar.gz"

    version('3.1.4', sha256='ca122a2cdcdffb0fd04f9dfe3493766f298bef02dea2f190f35ea6fdee222b96')

    depends_on('py-setuptools', type='build')
    depends_on('py-cffi@1.1:', type=('build', 'run'))
    depends_on('py-six@1.4.1:', type=('build', 'run'))
