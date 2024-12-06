# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyYte(PythonPackage):
    """A YAML template engine with Python expressions."""

    homepage = "https://yte-template-engine.github.io"
    pypi = "yte/yte-1.5.1.tar.gz"

    maintainers("charmoniumQ")

    license("MIT")

    version("1.5.1", sha256="6d0b315b78af83276d78f5f67c107c84238f772a76d74f4fc77905b46f3731f5")

    # https://github.com/yte-template-engine/yte/blob/v1.5.1/pyproject.toml#L12
    depends_on("py-dpath@2", type=("build", "run"))
    depends_on("py-plac@1.3.4:1", type=("build", "run"))
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-pyyaml@6", type=("build", "run"))

    # https://github.com/yte-template-engine/yte/blob/v1.5.1/pyproject.toml#L41
    depends_on("py-poetry-core@1:", type="build")
