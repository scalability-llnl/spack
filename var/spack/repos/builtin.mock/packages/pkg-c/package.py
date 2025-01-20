# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PkgC(Package):
    """Simple package with no dependencies"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/c-1.0.tar.gz"

    # Needed to test CDash reporting
    phases = ["configure", "build", "install"]

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    def configure(self, spec, prefix):
        pass

    def build(self, spec, prefix):
        pass

    def install(self, spec, prefix):
        touch(prefix.pkg_c)
