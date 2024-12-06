# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vsftpd(MakefilePackage):
    """vsftpd is a GPL licensed FTP server for UNIX systems, including
    Linux."""

    homepage = "https://security.appspot.com/vsftpd.html"
    url = "https://security.appspot.com/downloads/vsftpd-3.0.3.tar.gz"

    license("GPL-2.0-only")

    version("3.0.3", sha256="9d4d2bf6e6e2884852ba4e69e157a2cecd68c5a7635d66a3a8cf8d898c955ef7")
    version("3.0.2", sha256="be46f0e2c5528fe021fafc8dab1ecfea0c1f183063a06977f8537fcd0b195e56")
    version("3.0.1", sha256="65487a9fccc0ae566df5999a84448a9ccb57b556b7643ffd345540299487784c")

    depends_on("c", type="build")  # generated

    depends_on("libcap")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.man.man5)
        mkdirp(prefix.man.man8)
        install("vsftpd", prefix.bin)
        install("vsftpd.conf.5", prefix.man.man5)
        install("vsftpd.8", prefix.man.man8)
        install_tree("xinetd.d", join_path(prefix, "xinetd.d"))
