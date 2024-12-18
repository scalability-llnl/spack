# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *
from spack.util.environment import is_system_path


class Subversion(AutotoolsPackage):
    """Apache Subversion - an open source version control system."""

    homepage = "https://subversion.apache.org/"
    urls = [
        "https://archive.apache.org/dist/subversion/subversion-1.12.2.tar.gz",
        "https://downloads.apache.org/subversion/subversion-1.13.0.tar.gz",
    ]

    maintainers("cosmicexplorer")

    tags = ["build-tools"]

    # internal lz4, x509, and utf8proc code have different licenses.
    license("Apache-2.0 AND BSD-3-Clause AND BSD-2-Clause AND MIT", checked_by="tgamblin")

    version("1.14.2", sha256="fd826afad03db7a580722839927dc664f3e93398fe88b66905732c8530971353")
    version("1.14.1", sha256="dee2796abaa1f5351e6cc2a60b1917beb8238af548b20d3e1ec22760ab2f0cad")
    version("1.14.0", sha256="ef3d1147535e41874c304fb5b9ea32745fbf5d7faecf2ce21d4115b567e937d0")
    version("1.13.0", sha256="daad440c03b8a86fcca804ea82217bb1902cfcae1b7d28c624143c58dcb96931")
    version("1.12.2", sha256="f4927d6603d96c5ddabebbafe9a0f6833c18a891ff0ce1ea6ffd186ce9bc21f3")
    version("1.9.7", sha256="c72a209c883e20245f14c4e644803f50ae83ae24652e385ff5e82300a0d06c3c")
    version("1.9.6", sha256="a400cbc46d05cb29f2d7806405bb539e9e045b24013b0f12f8f82688513321a7")
    version("1.9.5", sha256="280ba586c5d51d7b976b65d22d5e8e42f3908ed1c968d71120dcf534ce857a83")
    version("1.9.3", sha256="74cd21d2f8a2a54e4dbd2389fe1605a19dbda8ba88ffc4bb0edc9a66e143cc93")
    version("1.8.17", sha256="1b2cb9a0ca454035e55b114ee91c6433b9ede6c2893f2fb140939094d33919e4")
    version("1.8.13", sha256="17e8900a877ac9f0d5ef437c20df437fec4eb2c5cb9882609d2277e2312da52c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("serf", default=True, description="Serf HTTP client library")
    variant("perl", default=False, description="Build with Perl bindings")
    variant("apxs", default=True, description="Build with APXS")
    variant("nls", default=True, description="Enable Native Language Support")

    depends_on("apr")
    depends_on("apr-util")
    depends_on("zlib-api")
    depends_on("sqlite@3.8.2:")
    depends_on("expat")
    depends_on("lz4", when="@1.10:")
    depends_on("utf8proc", when="@1.10:")
    depends_on("serf", when="+serf")
    depends_on("gettext", when="+nls")

    extends("perl", when="+perl")
    depends_on("swig@1.3.24:3.0.0", when="+perl")
    depends_on("perl-termreadkey", when="+perl")

    executables = [r"^svn$"]

    # https://www.linuxfromscratch.org/blfs/view/svn/general/subversion.html
    def configure_args(self):
        spec = self.spec
        args = [
            "--with-apr={0}".format(spec["apr"].prefix),
            "--with-apr-util={0}".format(spec["apr-util"].prefix),
            "--with-sqlite={0}".format(spec["sqlite"].prefix),
            "--with-expat={0}:{1}:{2}".format(
                spec["expat"].headers.directories[0],
                spec["expat"].libs.directories[0],
                spec["expat"].libs.names[0],
            ),
            "--with-zlib={0}".format(spec["zlib-api"].prefix),
            "--without-apxs",
            "--without-trang",
            "--without-doxygen",
            "--without-berkeley-db",
            "--without-sasl",
            "--without-libmagic",
            "--without-kwallet",
            "--without-jdk",
            "--without-boost",
        ]

        if spec.satisfies("@1.10:"):
            args.extend(
                [
                    "--with-lz4={0}".format(spec["lz4"].prefix),
                    "--with-utf8proc={0}".format(spec["utf8proc"].prefix),
                ]
            )

        if "+serf" in spec:
            args.append("--with-serf={0}".format(spec["serf"].prefix))
        else:
            args.append("--without-serf")

        if "swig" in spec:
            args.append("--with-swig={0}".format(spec["swig"].prefix))
        else:
            args.append("--without-swig")

        if "+perl" in spec:
            args.append("PERL={0}".format(spec["perl"].command.path))

        if spec.satisfies("~apxs"):
            args.append("APXS=no")

        if "+nls" in spec:
            args.append("--enable-nls")
            if "intl" in spec["gettext"].libs.names:
                # Using .libs.link_flags is the canonical way to add these arguments,
                # but since libintl is much smaller than the rest and also the only
                # necessary one, we would specify it by hand here
                args.append("LIBS=-lintl")
                if not is_system_path(spec["gettext"].prefix):
                    args.append("LDFLAGS={0}".format(spec["gettext"].libs.search_flags))
        else:
            args.append("--disable-nls")

        return args

    def build(self, spec, prefix):
        make()
        if "+perl" in spec:
            make("swig-pl")
            with working_dir(join_path("subversion", "bindings", "swig", "perl", "native")):
                perl = spec["perl"].command
                perl("Makefile.PL", "INSTALL_BASE={0}".format(prefix))

    def check(self):
        make("check")
        if "+perl" in self.spec:
            make("check-swig-pl")

    def install(self, spec, prefix):
        make("install", parallel=False)
        if "+perl" in spec:
            make("install-swig-pl-lib")
            with working_dir(join_path("subversion", "bindings", "swig", "perl", "native")):
                make("install")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"^svn, version\s+([\d\.]+)", output)
        return match.group(1) if match else None
