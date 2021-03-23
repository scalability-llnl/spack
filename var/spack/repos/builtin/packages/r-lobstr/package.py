# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLobstr(RPackage):
    """A set of tools for inspecting and understanding R data structures
    inspired by str(). Includes ast() for visualizing abstract syntax trees,
    ref() for showing shared references, cst() for showing call stack trees,
    and obj_size() for computing object sizes."""

    homepage = "https://lobstr.r-lib.org"
    url      = "https://cloud.r-project.org/src/contrib/lobstr_1.1.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/lobstr"

    version('1.1.1', sha256='923a384d9239d44b63dfc57f5a0309a1e59b9698ef05183f598f6f4fffb1e0fd')
    version('1.0.1', sha256='f94d0a207f1b44097907d761c45130be386e908aec4ac472bf2fec6d36c74a69')
    version('1.0.0', sha256='b9d5dcda36a1c1bd208ddf814f9b5a9c2c8b07730647b98505be7e296b14c883')

    depends_on('r-rlang@0.3.0:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-crayon', type=('build', 'run'))
