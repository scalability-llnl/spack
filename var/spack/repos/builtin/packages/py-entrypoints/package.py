# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEntrypoints(PythonPackage):
    """Discover and load entry points from installed packages."""

    homepage = "https://github.com/takluyver/entrypoints"
    pypi = "entrypoints/entrypoints-0.2.3.tar.gz"

    license("MIT")

    version("0.4", sha256="b706eddaa9218a19ebcd67b56818f05bb27589b1ca9e8d797b74affad4ccacd4")
    version("0.3", sha256="c70dd71abe5a8c85e55e12c19bd91ccfeec11a6e99044204511f9ed547d48451")
    version("0.2.3", sha256="d2d587dde06f99545fb13a383d2cd336a8ff1f359c5839ce3a64c917d10c029f")

    depends_on("python@3.6:", when="@0.4:", type=("build", "run"))
    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-flit-core@2:3", when="@0.4:", type="build")
    depends_on("py-flit", when="@:0.3", type="build")
