# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyRubyinline(RubyPackage):
    """Inline allows you to write foreign code within your ruby code."""

    homepage = "https://www.zenspider.com/projects/rubyinline.html"
    url = "https://rubygems.org/downloads/RubyInline-3.12.5.gem"

    # Source code available at https://github.com/seattlerb/rubyinline
    # but I had trouble getting the Rakefile to build

    version(
        "3.12.5",
        sha256="d4559cb86b7fedd2e9b4b0a3bd99a1955186dbc09f1269920a0dd5c67639c156",
        expand=False,
    )

    depends_on("ruby-zentest@4.3:4", type=("build", "run"))
