# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PySvgpath(PythonPackage):
    """svg.path is a collection of objects that implement the different path
    commands in SVG, and a parser for SVG path definitions.
    """

    homepage = "https://github.com/regebro/svg.path"
    pypi = "svg.path/svg.path-4.1.tar.gz"
    git = "https://github.com/regebro/svg.path.git"

    license("MIT")

    version("6.2", sha256="1a2159f9db898df93c4637cfd3ccaf7da1fd073f59fa9a5950c73e46d4aa1aca")
    version("4.1", sha256="7e6847ba690ff620e20f152818d52e1685b993aacbc41b321f8fee3d1cb427db")

    depends_on("py-setuptools", type="build")
