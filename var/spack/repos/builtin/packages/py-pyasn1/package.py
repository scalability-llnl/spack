# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack.package import *


class PyPyasn1(PythonPackage):
    """Pure-Python implementation of ASN.1 types and DER/BER/CER codecs
    (X.208)."""

    homepage = "https://github.com/etingof/pyasn1"
    url      = "https://pypi.io/packages/source/p/pyasn1/pyasn1-0.4.6.tar.gz"

    version('0.4.6', sha256='b773d5c9196ffbc3a1e13bdf909d446cad80a039aa3340bcad72f395b76ebc86')
    version('0.4.5', sha256='da2420fe13a9452d8ae97a0e478adde1dee153b11ba832a95b223a2ba01c10f7')
    version('0.2.3', sha256='738c4ebd88a718e700ee35c8d129acce2286542daa80a82823a7073644f706ad')

    depends_on('python@2.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
