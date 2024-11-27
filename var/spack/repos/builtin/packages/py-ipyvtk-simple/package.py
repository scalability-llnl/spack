# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpyvtkSimple(PythonPackage):
    """ipywidget for vtkRenderWindow."""

    homepage = "https://github.com/Kitware/ipyvtklink"
    pypi = "ipyvtk_simple/ipyvtk_simple-0.1.4.tar.gz"

    license("BSD-3-Clause")

    version("0.1.4", sha256="ffac12e9287affd7c31538ac7f2d2390c72342a73b31010735b275ca841ceaa5")

    depends_on("py-setuptools", type="build")
    depends_on("py-ipycanvas@0.5.0:", type=("build", "run"))
    depends_on("py-ipyevents@0.8.0:", type=("build", "run"))
    depends_on("py-ipywidgets", type=("build", "run"))
