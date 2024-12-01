# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyscreeze(PythonPackage):
    """PyScreeze can take screenshots, save them to files, and
    locate images within the screen. This is useful if you have
    a small image of, say, a button that needs to be clicked
    and want to locate it on the screen."""

    homepage = "https://github.com/asweigart/pyscreeze"
    pypi = "PyScreeze/PyScreeze-0.1.27.tar.gz"

    license("MIT")

    version("0.1.27", sha256="cba2f264fe4b6c70510061cb2ba6e1da0e3bfecfdbe8a3b2cd6305a2afda9e6b")

    depends_on("python@2.7:2,3.2:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("pil", type=("build", "run"))
    depends_on("scrot", type="run")
