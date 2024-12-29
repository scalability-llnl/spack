# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tomcat(Package):
    """
    The Apache Tomcat software is an open source implementation of the
    Java Servlet, JavaServer Pages, Java Expression Language and Java
    WebSocket technologies.
    """

    homepage = "https://tomcat.apache.org/"
    url = (
        "https://archive.apache.org/dist/tomcat/tomcat-11/v11.0.0/bin/apache-tomcat-11.0.0.tar.gz"
    )

    license("Apache-2.0")

    version("11.0.0", sha256="d0ca319af349838f59009a9c5ed3709f02344201059dbc26dce4313ee969cd20")
    version("10.1.31", sha256="06f6e2e11ef5afb435a4b27e1e264ebcdbafd95389f5ee37e425dc135ed325d4")
    version(
        "9.0.96",
        sha256="bf4ad04955457ad663157876461015437a7479546aec9a38840d736b3d70151f",
        preferred=True,
    )
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2023-46589
        version(
            "9.0.30", sha256="43a9b268671bbd3aace427637fbf577e742b521901e111342321ae901478100b"
        )
        version(
            "9.0.29", sha256="1bf634413326ec96972fc1c3ac6666e8e4cab49ad3fc9f5e3228b85208d9c4b0"
        )
        version(
            "9.0.27", sha256="6616a150e1593ef1a622298aaef9b889db70c8ee5122d35ad52adfcda1084d10"
        )
        version(
            "9.0.26", sha256="b5430890d3b986d6b7ec6a6ef611f9451cbfa933b0a1a3dd48e2cd1f46a63381"
        )
        version(
            "9.0.24", sha256="22064138e25f7ab899802804775259a156c06770535b8ce93856beba13dfcf6d"
        )

    # https://tomcat.apache.org/whichversion.html
    depends_on("java@8:", type="run", when="@9:")
    depends_on("java@11:", type="run", when="@10:")
    depends_on("java@17:", type="run", when="@11:")

    def url_for_version(self, version):
        return f"https://archive.apache.org/dist/tomcat/tomcat-{version.up_to(1)}/v{version}/bin/apache-tomcat-{version}.tar.gz"

    def install(self, spec, prefix):
        install_tree(".", prefix)
