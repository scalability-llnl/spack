# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySpectral(PythonPackage):
    """Spectral Python (SPy) is a pure Python module for processing
    hyperspectral image data (imaging spectroscopy data). It has functions for
    reading, displaying, manipulating, and classifying hyperspectral imagery.
    SPy is Free, Open Source Software (FOSS) distributed under the MIT
    License."""

    homepage = "http://www.spectralpython.net/"
    pypi = "spectral/spectral-0.22.4.tar.gz"

    license("MIT")

    version("0.22.4", sha256="b208ffd1042e32fd2276a35e098e3df26a5f6ff1310b829e97d222c66645a9af")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
