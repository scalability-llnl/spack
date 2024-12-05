# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Flac(AutotoolsPackage):
    """Encoder/decoder for the Free Lossless Audio Codec"""

    homepage = "https://xiph.org/flac/index.html"
    url = "http://downloads.xiph.org/releases/flac/flac-1.3.2.tar.xz"

    license("BSD-3-Clause AND GPL-2.0-or-later")

    version("1.4.3", sha256="6c58e69cd22348f441b861092b825e591d0b822e106de6eb0ee4d05d27205b70")
    version("1.4.2", sha256="e322d58a1f48d23d9dd38f432672865f6f79e73a6f9cc5a5f57fcaa83eb5a8e4")
    version("1.4.1", sha256="91303c3e5dfde52c3e94e75976c0ab3ee14ced278ab8f60033a3a12db9209ae6")
    version("1.4.0", sha256="af41c0733c93c237c3e52f64dd87e3b0d9af38259f1c7d11e8cbf583c48c2506")
    version("1.3.4", sha256="8ff0607e75a322dd7cd6ec48f4f225471404ae2730d0ea945127b1355155e737")
    version("1.3.3", sha256="213e82bd716c9de6db2f98bcadbc4c24c7e2efe8c75939a1a84e28539c4e1748")
    version("1.3.2", sha256="91cfc3ed61dc40f47f050a109b08610667d73477af6ef36dcad31c31a4a8d53f")
    version("1.3.1", sha256="4773c0099dba767d963fd92143263be338c48702172e8754b9bc5103efe1c56c")
    version("1.3.0", sha256="fa2d64aac1f77e31dfbb270aeb08f5b32e27036a52ad15e69a77e309528010dc")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("libogg@1.1.2:")
