# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RTinytex(RPackage):
    """Helper Functions to Install and Maintain TeX Live, and Compile LaTeX Documents

    Helper functions to install and maintain the 'LaTeX' distribution named
    'TinyTeX' (<https://yihui.name/tinytex/>), a lightweight, cross-platform,
    portable, and easy-to-maintain version of 'TeX Live'. This package also
    contains helper functions to compile 'LaTeX' documents, and install missing
    'LaTeX' packages automatically."""

    homepage = "https://github.com/yihui/tinytex"
    url      = "https://cloud.r-project.org/src/contrib/tinytex_0.15.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/tinytex"

    version('0.28', sha256='76a0650aeab04eb252dc9cfa9ba855d88b09dfc2207c4a8ea2ea04fa0e0eea86')
    version('0.15', sha256='5d0988d3b7f763dfa65c722f177452a21344e428415a4b31aeb51478f0abad90')

    depends_on('r-xfun@0.5:', type=('build', 'run'))
    depends_on('r-xfun@0.19:', when='@0.28:', type=('build', 'run'))
