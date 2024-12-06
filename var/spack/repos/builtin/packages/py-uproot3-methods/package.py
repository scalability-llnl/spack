# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUproot3Methods(PythonPackage):
    """Pythonic mix-ins for ROOT classes.

    This package is typically used as a dependency for uproot 3.x, to define
    methods on the classes that are automatically generated from ROOT files.
    This includes histograms (TH*) and physics objects like TLorentzVectors.
    The reason it's a separate library is so that we can add physics-specific
    functionality on a shorter timescale than we can update Uproot 3 itself,
    which is purely an I/O package."""

    homepage = "https://github.com/scikit-hep/uproot3-methods"
    pypi = "uproot3-methods/uproot3-methods-0.10.1.tar.gz"

    version("0.10.1", sha256="dd68f90be1ea276360b96369836849df29045f7fe4e534f9ac21ea00798ee358")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.13.1:", type=("build", "run"))
    depends_on("py-awkward0", type=("build", "run"))
