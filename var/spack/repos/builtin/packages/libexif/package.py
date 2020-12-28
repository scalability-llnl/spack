# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Libexif(AutotoolsPackage, SourceforgePackage):
    """A library to parse an EXIF file and read the data from those tags"""

    homepage = "https://sourceforge.net/projects/libexif"
    sourceforge_mirror_path = "libexif/libexif-0.6.21.tar.bz2"

    maintainers = ['TheQueasle']

    version('0.6.21', sha256='16cdaeb62eb3e6dfab2435f7d7bccd2f37438d21c5218ec4e58efa9157d4d41a')
    depends_on('glib')
