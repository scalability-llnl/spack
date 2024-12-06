# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySvgpathtools(PythonPackage):
    """A collection of tools for manipulating and analyzing SVG Path objects
    and Bezier curves."""

    pypi = "svgpathtools/svgpathtools-1.3.3.tar.gz"

    license("MIT")

    version("1.3.3", sha256="e4b3784ae41b725fbce6a33a8981210967b16d0b557cb5d98c0ed0c81f0f89b9")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-svgwrite", type=("build", "run"))
