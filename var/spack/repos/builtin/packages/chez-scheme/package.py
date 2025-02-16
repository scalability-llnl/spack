# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ChezScheme(AutotoolsPackage):
    """Compiler and run-time system for the language of the Revised^6 Report
    on Scheme (R6RS), with numerous extensions."""

    homepage = "https://cisco.github.io/ChezScheme/"
    url = "https://github.com/cisco/ChezScheme/releases/download/v10.1.0/csv10.1.0.tar.gz"
    git = "https://github.com/cisco/ChezScheme.git"

    license("Apache-2.0", checked_by="Buldram")
    maintainers("Buldram")

    version("main", branch="main", submodules=True)
    version("10.1.0", sha256="9181a6c8c4ab5e5d32d879ff159d335a50d4f8b388611ae22a263e932c35398b")
    version("10.0.0", sha256="d37199012b5ed1985c4069d6a87ff18e5e1f5a2df27e402991faf45dc4f2232c")

    variant("threads", default=True, description="Enable multithreading support")
    variant("iconv", default=True, description="Use iconv")
    variant("libffi", default=True, description="Use libffi")
    variant("curses", default=True, description="Use ncurses")
    variant("x11", default=True, description="Use libx11")

    depends_on("c", type="build")
    depends_on("lz4", type="build")
    depends_on("zlib-api", type="build")
    depends_on("uuid", type="build")
    depends_on("uuid", type="link", when="platform=windows")
    depends_on("iconv", type="link", when="+iconv")
    depends_on("libffi", type="link", when="+libffi")
    depends_on("ncurses", type="link", when="+curses")
    depends_on("libx11", type="build", when="+x11")

    conflicts("^[virtuals=iconv] libiconv", when="platform=linux")
    conflicts("+iconv", when="platform=windows")
    conflicts("+curses", when="platform=windows")

    def setup_build_environment(self, env):
        env.set("LZ4", self.spec["lz4"].libs.link_flags)
        env.set("ZLIB", self.spec["zlib-api"].libs.link_flags)
        env.set("ZUO_JOBS", make_jobs)

    def patch(self):
        true = which_string("true", required=True)
        if true not in ["/bin/true", "/usr/bin/true"]:
            filter_file("/bin/true", f"'{true}'", "makefiles/installsh", string=True)
        if self.spec.satisfies("+curses"):
            filter_file(
                "-lncurses", f"'{self.spec['ncurses'].libs.link_flags}'", "configure", string=True
            )

    def configure_args(self):
        args = ["--as-is", "--threads" if self.spec.satisfies("+threads") else "--no-threads"]
        if self.spec.satisfies("~iconv"):
            args.append("--disable-iconv")
        if self.spec.satisfies("+libffi"):
            args.append("--enable-libffi")
        if self.spec.satisfies("~curses"):
            args.append("--disable-curses")
        if self.spec.satisfies("~x11"):
            args.append("--disable-x11")
        return args
