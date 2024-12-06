# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Voms(AutotoolsPackage):
    """The VOMS native service and APIs."""

    homepage = "https://github.com/italiangrid/voms"
    url = "https://github.com/italiangrid/voms/archive/refs/tags/v2.1.0.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("2.1.0", sha256="2fd2468620af531c02e9ac495aaaf2a8d5b8cfbe24d4904f2e8fa7f64cdeeeec")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("openssl")
    depends_on("gsoap@2.7:")
    depends_on("expat")
    depends_on("zlib-api")

    force_autoreconf = True

    def patch(self):
        filter_file(
            r"/usr/bin/soapcpp2", f"{self.spec['gsoap'].prefix.bin.soapcpp2}", "m4/wsdl2h.m4"
        )

    def setup_build_environment(self, env):
        # https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=voms
        pkgconfig = Executable(join_path(self.spec["pkgconfig"].prefix.bin, "pkg-config"))
        env.set("GSOAP_SSL_PP_CFLAGS", pkgconfig("--cflags", "gsoapssl++", "zlib", output=str))
        env.set("GSOAP_SSL_PP_LIBS", pkgconfig("--libs", "gsoapssl++", "zlib", output=str))

    def autoreconf(self, spec, prefix):
        autogen = Executable("./autogen.sh")
        autogen()

    def configure_args(self):
        args = [f"--with-gsoap-wsdl2h={self.spec['gsoap'].prefix.bin.wsdl2h}"]
        return args
