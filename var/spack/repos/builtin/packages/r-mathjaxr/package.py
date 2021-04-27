# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RMathjaxr(RPackage):
    """Using 'Mathjax' in Rd Files

    Provides 'MathJax' and macros to enable its use within Rd files for
    rendering equations in the HTML help files."""

    homepage = "https://github.com/wviechtb/mathjaxr"
    url      = "https://cloud.r-project.org/src/contrib/mathjaxr_1.0-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/mathjaxr"

    version('1.0-1', sha256='0d3d370c4d0c7c7c6d5541d4e0ae50170b4084ca8a66e8a43bd92c7d1c112148')
