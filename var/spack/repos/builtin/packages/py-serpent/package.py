# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

# Package automatically generated using 'pip2spack' converter


class PySerpent(PythonPackage):
    """
    Serialization based on ast.literal_eval
    """

    homepage = "https://github.com/irmen/Serpent"
    pypi = "serpent/serpent-1.40.tar.gz"
    maintainers("liuyangzhuan")

    license("MIT")

    version("1.40", sha256="10b34e7f8e3207ee6fb70dcdc9bce473851ee3daf0b47c58aec1b48032ac11ce")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.2:", type=("build", "run"))
