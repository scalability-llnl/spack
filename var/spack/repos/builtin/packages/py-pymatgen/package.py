# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPymatgen(PythonPackage):
    """Python Materials Genomics is a robust materials analysis code that
    defines core object representations for structures and molecules with
    support for many electronic structure codes. It is currently the core
    analysis code powering the Materials Project."""

    homepage = "http://www.pymatgen.org/"
    url      = "https://pypi.io/packages/source/p/pymatgen/pymatgen-4.7.2.tar.gz"

    version('4.7.2', sha256='e439b78cc3833a03963c3c3efe349d8a0e52a1550c8a05c56a89aa1b86657436')
    version('4.6.2', sha256='f34349090c6f604f7d402cb09cd486830b38523639d7160d7fd282d504036a0e')

    extends('python', ignore='bin/tabulate')

    depends_on('py-setuptools@18.0:', type='build')

    depends_on('py-numpy@1.9:',          type=('build', 'run'))
    depends_on('py-six',                 type=('build', 'run'))
    depends_on('py-requests',            type=('build', 'run'))
    depends_on('py-pyyaml@3.11:',        type=('build', 'run'))
    depends_on('py-monty@0.9.6:',        type=('build', 'run'))
    depends_on('py-scipy@0.14:',         type=('build', 'run'))
    depends_on('py-pydispatcher@2.0.5:', type=('build', 'run'))
    depends_on('py-tabulate',            type=('build', 'run'))
    depends_on('py-spglib@1.9.8.7:',     type=('build', 'run'))
    depends_on('py-matplotlib@1.5:',     type=('build', 'run'))
    depends_on('py-palettable@2.1.1:',   type=('build', 'run'))
