# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyNarray(RubyPackage):
    """Numo::NArray is an Numerical N-dimensional Array class for fast
    processing and easy manipulation of multi-dimensional numerical data,
    similar to numpy.ndaray."""

    homepage = "https://masa16.github.io/narray/"
    url = "https://github.com/ruby-numo/numo-narray/archive/v0.9.1.8.tar.gz"
    git = "https://github.com/ruby-numo/numo-narray.git"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("0.9.1.8", sha256="48814c6ebf2c4846fcf6cfd2705a15a97a608960c1676cb6c7b5c9254b0dd51b")

    depends_on("c", type="build")  # generated

    depends_on("ruby@2.2:2", type=("build", "run"))
