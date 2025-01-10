# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsdfTransformSchemas(PythonPackage):
    """ASDF schemas for transforms"""

    homepage = "https://asdf-transform-schemas.readthedocs.io"
    pypi = "asdf_transform_schemas/asdf_transform_schemas-0.3.0.tar.gz"

    maintainers("lgarrison")

    license("BSD-3-Clause")

    version("0.3.0", sha256="0cf2ff7b22ccb408fe58ddd9b2441a59ba73fe323e416d59b9e0a4728a7d2dd6")

    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@3.4: +toml", type="build")

    depends_on("py-asdf-standard@1.0.1:", type=("build", "run"))
    depends_on("py-importlib-resources@3:", type=("build", "run"), when="^python@:3.8")
