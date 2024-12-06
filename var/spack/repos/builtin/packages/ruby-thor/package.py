# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyThor(RubyPackage):
    """Thor is a toolkit for building powerful command-line interfaces."""

    homepage = "http://whatisthor.com/"
    url = "https://github.com/erikhuda/thor/archive/v1.0.1.tar.gz"

    license("MIT")

    version("1.0.1", sha256="e6b902764e237ce296cf9e339c93f8ca83bec5b59be0bf8bacd7ffddc6684d07")

    depends_on("ruby@2.0.0:", type=("build", "run"))
