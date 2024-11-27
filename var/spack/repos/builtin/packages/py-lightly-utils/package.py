# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLightlyUtils(PythonPackage):
    """A utility package for lightly."""

    homepage = "https://www.lightly.ai/"
    pypi = "lightly_utils/lightly_utils-0.0.2.tar.gz"

    license("MIT")

    version("0.0.2", sha256="a351f3d600f0ab08d12f294725c6457ae000645cb0a1083d0845cb196ccfe698")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("pil", type=("build", "run"))
