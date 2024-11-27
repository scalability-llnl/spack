# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Vcsh(Package):
    """config manager based on git"""

    homepage = "https://github.com/RichiH/vcsh"
    url = "https://github.com/RichiH/vcsh/archive/v1.20151229.tar.gz"

    license("GPL-2.0-or-later")

    version(
        "1.20151229-1", sha256="7682a517eaf88a86ea5e38ad81707800e965375eaff8b5cfd882e210fe2fef71"
    )
    version(
        "1.20151229", sha256="ae069506b0490287aefa582ab4e6af1c7ebc4dca743b17d91e0c8d0327d7a3fa"
    )
    version(
        "1.20150502", sha256="127c7f35e9b097b722917d42f9652375033b12f14b6702a08621cb16205d253f"
    )
    version(
        "1.20141026", sha256="63e65df01f35611b3dfca97317298fc2da6c33bfad6edb778ea44b23857e7c54"
    )
    version(
        "1.20141025", sha256="2a9009b19289f60d5919d9e19d2a3f53dbe373dbc84e6d50ec0ee1b5ffb2f282"
    )

    depends_on("git", type="run")

    # vcsh provides a makefile, if needed the install method should be adapted
    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("vcsh", prefix.bin)
