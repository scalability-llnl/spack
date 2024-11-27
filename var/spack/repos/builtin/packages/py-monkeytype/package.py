# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMonkeytype(PythonPackage):
    """Generating type annotations from sampled production types."""

    homepage = "https://github.com/instagram/MonkeyType"
    pypi = "MonkeyType/MonkeyType-22.2.0.tar.gz"

    license("BSD-3-Clause")

    version("22.2.0", sha256="6b0c00b49dcc5095a2c08d28246cf005e05673fc51f64d203f9a6bca2036dfab")

    depends_on("py-setuptools", type="build")
    depends_on("py-mypy-extensions", type=("build", "run"))
    depends_on("py-libcst@0.3.7:", type=("build", "run"))
