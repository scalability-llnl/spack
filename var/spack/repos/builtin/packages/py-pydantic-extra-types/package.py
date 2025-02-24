# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydanticExtraTypes(PythonPackage):
    """A place for pydantic types that probably shouldn't
    exist in the main pydantic lib."""

    homepage = "https://github.com/pydantic/pydantic-extra-types"
    pypi = "pydantic_extra_types/pydantic_extra_types-2.10.0.tar.gz"

    license("MIT", checked_by="wdconinc")

    version("2.10.0", sha256="552c47dd18fe1d00cfed75d9981162a2f3203cf7e77e55a3d3e70936f59587b9")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-hatchling", type="build")
    depends_on("py-pydantic@2.5.2:", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
