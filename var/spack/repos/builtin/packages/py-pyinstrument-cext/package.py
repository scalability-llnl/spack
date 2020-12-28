# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyinstrumentCext(PythonPackage):
    """A CPython extension supporting pyinstrument."""

    homepage = "https://github.com/joerick/pyinstrument_cext"
    url      = "https://pypi.io/packages/source/p/pyinstrument_cext/pyinstrument_cext-0.2.2.tar.gz"

    version('0.2.2', sha256='f29e25f71d74c0415ca9310e5567fff0f5d29f4240a09a885abf8b0eed71cc5b')

    depends_on('py-setuptools', type='build')
