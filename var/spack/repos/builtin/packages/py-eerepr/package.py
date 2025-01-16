# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEerepr(PythonPackage):
    """Code Editor-style reprs for Earth Engine data in a Jupyter notebook."""

    homepage = "https://github.com/aazuspan/eerepr"
    pypi = "eerepr/eerepr-0.1.0.tar.gz"

    license("MIT")

    version("0.1.0", sha256="a3c6f4d94ee19374aea2ff7ae9f2471f06649be5e18f9cb1cced8a00c2c20857")

    depends_on("py-hatchling", type="build")
    depends_on("py-earthengine-api", type=("build", "run"))
