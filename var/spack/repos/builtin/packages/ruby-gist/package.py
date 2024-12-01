# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RubyGist(RubyPackage):
    """The gist gem provides a gist command that you can use from your terminal to upload content to https://gist.github.com/."""

    homepage = "https://github.com/defunkt/gist"
    url = "https://rubygems.org/downloads/gist-6.0.0.gem"

    version(
        "6.0.0",
        sha256="0d0a3616b1a4eec837ce4e5b5477bc809d58597ee350b2c34104acd3b00ccd62",
        expand=False,
    )

    depends_on("ruby@1.8:2", type=("build", "run"))
