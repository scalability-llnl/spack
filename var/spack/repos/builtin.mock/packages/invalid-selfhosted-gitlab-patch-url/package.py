# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class InvalidSelfhostedGitlabPatchUrl(Package):
    """Package that has GitLab patch URLs that fail auditing."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/patch-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    patch(
        "https://gitlab.gnome.org/GNOME/glib/-/commit/bda87264372c006c94e21ffb8ff9c50ecb3e14bd.patch",
        sha256="2e811ec62cb09044c95a4d0213993f09af70cdcc1c709257b33bc9248ae950ed",
    )
