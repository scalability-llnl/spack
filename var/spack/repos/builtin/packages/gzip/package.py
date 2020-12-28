# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Gzip(AutotoolsPackage):
    """GNU Gzip is a popular data compression program originally written by
    Jean-loup Gailly for the GNU project."""

    homepage = "https://www.gnu.org/software/gzip/"
    url      = "https://ftp.gnu.org/gnu/gzip/gzip-1.10.tar.gz"

    version('1.10', sha256='c91f74430bf7bc20402e1f657d0b252cb80aa66ba333a25704512af346633c68')

    depends_on('gmake', type='build')

    # Gzip makes a recursive symlink if built in-source
    build_directory = 'spack-build'
