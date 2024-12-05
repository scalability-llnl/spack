# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPykml(PythonPackage):
    """pyKML is a Python package for parsing and authoring KML documents.
    It is based on the lxml.objectify API which provides Pythonic access to
    XML documents.
    """

    pypi = "pykml/pykml-0.1.3.tar.gz"

    license("BSD-3-Clause")

    version("0.2.0", sha256="44a1892e7c2a649c8ae9f8e2899ff76cae79ec6749ffb64d11140b4e87d0f957")

    depends_on("py-setuptools", type="build")
    depends_on("py-lxml@3.3.6:", type=("build", "run"))
