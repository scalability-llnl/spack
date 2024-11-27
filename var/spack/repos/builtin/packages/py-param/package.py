# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyParam(PythonPackage):
    """Param is a library providing Parameters: Python attributes extended to have
    features such as type and range checking, dynamically generated values,
    documentation strings, default values, etc., each of which is inherited from
    parent classes if not specified in a subclass."""

    homepage = "https://param.holoviz.org/"
    pypi = "param/param-1.12.0.tar.gz"

    maintainers("haralmha")

    license("BSD-3-Clause")

    version("1.12.0", sha256="35d0281c8e3beb6dd469f46ff0b917752a54bed94d1b0c567346c76d0ff59c4a")

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
