# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestPylint(PythonPackage):
    """Run pylint with pytest and have configurable rule types (i.e.
    Convention, Warn, and Error) fail the build. You can also specify a
    pylintrc file.

    """

    homepage = "https://pypi.org/project/pytest-pylint/"
    pypi = "pytest-pylint/pytest-pylint-0.21.0.tar.gz"
    git = "https://github.com/pytest-dev/pytest"

    license("MIT")

    version("0.21.0", sha256="88764b8e1d5cfa18809248e0ccc2fc05035f08c35f0b0222ddcfea1c3c4e553e")

    # python_requires
    depends_on("python@3.7:", type=("build", "run"))

    # install_requires
    depends_on("py-setuptools", type=("build"))
    depends_on("py-pytest@7.0.0:", type=("build", "run"))
    depends_on("py-pylint@2.15.0:", type=("build", "run"))
    depends_on("py-tomli@1.1.0:", type=("build", "run"), when="^python@:3.10")
