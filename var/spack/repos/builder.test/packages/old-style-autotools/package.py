# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class OldStyleAutotools(AutotoolsPackage):
    """Package used to verify that old-style packages work correctly when executing the
    installation procedure.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("2.0", md5="abcdef0123456789abcdef0123456789")
    version("1.0", md5="0123456789abcdef0123456789abcdef")

    def configure(self, spec, prefix):
        pass

    def build(self, spec, prefix):
        pass

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

    def configure_args(self):
        """This override a function in the builder and construct the result using a method
        defined in this class and a super method defined in the builder.
        """
        return [self.foo()] + super().configure_args()

    def foo(self):
        return "--with-foo"

    @run_before("autoreconf")
    def create_configure(self):
        mkdirp(self.configure_directory)
        touch(self.configure_abs_path)

    @run_after("autoreconf", when="@1.0")
    def after_autoreconf_1(self):
        os.environ["AFTER_AUTORECONF_1_CALLED"] = "1"

    @run_after("autoreconf", when="@2.0")
    def after_autoreconf_2(self):
        os.environ["AFTER_AUTORECONF_2_CALLED"] = "1"

    def check(self):
        os.environ["CHECK_CALLED"] = "1"

    def installcheck(self):
        os.environ["INSTALLCHECK_CALLED"] = "1"
