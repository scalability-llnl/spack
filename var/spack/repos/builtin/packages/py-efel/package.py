# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyEfel(PythonPackage):
    """The Electrophys Feature Extract Library (eFEL) allows
    neuroscientists to automatically extract features from time series data
    recorded from neurons (both in vitro and in silico).
    Examples are the action potential width and amplitude in
    voltage traces recorded during whole-cell patch clamp experiments.
    The user of the library provides a set of traces and selects the
    features to be calculated. The library will then extract the requested
    features and return the values to the user."""

    homepage = "https://github.com/BlueBrain/eFEL"
    pypi = "efel/efel-3.0.80.tar.gz"

    license("LGPL-3.0-or-later")

    version("5.2.0", sha256="ed2c5efe22a4c703a4d9e47775b939009e1456713ac896898ebabf177c60b1dc")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.6:", type=("build", "run"))
