# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJiter(PythonPackage):
    """Fast iterable JSON parser."""

    homepage = "https://github.com/pydantic/jiter/"
    pypi = "jiter/jiter-0.5.0.tar.gz"

    license("MIT", checked_by="qwertos")

    version("0.5.0", sha256="1d916ba875bcab5c5f7d927df998c4cb694d27dceddf3392e58beaf10563368a")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-maturin@1", type="build")
    depends_on("rust@1.73:", type=("build", "run"))
