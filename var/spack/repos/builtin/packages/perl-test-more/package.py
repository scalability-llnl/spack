# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestMore(PerlPackage):
    """Test2 is a new testing framework produced by forking Test::Builder,
    completely refactoring it, adding many new features and capabilities."""

    homepage = "https://github.com/Test-More/test-more"
    url = "https://github.com/Test-More/test-more/archive/v1.302183.tar.gz"

    license("Artistic-1.0")

    version("1.302183", sha256="1356ec24c5ab3f7ad8327091ddc6ace164a27767be10325776bf9743360ab4f7")
    version("1.302182", sha256="60727db9435cb244f6dcf4ca598c8ef39ac3035a0c36fd5c9c5b89be4f138366")
    version("1.302181", sha256="acb3c990d646928e7571c140510d7424716d3281c4064b1787294e72b39f61ce")
    version("1.302180", sha256="4dbed31e9434d74427b41a17ca3e0511a81ee5cb1240408c7f439c6449672a20")
