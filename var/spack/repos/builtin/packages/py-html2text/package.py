# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHtml2text(PythonPackage):
    """Turn HTML into equivalent Markdown-structured text."""

    homepage = "https://github.com/Alir3z4/html2text/"
    url      = "https://pypi.io/packages/source/h/html2text/html2text-2016.9.19.tar.gz"

    version('2016.9.19', sha256='554ef5fd6c6cf6e3e4f725a62a3e9ec86a0e4d33cd0928136d1c79dbeb7b2d55')

    depends_on('py-setuptools', type='build')
