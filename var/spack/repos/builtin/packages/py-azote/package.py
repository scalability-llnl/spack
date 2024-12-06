# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAzote(PythonPackage):
    """Azote is a GTK+3 - based picture browser and background setter,
    as the frontend to the swaybg (sway/Wayland) and feh (X windows)
    commands."""

    homepage = "https://github.com/nwg-piotr/azote"
    url = "https://github.com/nwg-piotr/azote/archive/v1.7.14.tar.gz"

    license("GPL-3.0-only")

    version("1.7.14", sha256="68f9be55858dc33650a6712f68c9e5d2c96be9d7ca380dbde8ea9b2895f3f22f")
    version("1.7.12", sha256="71d56784decf19b4e1a30943e054fd95f5044f7d471a65cecfef885ac8ef917e")
    version("1.7.11", sha256="d8f0a63c3dacf1cb5b7c4b0b23a4f9190fc3c94c499a98f4f0827cace4b855b5")

    depends_on("python@3.4.0:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
