# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fastdfs(Package):
    """
    FastDFS is an open source high performance distributed file system.
    It's major functions include: file storing, file syncing and file
    accessing (file uploading and file downloading), and it can resolve
    the high capacity and load balancing problem. FastDFS should meet
    the requirement of the website whose service based on files such
    as photo sharing site and video sharing site.
    """

    homepage = "https://github.com/happyfish100/fastdfs"
    url = "https://github.com/happyfish100/fastdfs/archive/V6.05.tar.gz"

    license("GPL-3.0-or-later")

    version("6.05", sha256="00b736a1a7bd9cb5733aa51969efaa3b46df3764988c1edb43f06d72c4d575d9")
    version("6.04", sha256="76090f6bbd0add08b049ce17f30a7507a44ef0d883784cad774b380ba4906916")
    version("6.03", sha256="142be123eb389335b3b3793f0765494bdad3a632e4352af57861ed29098ec8d1")
    version("6.02", sha256="b1801f80da9ebce1d84e7e05356c4614190651cb6a5cb4f5662d9196fe243e21")
    version("6.01", sha256="b72f4ff6beb21a83af59aeba9f1904e727fa2c1e960e0a9c2b969138d2804148")

    depends_on("c", type="build")  # generated

    depends_on("perl", type="build")
    depends_on("libfastcommon", type="build")

    def install(self, spec, prefix):
        sh = which("sh")
        sh("make.sh")
        sh("make.sh", "install")
        install_tree(".", prefix)
