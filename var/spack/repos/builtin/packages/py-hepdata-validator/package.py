# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHepdataValidator(PythonPackage):
    """Validation schema and code for HEPdata submissions."""

    homepage = "https://github.com/hepdata/hepdata-validator"
    url = "https://pypi.io/packages/source/h/hepdata_validator/hepdata_validator-0.1.16.tar.gz"

    tags = ['hep']

    version('0.1.16', sha256='3d7f725328ecdbb66826bff2e48a40a1d9234249859c8092ca0e92be7fb78111')
    version('0.1.15', sha256='1030654b1a1cfc387c2759f8613f033da467c8182dc027e181227aeb52854bb2')
    version('0.1.14', sha256='d1596741fb26be234c2adb6972306908f09b049dc670d8312cf2636f1a615a52')
    version('0.1.8', sha256='08686563e0130c5dd6d9fb8d5c7bf5a2617a637b105a42f7106b96a31eaffa61')

    depends_on('py-setuptools', type='build')
    depends_on('py-jsonschema', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
