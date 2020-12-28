# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyasn1Modules(PythonPackage):
    """A collection of ASN.1 modules expressed in form of pyasn1 classes.
    Includes protocols PDUs definition (SNMP, LDAP etc.) and various data
    structures (X.509, PKCS etc.)."""

    homepage = "https://github.com/etingof/pyasn1-modules"
    url      = "https://pypi.io/packages/source/p/pyasn1-modules/pyasn1-modules-0.2.6.tar.gz"

    version('0.2.6', sha256='43c17a83c155229839cc5c6b868e8d0c6041dba149789b6d6e28801c64821722')
    version('0.2.5', sha256='ef721f68f7951fab9b0404d42590f479e30d9005daccb1699b0a51bb4177db96')

    depends_on('python@2.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pyasn1@0.4.6:0.4.999', type=('build', 'run'), when='@0.2.6')
    depends_on('py-pyasn1@0.4.1:0.4.999', type=('build', 'run'), when='@0.2.5')
