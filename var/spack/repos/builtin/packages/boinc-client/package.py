# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BoincClient(AutotoolsPackage):
    """BOINC is a platform for high-throughput computing on a
    large scale (thousands or millions of computers). It can be
    used for volunteer computing (using consumer devices) or
    grid computing (using organizational resources). It
    supports virtualized, parallel, and GPU-based
    applications."""

    homepage = "https://boinc.berkeley.edu/"
    url = "https://github.com/BOINC/boinc/archive/client_release/7.16/7.16.5.tar.gz"

    license("LGPL-3.0-only")

    version("7.16.5", sha256="33db60991b253e717c6124cce4750ae7729eaab4e54ec718b9e37f87012d668a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("manager", default=False, description="Builds the client manager")
    variant("graphics", default=False, description="Graphic apps support")

    # Dependency documentation:
    # https://boinc.berkeley.edu/trac/wiki/SoftwarePrereqsUnix
    conflicts("%gcc@:3.0.4")

    depends_on("autoconf@2.58:", type="build")
    depends_on("automake@1.8:", type="build")
    depends_on("libtool@1.5:", type="build")
    depends_on("m4@1.4:", type="build")

    depends_on("curl@7.17.1:")
    depends_on("openssl@0.9.8:")

    depends_on("freeglut@3:", when="+graphics")
    depends_on("libsm", when="+graphics")
    depends_on("libice", when="+graphics")
    depends_on("libxmu", when="+graphics")
    depends_on("libxi", when="+graphics")
    depends_on("libx11", when="+graphics")
    depends_on("libjpeg", when="+graphics")

    depends_on("wxwidgets@3.0.0:", when="+manager")
    depends_on("libnotify", when="+manager")
    depends_on("sqlite@3.1:", when="+manager")

    patch("systemd-fix.patch")

    def configure_args(self):
        spec = self.spec
        args = []

        args.append("--disable-server")
        args.append("--enable-client")

        if spec.satisfies("+manager"):
            args.append("--enable-manager")
        else:
            args.append("--disable-manager")

        return args
