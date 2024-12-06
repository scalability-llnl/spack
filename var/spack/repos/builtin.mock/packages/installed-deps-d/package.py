# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class InstalledDepsD(Package):
    """Used by test_installed_deps test case."""

    #     a
    #    / \
    #   b   c   b --> d build/link
    #   |\ /|   b --> e build/link
    #   |/ \|   c --> d build
    #   d   e   c --> e build/link

    homepage = "http://www.example.com"
    url = "http://www.example.com/d-1.0.tar.gz"

    version("1", md5="0123456789abcdef0123456789abcdef")
    version("2", md5="abcdef0123456789abcdef0123456789")
    version("3", md5="def0123456789abcdef0123456789abc")
