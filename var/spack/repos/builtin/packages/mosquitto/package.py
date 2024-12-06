# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mosquitto(CMakePackage):
    """Mosquitto is an open source implementation of a server
    for version 5.0, 3.1.1, and 3.1 of the MQTT protocol."""

    homepage = "https://mosquitto.org"
    git = "https://github.com/eclipse/mosquitto"
    url = "https://mosquitto.org/files/source/mosquitto-2.0.14.tar.gz"

    license("EPL-1.0 OR EPL-2.0")

    version("2.0.18", sha256="d665fe7d0032881b1371a47f34169ee4edab67903b2cd2b4c083822823f4448a")
    version("2.0.14", sha256="d0dde8fdb12caf6e2426b4f28081919a2fce3448773bdb8af0d3cd5fe5776925")
    version("1.6.15", sha256="5ff2271512f745bf1a451072cd3768a5daed71e90c5179fae12b049d6c02aa0f")
    version("1.5.11", sha256="4a3b8a8f5505d27a7a966dd68bfd76f1e69feb51796d1b46b7271d1bb5a1a299")
    version("1.4.15", sha256="7d3b3e245a3b4ec94b05678c8199c806359737949f4cfe0bf936184f6ca89a83")
    version("1.3.5", sha256="16eb3dbef183827665feee9288362c7352cd016ba04ca0402a0ccf857d1c2ab2")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("tls", default=True, description="Build with TLS support")
    variant("cjson", default=True, description="Build with cJSON support", when="@2.0.0:")
    variant("static", default=False, description="Build with static libraries", when="@1.5.0:")
    variant("c-ares", default=False, description="Build with c-ares support", when="@1.4.0:")
    variant("websocket", default=False, description="Build with websocket support", when="@1.4.0:")

    depends_on("openssl", when="+tls")
    depends_on("cjson", when="+cjson")
    depends_on("c-ares", when="+c-ares")
    depends_on("libwebsockets", when="+websocket")

    def cmake_args(self):
        args = [
            self.define("DOCUMENTATION", "no"),
            self.define_from_variant("WITH_CJSON", "cjson"),
            self.define_from_variant("WITH_TLS", "tls"),
            self.define_from_variant("WITH_STATIC_LIBRARIES", "static"),
            self.define_from_variant("WITH_SRV", "c-ares"),
            self.define_from_variant("WITH_WEBSOCKETS", "websocket"),
        ]
        return args
