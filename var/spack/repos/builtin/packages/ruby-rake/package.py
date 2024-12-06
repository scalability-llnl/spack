# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyRake(RubyPackage):
    """Rake is a Make-like program implemented in Ruby."""

    homepage = "https://github.com/ruby/rake"
    url = "https://github.com/ruby/rake/archive/v13.0.1.tar.gz"

    license("MIT")

    version("13.0.6", sha256="a39d555a08a3cbd6961a98d0bf222a01018683760664ede3c1610af5ca5de0cc")
    version("13.0.1", sha256="d865329b5e0c38bd9d11ce70bd1ad6e0d5676c4eee74fd818671c55ec49d92fd")

    depends_on("c", type="build")  # generated

    depends_on("ruby@2.2:", type=("build", "run"))
