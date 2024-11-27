# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPytestFlakes(PythonPackage):
    """py.test plugin for efficiently checking python source with pyflakes."""

    homepage = "https://github.com/asmeurer/pytest-flakes"
    pypi = "pytest-flakes/pytest-flakes-4.0.2.tar.gz"

    license("MIT")

    version("4.0.3", sha256="bf070c5485dad82d5b5f5d0eb08d269737e378492d9a68f5223b0a90924c7754")
    version("4.0.2", sha256="6733db47937d9689032876359e5ee0ee6926e3638546c09220e2f86b3581d4c1")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pytest@5:", type=("build", "run"))
    depends_on("py-pyflakes", type=("build", "run"))
