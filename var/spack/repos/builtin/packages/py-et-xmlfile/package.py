# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyEtXmlfile(PythonPackage):
    """An implementation of lxml.xmlfile for the standard library."""

    homepage = "https://bitbucket.org/openpyxl/et_xmlfile"
    pypi = "et_xmlfile/et_xmlfile-1.0.1.tar.gz"

    version('1.0.1', sha256='614d9722d572f6246302c4491846d2c393c199cfa4edc9af593437691683335b')

    depends_on('py-setuptools', type='build')
