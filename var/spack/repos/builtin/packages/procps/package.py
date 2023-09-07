# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.util.environment import is_system_path


class Procps(AutotoolsPackage):
    """Command line and full screen utilities for browsing procfs, a "pseudo"
    file system dynamically generated by the kernel to provide information
    about the status of entries in its process table."""

    homepage = "https://gitlab.com/procps-ng/procps"
    git = "https://gitlab.com/procps-ng/procps.git"
    url = "https://gitlab.com/procps-ng/procps/-/archive/v4.0.3/procps-v4.0.3.tar.gz"

    version("master", branch="master")
    version("4.0.3", sha256="14cc21219c45d196772274ea3f194f6d668b6cc667fbde9ee6d8039121b73fa6")
    version("4.0.2", sha256="b03e4b55eaa5661e726acb714e689356d80bc056b09965c2284d039ba8dc21e8")
    version("4.0.1", sha256="1eaff353306aba12816d14881f2b88c7c9d06023825f7224700f0c01f66c65cd")
    version("4.0.0", sha256="dea39e0e7b1367e28c887d736d1a9783df617497538603cdff432811a1016945")
    version("3.3.17", sha256="efa6f6b4625a795f5c8a3d5bd630a121d270bc8573c5a0b6a6068e73611d6cd5")
    version("3.3.16", sha256="7f09945e73beac5b12e163a7ee4cae98bcdd9a505163b6a060756f462907ebbc")
    version("3.3.15", sha256="14dfa751517dd844efa9f492e3ad8071f908a269c6aea643b9a1759235fa2053")
    version("3.3.14", sha256="1ff716e7bde6b3841b8519831690b10b644ed344490369c55e410edc8db2fe18")

    variant("nls", default=True, description="Enable Native Language Support.")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig@0.9.0:", type="build")
    depends_on("dejagnu", type="test")
    depends_on("iconv")
    depends_on("gettext", type="build")
    depends_on("gettext", when="+nls")
    depends_on("ncurses")

    conflicts("platform=darwin", msg="procps is linux-only")

    # Need to tell the build to use the tools it already has to find
    # libintl (if appropriate).
    patch("libintl-3.3.14.patch", when="@3.3.14:3.3")
    patch("libintl-4.0.0.patch", when="@=4.0.0")
    patch("libintl-4.0.1.patch", when="@4.0.1:4.0.3")

    def autoreconf(self, spec, prefix):
        sh = which("sh")
        sh("autogen.sh")

    def configure_args(self):
        spec = self.spec
        args = ["--with-ncurses"]

        if "+nls" in spec:
            args.append("--enable-nls")
            if "intl" not in spec["gettext"].libs.names:
                args.append("--without-libintl-prefix")
            elif not is_system_path(spec["gettext"].prefix):
                args.append("--with-libintl-prefix=" + spec["gettext"].prefix)
        else:
            args.append("--disable-nls")

        if spec["iconv"].name == "libc":
            args.append("--without-libiconv-prefix")
        elif not is_system_path(spec["iconv"].prefix):
            args.append("--with-libiconv-prefix={0}".format(spec["iconv"].prefix))

        return args
