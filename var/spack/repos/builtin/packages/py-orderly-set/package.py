# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOrderlySet(PythonPackage):
    """Orderly Set is a package containing multiple implementations of
    Ordered Set."""

    homepage = "https://github.com/seperman/orderly-set"
    pypi = "orderly_set/orderly_set-5.2.3.tar.gz"

    license("MIT", checked_by="wdconinc")

    version("5.2.3", sha256="571ed97c5a5fca7ddeb6b2d26c19aca896b0ed91f334d9c109edd2f265fb3017")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
