# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHyperlink(PythonPackage):
    """A featureful, immutable, and correct URL for Python."""

    homepage = "https://github.com/python-hyper/hyperlink"
    pypi = "hyperlink/hyperlink-21.0.0.tar.gz"

    license("MIT")

    version("21.0.0", sha256="427af957daa58bc909471c6c40f74c5450fa123dd093fc53efd2e91d2705a56b")

    depends_on("python@2.6:2,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-idna@2.5:", type=("build", "run"))
