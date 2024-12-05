# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class Canfail(Package):
    """Package which fails install unless a special attribute is set"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    def set_install_succeed(self):
        os.environ["CANFAIL_SUCCEED"] = "1"

    def set_install_fail(self):
        os.environ.pop("CANFAIL_SUCCEED", None)

    @property
    def succeed(self):
        result = True if "CANFAIL_SUCCEED" in os.environ else False
        return result

    def install(self, spec, prefix):
        if not self.succeed:
            raise InstallError("'succeed' was false")
        touch(join_path(prefix, "an_installation_file"))
