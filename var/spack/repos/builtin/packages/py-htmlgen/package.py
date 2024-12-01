# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyHtmlgen(PythonPackage):
    """Library to generate HTML from classes."""

    homepage = "https://github.com/srittau/python-htmlgen"
    url = "https://github.com/srittau/python-htmlgen/archive/v1.2.2.tar.gz"

    license("MIT")

    version("1.2.2", sha256="9dc60e10511f0fd13014659514c6c333498c21779173deb585cd4964ea667770")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
