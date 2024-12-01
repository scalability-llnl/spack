# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyRdiscount(RubyPackage):
    """Fast Implementation of Gruber's Markdown in C."""

    homepage = "https://dafoster.net/projects/rdiscount/"
    url = "https://github.com/davidfstr/rdiscount/archive/2.2.0.2.tar.gz"

    license("BSD-3-Clause")

    version("2.2.0.2", sha256="a6956059fc61365c242373b03c5012582d7342842eae38fe59ebc1bc169744db")

    depends_on("c", type="build")  # generated

    depends_on("ruby@1.9.3:", type=("build", "run"))
