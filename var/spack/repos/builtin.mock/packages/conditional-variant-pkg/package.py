# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ConditionalVariantPkg(Package):
    """This package is used to test conditional variants."""

    homepage = "http://www.example.com/conditional-variant-pkg"
    url = "http://www.unit-test-should-replace-this-url/conditional-variant-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")
    version("2.0", md5="abcdef0123456789abcdef0123456789")

    variant(
        "version_based",
        default=True,
        when="@2.0:",
        description="Check that version constraints work",
    )

    variant(
        "variant_based",
        default=False,
        when="+version_based",
        description="Check that variants can depend on variants",
    )

    variant("two_whens", default=False, when="@1.0")
    variant("two_whens", default=False, when="+variant_based")

    def install(self, spec, prefix):
        assert False
