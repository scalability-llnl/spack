# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sox(AutotoolsPackage):
    """SoX, the Swiss Army knife of sound processing programs."""

    homepage = "https://sox.sourceforge.net/Main/HomePage"
    url = "https://downloads.sourceforge.net/project/sox/sox/14.4.2/sox-14.4.2.tar.bz2"

    version("14.4.2", sha256="81a6956d4330e75b5827316e44ae381e6f1e8928003c6aa45896da9041ea149c")

    depends_on("c", type="build")  # generated

    variant("mp3", default=False, description="Build with mp3 support")

    depends_on("bzip2")
    depends_on("flac")
    depends_on("libvorbis")
    depends_on("opus")
    depends_on("lame", when="+mp3")
    depends_on("libmad", when="+mp3")
