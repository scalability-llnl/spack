# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyMustache(RubyPackage):
    """Inspired by ctemplate and et, Mustache is a framework-agnostic way to
    render logic-free views."""

    homepage = "https://github.com/mustache/mustache"
    url = "https://github.com/mustache/mustache/archive/v1.1.1.tar.gz"

    license("MIT")

    version("1.1.1", sha256="9ab4a9842a37d5278789ba26152b0b78f649e3020266809ec33610a89f7e65ea")

    depends_on("ruby@2.0:", type=("build", "run"))
