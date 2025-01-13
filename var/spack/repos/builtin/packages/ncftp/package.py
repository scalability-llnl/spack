# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ncftp(AutotoolsPackage):
    """NcFTP Client is a set of application programs implementing the
    File Transfer Protocol."""

    homepage = "https://www.ncftp.com/"
    url = "ftp://ftp.ncftp.com/ncftp/ncftp-3.2.6-src.tar.gz"

    license("ClArtistic")

    version("3.2.7", sha256="dbde0d3b4d28ba3a445621e10deaee57a6ba3ced277cc9dbce4052bcddf6cb2a")
    version("3.2.6", sha256="129e5954850290da98af012559e6743de193de0012e972ff939df9b604f81c23")

    depends_on("ncurses")

    def url_for_version(self, version):
        url = "https://www.ncftp.com/public_ftp/ncftp/{}-src.tar.gz"
        if version < Version("3.2.7"):
            return url.format(f"older_versions/ncftp-{version}")
        else:
            return url.format(f"ncftp-{version}")

    def setup_build_environment(self, env):
        if self.spec.satisfies("%gcc@10:"):
            # https://bugs.gentoo.org/722550
            env.set("CFLAGS", "-fcommon")
