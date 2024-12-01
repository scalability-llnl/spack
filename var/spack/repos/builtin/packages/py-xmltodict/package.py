# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXmltodict(PythonPackage):
    """xmltodict is a Python module that makes working with XML feel like
    you are working with JSON."""

    homepage = "https://github.com/martinblech/xmltodict"
    pypi = "xmltodict/xmltodict-0.12.0.tar.gz"

    license("MIT")

    version("0.12.0", sha256="50d8c638ed7ecb88d90561beedbf720c9b4e851a9fa6c47ebd64e99d166d8a21")

    depends_on("py-setuptools", type="build")
    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
