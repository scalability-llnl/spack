# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
    url      = "https://archive.apache.org/dist/tomcat/tomcat-9/v9.0.30/bin/apache-tomcat-9.0.30.tar.gz"

    version('9.0.30', sha256='43a9b268671bbd3aace427637fbf577e742b521901e111342321ae901478100b')
    version('9.0.29', sha256='1bf634413326ec96972fc1c3ac6666e8e4cab49ad3fc9f5e3228b85208d9c4b0')
    version('9.0.27', sha256='6616a150e1593ef1a622298aaef9b889db70c8ee5122d35ad52adfcda1084d10')
    version('9.0.26', sha256='b5430890d3b986d6b7ec6a6ef611f9451cbfa933b0a1a3dd48e2cd1f46a63381')
    version('9.0.24', sha256='22064138e25f7ab899802804775259a156c06770535b8ce93856beba13dfcf6d')

    def url_for_version(self, version):
        url = "https://archive.apache.org/dist/tomcat/tomcat-9/v{0}/bin/apache-tomcat-{0}.tar.gz"
        return url.format(version)

    def install(self, spec, prefix):
        install_tree('.', prefix)
