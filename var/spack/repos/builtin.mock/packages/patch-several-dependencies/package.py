# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PatchSeveralDependencies(Package):
    """Package that requries multiple patches on a dependency."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/patch-a-dependency-1.0.tar.gz"

    version("2.0", md5="0123456789abcdef0123456789abcdef")
    version("1.0", md5="0123456789abcdef0123456789abcdef")

    variant("foo", default=False, description="Forces a version on libelf")

    # demonstrate all the different ways to patch things

    # single patch file in repo
    depends_on("libelf", patches="foo.patch")
    depends_on("libelf@0.8.10", patches="foo.patch", when="+foo")

    # using a list of patches in one depends_on
    depends_on(
        "libdwarf",
        patches=[
            patch("bar.patch"),  # nested patch directive
            patch("baz.patch", when="@20111030"),  # and with a conditional
        ],
        when="@1.0",
    )  # with a depends_on conditional

    # URL patches
    depends_on(
        "fake",
        patches=[
            # uncompressed URL patch
            patch(
                "http://example.com/urlpatch.patch",
                sha256="abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234",
            ),
            # compressed URL patch requires separate archive sha
            patch(
                "http://example.com/urlpatch2.patch.gz",
                archive_sha256="abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd",
                sha256="1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd",
            ),
        ],
    )
