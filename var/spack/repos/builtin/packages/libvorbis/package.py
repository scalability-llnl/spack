# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libvorbis(AutotoolsPackage):
    """Ogg Vorbis is a fully open, non-proprietary, patent-and-royalty-free,
    general-purpose compressed audio format for mid to high quality (8kHz-
    48.0kHz, 16+ bit, polyphonic) audio and music at fixed and variable
    bitrates from 16 to 128 kbps/channel."""

    homepage = "https://xiph.org/vorbis/"
    url = "http://downloads.xiph.org/releases/vorbis/libvorbis-1.3.5.tar.gz"

    license("BSD-3-Clause")

    version("1.3.7", sha256="0e982409a9c3fc82ee06e08205b1355e5c6aa4c36bca58146ef399621b0ce5ab")
    version("1.3.5", sha256="6efbcecdd3e5dfbf090341b485da9d176eb250d893e3eb378c428a2db38301ce")

    depends_on("c", type="build")  # generated

    depends_on("libogg")

    depends_on("pkgconfig", type="build")

    def patch(self):
        filter_file(r"-force_cpusubtype_ALL", "", "configure", string=True)

    # `make check` crashes when run in parallel
    parallel = False
