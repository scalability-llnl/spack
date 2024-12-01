# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.util.environment import is_system_path


class Lftp(AutotoolsPackage):
    """LFTP is a sophisticated file transfer program supporting a number
    of network protocols (ftp, http, sftp, fish, torrent)."""

    homepage = "https://lftp.yar.ru/"
    url = "https://lftp.yar.ru/ftp/lftp-4.9.2.tar.gz"

    license("GPL-3.0-or-later")

    version("4.9.2", sha256="a37589c61914073f53c5da0e68bd233b41802509d758a022000e1ae2076da733")
    version("4.8.1", sha256="6117866215cd889dab30ff73292cd1d35fe0e12a9af5cd76d093500d07ab65a3")
    version("4.7.7", sha256="7bce216050094a1146ed05bed8fe5b3518224764ffe98884a848d44dc76fff8f")
    version("4.6.4", sha256="791e783779d3d6b519d0c23155430b9785f2854023eb834c716f5ba78873b15a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("expat")
    depends_on("gettext")
    depends_on("iconv")
    depends_on("ncurses")
    depends_on("openssl")
    depends_on("readline")
    depends_on("zlib-api")

    def configure_args(self):
        args = [
            "--with-expat={0}".format(self.spec["expat"].prefix),
            "--with-openssl={0}".format(self.spec["openssl"].prefix),
            "--with-readline={0}".format(self.spec["readline"].prefix),
            "--with-zlib={0}".format(self.spec["zlib-api"].prefix),
            "--disable-dependency-tracking",
        ]
        if self.spec["iconv"].name == "libiconv":
            args.append(f"--with-libiconv-prefix={self.spec['iconv'].prefix}")
        elif not is_system_path(self.spec["iconv"].prefix):
            args.append("--without-libiconv-prefix")
        if "intl" not in self.spec["gettext"].libs.names:
            args.append("--without-libintl-prefix")
        elif not is_system_path(self.spec["gettext"].prefix):
            args.append("--with-libintl-prefix={0}".format(self.spec["gettext"].prefix))

        return args
