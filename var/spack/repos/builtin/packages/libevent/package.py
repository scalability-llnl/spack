# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libevent(AutotoolsPackage):
    """The libevent API provides a mechanism to execute a callback function
    when a specific event occurs on a file descriptor or after a
    timeout has been reached. Furthermore, libevent also support
    callbacks due to signals or regular timeouts.

    """

    homepage = "https://libevent.org"
    url = "https://github.com/libevent/libevent/releases/download/release-2.1.8-stable/libevent-2.1.8-stable.tar.gz"
    list_url = "https://libevent.org/old-releases.html"

    license("BSD-3-Clause")

    version("2.1.12", sha256="92e6de1be9ec176428fd2367677e61ceffc2ee1cb119035037a27d346b0403bb")
    version("2.1.11", sha256="a65bac6202ea8c5609fd5c7e480e6d25de467ea1917c08290c521752f147283d")
    version("2.1.10", sha256="e864af41a336bb11dab1a23f32993afe963c1f69618bd9292b89ecf6904845b0")
    version("2.1.8", sha256="965cc5a8bb46ce4199a47e9b2c9e1cae3b137e8356ffdad6d94d3b9069b71dc2")
    version("2.0.22", sha256="71c2c49f0adadacfdbe6332a372c38cf9c8b7895bb73dabeaa53cdcc1d4e1fa3")
    version("2.0.21", sha256="22a530a8a5ba1cb9c080cba033206b17dacd21437762155c6d30ee6469f574f5")
    version("2.0.20", sha256="10698a0e6abb3ca00b1c9e8cfddc66933bcc4c9c78b5600a7064c4c3ef9c6a24")
    version("2.0.19", sha256="1591fb411a67876a514a33df54b85417b31e01800284bcc6894fc410c3eaea21")
    version("2.0.18", sha256="44ed97277715b24ef3b36e93d8c1d39ae80c29c7723793911e22dc6e0c3c4acb")
    version("2.0.17", sha256="51735d1241f9f6d2d6465d8abc76f7511764f6de7d81026120c629612296faa6")
    version("2.0.16", sha256="a578c7bcaf3bab1cc7924bd4d219f2ea621ab8c51dfc4f886e234b6ef4d38295")
    version("2.0.15", sha256="ab535bae9af788c8711a8d138c4cae0722f22a1a4ac4d8084abc7b0e0468bc5c")
    version("2.0.14", sha256="3c97a72cddd5bff63450efe7c646e15ad08dec32d5223b69cb10c2dc305812da")
    version("2.0.13", sha256="e2cc3b9f03e68ff878919b1cd031a210ba9ff376283d895161afcbc25aca00a9")
    version("2.0.12", sha256="ac0283f72e0f881e93ac3ae9497a20c78bd075c6c12506ad10e821aa1c29e5ab")

    depends_on("c", type="build")  # generated

    variant(
        "openssl", default=True, description="Build with encryption enabled at the libevent level."
    )
    # Versions before 2.1 do not build with OpenSSL 1.1
    depends_on("openssl@:1.0", when="@:2.0+openssl")
    depends_on("openssl", when="+openssl")

    def url_for_version(self, version):
        if version >= Version("2.0.22"):
            url = "https://github.com/libevent/libevent/releases/download/release-{0}-stable/libevent-{0}-stable.tar.gz"
        else:
            url = "https://github.com/downloads/libevent/libevent/libevent-{0}-stable.tar.gz"

        return url.format(version)

    @property
    def libs(self):
        libs = find_libraries("libevent", root=self.prefix, shared=True, recursive=True)
        return LibraryList(libs)

    def configure_args(self):
        spec = self.spec
        configure_args = []
        if spec.satisfies("+openssl"):
            configure_args.append("--enable-openssl")
        else:
            configure_args.append("--disable-openssl")

        return configure_args

    def patch(self):
        if self.spec.satisfies("%nvhpc"):
            # Remove incompatible compiler flags
            filter_file(" -Wmissing-declarations", "", "configure")
            filter_file(" -Wbad-function-cast", "", "configure")
            filter_file(" -Wno-unused-parameter", "", "configure")
            filter_file(" -Wmissing-field-initializers", "", "configure")
            filter_file(" -Waddress", "", "configure")
            filter_file(" -Wnormalized=id", "", "configure")
            filter_file(" -Woverride-init", "", "configure")
            filter_file(" -Wlogical-op", "", "configure")
