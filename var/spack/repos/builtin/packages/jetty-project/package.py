# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class JettyProject(MavenPackage):
    """Jetty is a lightweight highly scalable java based web
    server and servlet engine."""

    homepage = "https://www.eclipse.org/jetty"
    url = "https://github.com/eclipse/jetty.project/archive/jetty-9.4.31.v20200723.tar.gz"

    license("Apache-2.0")

    version(
        "9.4.31.v20200723",
        sha256="3cab80ddc14763764509552d79d5f1f17b565a3eb0a1951991d4a6fcfee9b4b1",
    )
    version(
        "9.4.30.v20200611",
        sha256="fac8bb95f8e8de245b284d359607b414893992ebb4e2b6e3ee40161297ea2111",
    )

    depends_on("java@8", type=("build", "run"))
    depends_on("maven@3:", type="build")
