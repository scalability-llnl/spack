# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOwslib(PythonPackage):
    """OWSLib is a Python package for client programming with Open Geospatial
    Consortium (OGC) web service (hence OWS) interface standards, and their
    related content models."""

    homepage = "http://http://geopython.github.io/OWSLib/#installation"
    pypi = "OWSLib/OWSLib-0.16.0.tar.gz"

    license("BSD-3-Clause")

    version("0.31.0", sha256="2ed6540087445cc57d905138a590b6ae58624ec7661b5c1682ed4e3303bcd150")
    version("0.25.0", sha256="20d79bce0be10277caa36f3134826bd0065325df0301a55b2c8b1c338d8d8f0a")
    version("0.17.1", sha256="b2e7fd694d3cffcee79317bad492d60c0aa887aea6916517c051c3247b33b5a5")
    version("0.16.0", sha256="ec95a5e93c145a5d84b0074b9ea27570943486552a669151140debf08a100554")

    depends_on("python@3.6:", when="@0.19.2:", type=("build", "run"))
    depends_on("python@3.5:", when="@0.19.1:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-lxml", when="@0.31:", type=("build", "run"))
    depends_on("py-python-dateutil@1.5:", type=("build", "run"))
    depends_on("py-pytz", type=("build", "run"))
    depends_on("py-pyyaml", when="@0.19.2:", type=("build", "run"))
    depends_on("py-requests@1:", type=("build", "run"))
    depends_on("py-pyproj@2:", when="@0.19.2:0.25", type=("build", "run"))
    depends_on("py-pyproj", when="@:0.25", type=("build", "run"))
