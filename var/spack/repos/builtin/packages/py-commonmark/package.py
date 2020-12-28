# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCommonmark(PythonPackage):
    """commonmark.py is a pure Python port of jgm's commonmark.js, a Markdown
    parser and renderer for the CommonMark specification, using only native
    modules."""

    homepage = "https://github.com/readthedocs/commonmark.py"
    url      = "https://pypi.io/packages/source/c/commonmark/commonmark-0.9.0.tar.gz"

    version('0.9.0', sha256='867fc5db078ede373ab811e16b6789e9d033b15ccd7296f370ca52d1ee792ce0')

    depends_on('py-setuptools', type='build')
    depends_on('py-future', type=('build', 'run'))
