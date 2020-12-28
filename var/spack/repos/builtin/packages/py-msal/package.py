# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyMsal(PythonPackage):
    """The Microsoft Authentication Library (MSAL) for Python library enables
    your app to access the Microsoft Cloud by supporting authentication of
    users with Microsoft Azure Active Directory accounts (AAD) and Microsoft
    Accounts (MSA) using industry standard OAuth2 and OpenID Connect."""

    homepage = "https://github.com/AzureAD/microsoft-authentication-library-for-python"
    url      = "https://pypi.io/packages/source/m/msal/msal-1.3.0.tar.gz"

    version('1.3.0', sha256='5442a3a9d006506e653d3c4daff40538bdf067bf07b6b73b32d1b231d5e77a92')
    version('1.0.0', sha256='ecbe3f5ac77facad16abf08eb9d8562af3bc7184be5d4d90c9ef4db5bde26340')

    depends_on('py-setuptools', type='build')
    depends_on('py-requests@2.0.0:2.999', type=('build', 'run'))
    depends_on('py-pyjwt@1.0.0:1.999+crypto', type=('build', 'run'))
