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

    variant("threads", default=False, description="Enable multithreading support")
    variant("libffi", default=False, description="Use libffi")
    variant("iconv", default=True, description="Use iconv")
    variant("curses", default=True, description="Use ncurses")
    variant("x11", default=True, description="Use libx11")

    depends_on("c", type="build")
    depends_on("zuo", type="build", when="@10.1.0:")
    depends_on("lz4", type="build")
    depends_on("zlib-api", type="build")
    depends_on("uuid", type="build")
    depends_on("uuid", type="link", when="platform=windows")
    depends_on("libffi", type="link", when="+libffi")
    depends_on("iconv", type="link", when="+iconv")
    depends_on("ncurses", type="link", when="+curses")
    depends_on("libx11", type="build", when="+x11")

    conflicts("^[virtuals=iconv] libiconv", when="platform=linux")
    conflicts("+iconv", when="platform=windows")
    conflicts("+curses", when="platform=windows")

    def setup_build_environment(self, env):
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
        spec = self.spec
        args = [
            f"LZ4={spec['lz4'].libs.link_flags}",
            f"ZLIB={spec['zlib-api'].libs.link_flags}",
            "--as-is",
            "--threads" if spec.satisfies("+threads") else "--nothreads",
        ]
        if spec.satisfies("@10.1.0:"):
            args.append(f"ZUO={spec['zuo'].prefix.bin.join('zuo')}")
        if spec.satisfies("+libffi"):
            args.append("--enable-libffi")
        if spec.satisfies("~iconv"):
            args.append("--disable-iconv")
        if spec.satisfies("~curses"):
            args.append("--disable-curses")
        if spec.satisfies("~x11"):
            args.append("--disable-x11")
        return args
