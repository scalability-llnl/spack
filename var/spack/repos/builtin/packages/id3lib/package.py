# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Id3lib(AutotoolsPackage):
    """Library for manipulating ID3v1 and ID3v2 tags"""

    homepage = "https://id3lib.sourceforge.net/"
    url = "https://downloads.sourceforge.net/project/id3lib/id3lib/3.8.3/id3lib-3.8.3.tar.gz"

    license("GPL-2.0-only")

    version("3.8.3", sha256="2749cc3c0cd7280b299518b1ddf5a5bcfe2d1100614519b68702230e26c7d079")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")

    # http://connie.slackware.com/~alien/slackbuilds/id3lib/build/id3lib-3.8.3_gcc4.diff
    # this is due to some changes in the c++ standard library headers
    patch("id3lib-3.8.3_gcc4.diff")
