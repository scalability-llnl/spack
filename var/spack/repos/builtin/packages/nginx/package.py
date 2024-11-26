# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nginx(AutotoolsPackage):
    """nginx [engine x] is an HTTP and reverse proxy server, a mail proxy
    server, and a generic TCP/UDP proxy server, originally written by Igor
    Sysoev."""

    homepage = "https://nginx.org/en/"
    url = "https://nginx.org/download/nginx-1.12.0.tar.gz"

    license("BSD-2-Clause")

    version("1.26.0", sha256="d2e6c8439d6c6db5015d8eaab2470ab52aef85a7bf363182879977e084370497")
    version("1.24.0", sha256="77a2541637b92a621e3ee76776c8b7b40cf6d707e69ba53a940283e30ff2f55d")
    version("1.23.4", sha256="d43300e36bb249a7e6edc60bca1b0fc372a0bafce2f346d76acfb677a8790fc0")
    version("1.23.3", sha256="75cb5787dbb9fae18b14810f91cc4343f64ce4c24e27302136fb52498042ba54")
    version("1.21.3", sha256="14774aae0d151da350417efc4afda5cce5035056e71894836797e1f6e2d1175a")
    version("1.15.6", sha256="a3d8c67c2035808c7c0d475fffe263db8c353b11521aa7ade468b780ed826cc6")
    version("1.13.8", sha256="8410b6c31ff59a763abf7e5a5316e7629f5a5033c95a3a0ebde727f9ec8464c5")
    version("1.12.0", sha256="b4222e26fdb620a8d3c3a3a8b955e08b713672e1bc5198d1e4f462308a795b30")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("openssl")
    depends_on("openssl@:1", when="@:1.21.2")
    depends_on("pcre")
    depends_on("zlib-api")

    conflicts("%gcc@8:", when="@:1.14")

    def configure_args(self):
        args = ["--with-http_ssl_module"]
        return args

    def setup_run_environment(self, env):
        """Prepend the sbin directory to PATH."""
        env.prepend_path("PATH", self.prefix.sbin)
