# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RXml(RPackage):
    """Many approaches for both reading and creating XML (and HTML) documents
    (including DTDs), both local and accessible via HTTP or FTP. Also offers
    access to an 'XPath' "interpreter"."""

    homepage = "https://cloud.r-project.org/package=XML"
    url      = "https://cloud.r-project.org/src/contrib/XML_3.98-1.9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/XML"

    version('3.98-1.20', sha256='46af86376ea9a0fb1b440cf0acdf9b89178686a05c4b77728fcff1f023aa4858')
    version('3.98-1.19', sha256='81b1c4a2df24c5747fa8b8ec2d76b4e9c3649b56ca94f6c93fbd106c8a72beab')
    version('3.98-1.9', sha256='a3b70169cb2fbd8d61a41ff222d27922829864807e9ecad373f55ba0df6cf3c3')
    version('3.98-1.5', sha256='deaff082e4d37931d2dabea3a60c3d6916d565821043b22b3f9522ebf3918d35')
    version('3.98-1.4', sha256='9c0abc75312f66aac564266b6b79222259c678aedee9fc347462978354f11126')

    depends_on('r@2.13.0:', type=('build', 'run'))
    depends_on('libxml2@2.6.3:')
