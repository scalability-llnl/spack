# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsgiref(PythonPackage):
    """ASGI specification and utilities."""

    homepage = "https://asgi.readthedocs.io/en/latest/"
    url      = "https://github.com/django/asgiref/archive/3.2.7.tar.gz"

    version('3.2.7', sha256='8a0b556b9e936418475f6670d59e14592c41d15d00b5ea4ad26f2b46f9f4fb9a')
    version('3.2.6', sha256='29788163bdad8d494475a0137eba39b111fd86fbe825534a9376f9f2ab44251a')
    version('3.2.5', sha256='eeb01ba02e86859746ee2a7bc8a75c484a006dc9575723563f24642a12b2bba8')
    version('3.2.4', sha256='89e47532340338b7eafd717ab28658e8b48f4565d8384628c88d2d41565c8da0')
    version('3.2.3', sha256='d38e16141c7189e23bfe03342d9cd3dbfd6baab99217892bfa7bc5646315b6bd')
    version('3.2.2', sha256='47edf327aa70f317c9bc810d469ce681f1b35a7f499f68cf2b5da3ba6a651e69')
    version('3.2.1', sha256='06a21df1f4456d29079f3c475c09ac31167bcc5f024c637dedf4e00d2dd9020b')
    version('3.2.0', sha256='5db8c7a6c1ff54ea04a52f994d8af959427f1cab8e427aa802492a89fb0b635a')
    version('3.1.4', sha256='bf01c52111ef7af2adc1e6d90282d2a32c5ebe09e84ae448389ceff7cef53fa9')
    version('3.1.3', sha256='5b8bb7b3719b8c12a6c2363784a4d8c0eb5e980d8b4fdb6f38eccb52071dfab5')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
