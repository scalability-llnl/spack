# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyRonn(RubyPackage):
    """Ronn builds manuals. It converts simple, human readable textfiles to
    roff for terminal display, and also to HTML for the web."""

    homepage = "https://rtomayko.github.io/ronn/"
    url = "https://github.com/rtomayko/ronn/archive/0.7.3.tar.gz"

    license("MIT")

    version("0.7.3", sha256="808aa6668f636ce03abba99c53c2005cef559a5099f6b40bf2c7aad8e273acb4")
    version("0.7.0", sha256="ea14337093de8707aa8a67b97357332fa8a03b0df722bdbf4f027fbe4379b185")

    depends_on("ruby-hpricot@0.8.2:", type=("build", "run"))
    depends_on("ruby-rdiscount@1.5.8:", type=("build", "run"))
    depends_on("ruby-mustache@0.7.0:", type=("build", "run"))
