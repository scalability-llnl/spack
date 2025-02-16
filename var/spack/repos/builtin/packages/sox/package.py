# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sox(AutotoolsPackage):
    """SoX, the Swiss Army knife of sound processing programs."""

    homepage = "https://sox.sourceforge.net/Main/HomePage"
    url = "https://downloads.sourceforge.net/project/sox/sox/14.4.2/sox-14.4.2.tar.bz2"

    version("14.4.2", sha256="81a6956d4330e75b5827316e44ae381e6f1e8928003c6aa45896da9041ea149c")

    depends_on("c", type="build")

    variant("mp3", default=False, description="Build with mp3 support")

    depends_on("bzip2")
    depends_on("flac")
    depends_on("libvorbis")
    depends_on("opus")
    depends_on("lame", when="+mp3")
    depends_on("libmad", when="+mp3")

    def flag_handler(self, name, flags):
        # https://github.com/Homebrew/homebrew-core/blob/master/Formula/s/sox.rb
        if name == "cflags":
            if self.spec.satisfies("%apple-clang@15:"):
                flags.append("-Wno-incompatible-function-pointer-types")
        return (flags, None, None)
