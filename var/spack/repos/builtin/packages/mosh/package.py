# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mosh(AutotoolsPackage):
    """Remote terminal application that allows roaming, supports intermittent
    connectivity, and provides intelligent local echo and line editing of user
    keystrokes. Mosh is a replacement for SSH. It's more robust and responsive,
    especially over Wi-Fi, cellular, and long-distance links.
    """

    homepage = "https://mosh.org/"
    url = "https://mosh.org/mosh-1.2.6.tar.gz"

    license("GPL-3.0-or-later")

    version("1.4.0", sha256="872e4b134e5df29c8933dff12350785054d2fd2839b5ae6b5587b14db1465ddd")
    version("1.3.2", sha256="da600573dfa827d88ce114e0fed30210689381bbdcff543c931e4d6a2e851216")
    version("1.3.0", sha256="320e12f461e55d71566597976bd9440ba6c5265fa68fbf614c6f1c8401f93376")
    version("1.2.6", sha256="7e82b7fbfcc698c70f5843bb960dadb8e7bd7ac1d4d2151c9d979372ea850e85")

    depends_on("protobuf")
    depends_on("ncurses")
    depends_on("zlib-api")
    depends_on("openssl")

    depends_on("pkgconfig", type="build")
    depends_on("perl", type="run")

    build_directory = "spack-build"
