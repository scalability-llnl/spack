# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGit2r(RPackage):
    """Interface to the 'libgit2' library, which is a pure C implementation of
    the 'Git' core methods. Provides access to 'Git' repositories to extract
    data and running some basic 'Git' commands."""

    homepage = "https://github.com/ropensci/git2r"
    url      = "https://cloud.r-project.org/src/contrib/git2r_0.18.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/git2r"

    version('0.27.1', sha256='099207f180aa45ddcc443cbb22487eafd14e1cd8e5979b3476214253fd773bc0')
    version('0.26.1', sha256='13d609286a0af4ef75ba76f2c2f856593603b8014e311b88896243a50b417435')
    version('0.26.0', sha256='56671389c3a50591e1dae3be8c3b0112d06d291f897d7fe14db17aea175616cf')
    version('0.18.0', sha256='91b32e49afb859c0c4f6f77988343645e9499e5046ef08d945d4d8149b6eff2d')
    version('0.15.0', sha256='682ab9e7f71b2ed13a9ef95840df3c6b429eeea070edeb4d21d725cf0b72ede6')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('zlib')
    depends_on('openssl')
    depends_on('libgit2')
