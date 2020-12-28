# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPandocfilters(PythonPackage):
    """A python module for writing pandoc filters"""

    homepage = "https://github.com/jgm/pandocfilters"
    url      = "https://pypi.io/packages/source/p/pandocfilters/pandocfilters-1.4.2.tar.gz"

    version('1.4.2', sha256='b3dd70e169bb5449e6bc6ff96aea89c5eea8c5f6ab5e207fc2f521a2cf4a0da9')
