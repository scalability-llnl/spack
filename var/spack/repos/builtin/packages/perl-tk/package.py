# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTk(PerlPackage):
    """Interface to Tk Graphics Library"""

    homepage = "https://metacpan.org/pod/distribution/Tk/Tk.pod"
    url = "https://cpan.metacpan.org/authors/id/S/SR/SREZIC/Tk-804.035.tar.gz"

    maintainers("cessenat")

    version("804.036", sha256="32aa7271a6bdfedc3330119b3825daddd0aa4b5c936f84ad74eabb932a200a5e")
    version("804.035", sha256="4d2b80291ba6de34d8ec886a085a6dbd2b790b926035a087e99025614c5ffdd4")
    version("804.033", sha256="84756e9b07a2555c8eecf88e63d5cbbba9b1aa97b1e71a3d4aa524a7995a88ad")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("perl-extutils-makemaker", type="build")
    depends_on("libx11")
    depends_on("libxcb")
    depends_on("libxft")
    depends_on("jpeg")
    depends_on("libpng")
    depends_on("freetype")
