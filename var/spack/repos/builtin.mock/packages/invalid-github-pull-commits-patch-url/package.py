# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class InvalidGithubPullCommitsPatchUrl(Package):
    """Package that has a GitHub pull request commit patch URL that fails auditing."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/patch-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    patch(
        "https://github.com/spack/spack/pull/1/commits/b4da28f71e2cef84c6e289afe89aa4bdf7936048.patch?full_index=1",
        sha256="eae9035b832792549fac00680db5f180a88ff79feb7d7a535b4fd71f9d885e73",
    )
