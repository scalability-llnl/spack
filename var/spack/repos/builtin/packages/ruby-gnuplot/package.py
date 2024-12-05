# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyGnuplot(RubyPackage):
    """Utility library to aid in interacting with gnuplot from ruby"""

    homepage = "https://github.com/rdp/ruby_gnuplot"
    url = "https://rubygems.org/downloads/gnuplot-2.6.2.gem"

    # Source code is available at https://github.com/rdp/ruby_gnuplot
    # but release tarballs are not available, download gem instead

    version(
        "2.6.2",
        sha256="d2c28d4a55867ef6f0a5725ce157581917b4d27417bc3767c7c643a828416bb3",
        expand=False,
    )

    depends_on("gnuplot+X")
