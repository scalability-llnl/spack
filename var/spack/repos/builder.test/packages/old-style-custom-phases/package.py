# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class OldStyleCustomPhases(AutotoolsPackage):
    """Package used to verify that old-style packages work correctly when defining custom
    phases (though it's not recommended for packagers to do so).
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("2.0", md5="abcdef0123456789abcdef0123456789")
    version("1.0", md5="0123456789abcdef0123456789abcdef")

    phases = ["configure"]

    def configure(self, spec, prefix):
        mkdirp(prefix.bin)

    @run_after("configure")
    def after_configure(self):
        os.environ["AFTER_CONFIGURE_CALLED"] = "1"
        os.environ["TEST_VALUE"] = "0"

    @run_after("install")
    def after_install(self):
        os.environ["AFTER_INSTALL_CALLED"] = "1"
        os.environ["TEST_VALUE"] = "1"
