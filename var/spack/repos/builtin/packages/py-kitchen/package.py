# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKitchen(PythonPackage):
    """Kitchen contains a cornucopia of useful code
    """

    homepage = "https://fedorahosted.org/kitchen"
    url      = "https://pypi.io/packages/source/k/kitchen/kitchen-1.2.6.tar.gz"

    version('1.2.6', sha256='b84cf582f1bd1556b60ebc7370b9d331eb9247b6b070ce89dfe959cba2c0b03c')
    version('1.1.1', sha256='25670f80bcbabd0656946125cfad310980d5a5900d6c160d4f0187292120284e')

    depends_on('py-setuptools', type='build')
