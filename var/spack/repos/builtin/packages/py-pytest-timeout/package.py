# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPytestTimeout(PythonPackage):
    """A plugin which will terminate tests after a certain timeout,
    assuming the test session isn't being debugged."""

    homepage = "https://github.com/pytest-dev/pytest-timeout/"
    pypi = "pytest-timeout/pytest-timeout-1.4.2.tar.gz"

    license("MIT")

    version("2.2.0", sha256="3b0b95dabf3cb50bac9ef5ca912fa0cfc286526af17afc806824df20c2f72c90")
    version("1.4.2", sha256="20b3113cf6e4e80ce2d403b6fb56e9e1b871b510259206d40ff8d609f48bda76")

    depends_on("py-setuptools", type="build")
    depends_on("py-pytest@5:", when="@2:", type=("build", "run"))
    depends_on("py-pytest@3.6.0:", type=("build", "run"))
