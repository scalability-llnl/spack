# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Liblzf(AutotoolsPackage):
    """LibLZF is a very small data compression library.

    It consists of only two .c and two .h files and is very easy to incorporate into
    your own programs. The compression algorithm is very, very fast, yet still written
    in portable C."""

    homepage = "http://oldhome.schmorp.de/marc/liblzf.html"
    url = "http://dist.schmorp.de/liblzf/liblzf-3.6.tar.gz"

    license("BSD-2-Clause")

    version("3.6", sha256="9c5de01f7b9ccae40c3f619d26a7abec9986c06c36d260c179cedd04b89fb46a")

    depends_on("c", type="build")  # generated
