# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Lighttpd(CMakePackage):
    """a secure, fast, compliant and very flexible web-server"""

    homepage = "https://www.lighttpd.net"
    url = "https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-1.4.50.tar.gz"

    license("BSD-3-Clause")

    version("1.4.69", sha256="657010184c4c470ad98944abbf0a8e2281800fa2bb1836c7a2cd4a8874e97b28")
    version("1.4.55", sha256="065259fb618774df516add13df22a52cac76a8f59e4561f143fe3ec810f4a03a")
    version("1.4.54", sha256="5151d38cb7c4c40effa13710e77ebdbef899f945b062cf32befc02d128ac424c")
    version("1.4.53", sha256="423b3951f212e3a30511eb86f4662a1848c6e857074289ff23fc310eef520266")
    version("1.4.52", sha256="0f9de0227681c078f6b8c6154b581ced5fe7bcb5ff428ccf292581764b771145")
    version("1.4.51", sha256="4301fe64136c7030d63cccc96996c6603dcbe82cca9a72e0aca29ce88284c978")
    version("1.4.50", sha256="c9a9f175aca6db22ebebbc47de52c54a99bbd1dce8d61bb75103609a3d798235")
    version("1.4.49", sha256="8b744baf9f29c386fff1a6d2e435491e726cb8d29cfdb1fe20ab782ee2fc2ac7")

    depends_on("c", type="build")  # generated

    depends_on("pcre")

    def cmake_args(self):
        return ["-DSBINDIR=bin"]
