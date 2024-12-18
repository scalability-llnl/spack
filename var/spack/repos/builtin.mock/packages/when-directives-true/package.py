# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class WhenDirectivesTrue(Package):
    """Package that tests True when specs on directives."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/example-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    patch(
        "https://example.com/foo.patch",
        sha256="abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234",
        when=True,
    )
    extends("extendee", when=True)
    depends_on("pkg-b", when=True)
    conflicts("@1.0", when=True)
    resource(
        url="http://www.example.com/example-1.0-resource.tar.gz",
        md5="0123456789abcdef0123456789abcdef",
        when=True,
    )
