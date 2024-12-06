# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libmpdclient(MesonPackage):
    """Libmpdclient is a C library which implements the Music Player
    Daemon protocol."""

    homepage = "https://www.musicpd.org/"
    url = "https://github.com/MusicPlayerDaemon/libmpdclient/archive/v2.19.tar.gz"

    license("BSD-3-Clause")

    version("2.19", sha256="12b566b75c3b6789ff8fc94698497d1f3fbaf0cbf9fa6c3a1e3906ef0d2bcbbb")
    version("2.18", sha256="9b97d00022f2053c06d87bff40b319dfab930ee2b5fa9b8dec208a2911ca3efc")
    version("2.17", sha256="06eb4b67c63f64d647e97257ff5f8506bf9c2a26b314bf5d0dd5944995b59fc9")
    version("2.16", sha256="6651898489b69d2f2f8e94f0ed6ddcc0dd2cdbcf99b02131b790551922558d6c")
    version("2.15", sha256="dd3d36801e397bf43719a291289ff610af71859c08f3196a506e4b1af43c290c")

    depends_on("c", type="build")  # generated
