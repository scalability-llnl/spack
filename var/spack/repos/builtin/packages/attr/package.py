# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Attr(AutotoolsPackage):
    """Commands for Manipulating Filesystem Extended Attributes"""

    homepage = "https://savannah.nongnu.org/projects/attr"
    url = "http://download.savannah.gnu.org/releases/attr/attr-2.4.47.src.tar.gz"

    license("LGPL-2.1-or-later")

    version("2.4.48", sha256="5ead72b358ec709ed00bbf7a9eaef1654baad937c001c044fe8b74c57f5324e7")
    version("2.4.47", sha256="25772f653ac5b2e3ceeb89df50e4688891e21f723c460636548971652af0a859")
    version("2.4.46", sha256="dcd69bdca7ff166bc45141eddbcf21967999a6b66b0544be12a1cc2fd6340e1f")

    depends_on("c", type="build")  # generated

    def url_for_version(self, version):
        if version >= Version("2.4.48"):
            url = "http://download.savannah.gnu.org/releases/attr/attr-{0}.tar.gz"
        else:
            url = "http://download.savannah.gnu.org/releases/attr/attr-{0}.src.tar.gz"
        return url.format(version)

    def configure_args(self):
        args = []
        args.append("--disable-static")
        return args

    # Ref. https://www.linuxfromscratch.org/blfs/view/7.5/postlfs/attr.html
    def install(self, spec, prefix):
        if self.version >= Version("2.4.48"):
            make("install")
        else:
            make("install", "install-dev", "install-lib")
