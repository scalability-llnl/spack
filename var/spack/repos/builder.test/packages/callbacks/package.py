# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import spack.build_systems.generic
from spack.package import *


class Callbacks(Package):
    """Package used to verify that callbacks on phases work correctly, including conditions"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("2.0", md5="abcdef0123456789abcdef0123456789")
    version("1.0", md5="0123456789abcdef0123456789abcdef")


class GenericBuilder(spack.build_systems.generic.GenericBuilder):
    def install(self, pkg, spec, prefix):
        os.environ["CALLBACKS_INSTALL_CALLED"] = "1"
        os.environ["INSTALL_VALUE"] = "CALLBACKS"
        mkdirp(prefix.bin)

    @run_before("install")
    def before_install_1(self):
        os.environ["BEFORE_INSTALL_1_CALLED"] = "1"
        os.environ["TEST_VALUE"] = "1"

    @run_before("install")
    def before_install_2(self):
        os.environ["BEFORE_INSTALL_2_CALLED"] = "1"
        os.environ["TEST_VALUE"] = "2"

    @run_after("install")
    def after_install_1(self):
        os.environ["AFTER_INSTALL_1_CALLED"] = "1"
        os.environ["TEST_VALUE"] = "3"

    @run_after("install", when="@1.0")
    def after_install_2(self):
        os.environ["AFTER_INSTALL_2_CALLED"] = "1"
        os.environ["TEST_VALUE"] = "4"
