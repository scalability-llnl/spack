# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class InvalidGithubPatchUrl(Package):
    """Package that has a GitHub patch URL that fails auditing."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/patch-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    patch(
        "https://github.com/spack/spack/commit/cc76c0f5f9f8021cfb7423a226bd431c00d791ce.patch",
        sha256="6057c3a8d50a23e93e5642be5a78df1e45d7de85446c2d7a63e3d0d88712b369",
    )
