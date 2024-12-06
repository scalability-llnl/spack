# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ConfigureWarning(AutotoolsPackage):
    """This package prints output that looks like an error during configure, but
    it actually installs successfully."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/configure-warning-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    parallel = False

    def autoreconf(self, spec, prefix):
        pass

    def configure(self, spec, prefix):
        print("foo: No such file or directory")
        return 0

    def build(self, spec, prefix):
        pass

    def install(self, spec, prefix):
        # sanity_check_prefix requires something in the install directory
        # Test requires overriding the one provided by `AutotoolsPackage`
        mkdirp(prefix.bin)
