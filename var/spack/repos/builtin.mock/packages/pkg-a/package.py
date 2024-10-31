# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.build_systems.autotools
from spack.package import *


class PkgA(AutotoolsPackage):
    """Simple package with one optional dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")
    version("2.0", md5="abcdef0123456789abcdef0123456789")

    variant(
        "foo", description="", values=any_combination_of("bar", "baz", "fee").with_default("bar")
    )

    variant("foobar", values=("bar", "baz", "fee"), default="bar", description="", multi=False)

    variant("lorem_ipsum", description="", default=False)

    variant("bvv", default=True, description="The good old BV variant")

    depends_on("pkg-b", when="foobar=bar")
    depends_on("test-dependency", type="test")

    parallel = False


class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder):
    def with_or_without_fee(self, activated):
        if not activated:
            return "--no-fee"
        return "--fee-all-the-time"

    def autoreconf(self, pkg, spec, prefix):
        pass

    def configure(self, pkg, spec, prefix):
        pass

    def build(self, pkg, spec, prefix):
        pass

    def install(self, pkg, spec, prefix):
        # sanity_check_prefix requires something in the install directory
        # Test requires overriding the one provided by `AutotoolsPackage`
        mkdirp(prefix.bin)
