# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyXdg(RubyPackage):
    """Provides a Ruby implementation of the XDG Base Directory Specification."""

    homepage = "https://www.alchemists.io/projects/xdg/"
    url = "https://rubygems.org/downloads/xdg-2.2.5.gem"

    # Source code can be found at https://github.com/bkuhlmann/xdg and
    # https://github.com/rubyworks/xdg but I was unable to get it to build
    # from source

    license("Hippocratic-2.1")

    version(
        "2.2.5",
        sha256="f3a5f799363852695e457bb7379ac6c4e3e8cb3a51ce6b449ab47fbb1523b913",
        expand=False,
    )
