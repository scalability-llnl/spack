# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyelftools(PythonPackage):
    """A pure-Python library for parsing and analyzing ELF files and DWARF
       debugging information"""
    homepage = "https://pypi.python.org/pypi/pyelftools"
    url      = "https://pypi.io/packages/source/p/pyelftools/pyelftools-0.26.tar.gz"

    version('0.26', sha256='86ac6cee19f6c945e8dedf78c6ee74f1112bd14da5a658d8c9d4103aed5756a2')
    version('0.23', sha256='fc57aadd096e8f9b9b03f1a9578f673ee645e1513a5ff0192ef439e77eab21de')

    depends_on('py-setuptools', when='@0.25:', type='build')
