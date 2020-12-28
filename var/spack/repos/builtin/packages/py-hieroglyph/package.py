# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHieroglyph(PythonPackage):
    """Hieroglyph is an extension for Sphinx which builds HTML
    presentations from ReStructured Text documents.
    """

    homepage = "https://github.com/nyergler/hieroglyph"
    url      = "https://pypi.io/packages/source/h/hieroglyph/hieroglyph-1.0.0.tar.gz"

    version('1.0.0', sha256='8e137f0b1cd60c47b870011089790d3c8ddb74fcf409a75ddf2c7f2516ff337c')
    version('master')

    depends_on('py-setuptools')
    depends_on('py-sphinx@1.2:')
    depends_on('py-six')
