# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class InvalidGitlabPatchUrl(Package):
    """Package that has GitLab patch URLs that fail auditing."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/patch-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    patch(
        "https://gitlab.com/QEF/q-e/-/commit/4ca3afd4c6f27afcf3f42415a85a353a7be1bd37.patch",
        sha256="d7dec588efb5c04f99d949d8b9bb4a0fbc98b917ae79e12e4b87ad7c3dc9e268",
    )
