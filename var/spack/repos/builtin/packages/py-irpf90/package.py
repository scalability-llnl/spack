# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIrpf90(PythonPackage):
    """IRPF90 is a Fortran90 preprocessor written in Python for programming
    using the Implicit Reference to Parameters (IRP) method. It simplifies the
    development of large fortran codes in the field of scientific high
    performance computing."""

    homepage = "http://irpf90.ups-tlse.fr"
    url = "https://pypi.io/packages/source/i/irpf90/irpf90-1.7.7.tar.gz"

    maintainers = ['scemama']

    version('1.7.7', sha256='c6b2eecb9180f1feaab9644bbed806637a4a30a0fad2c4775a985fcc01a99530')

    depends_on('python@2.7.0:2.8.999', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
