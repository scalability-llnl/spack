# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openresty(AutotoolsPackage):
    """
    OpenResty is a full-fledged web application server by bundling the
    standard nginx core, lots of 3rd-party nginx modules, as well as
    most of their external dependencies.
    """

    homepage = "https://github.com/openresty"
    url = "https://github.com/openresty/openresty/releases/download/v1.15.8.2/openresty-1.15.8.2.tar.gz"

    license("BSD-2-Clause")

    version("1.25.3.1", sha256="32ec1a253a5a13250355a075fe65b7d63ec45c560bbe213350f0992a57cd79df")
    version("1.15.8.2", sha256="bf92af41d3ad22880047a8b283fc213d59c7c1b83f8dae82e50d14b64d73ac38")
    version("1.15.8.1", sha256="89a1238ca177692d6903c0adbea5bdf2a0b82c383662a73c03ebf5ef9f570842")
    version("1.13.6.2", sha256="946e1958273032db43833982e2cec0766154a9b5cb8e67868944113208ff2942")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("pcre", type="build")

    def configure_args(self):
        args = ["--without-http_rewrite_module"]
        return args
