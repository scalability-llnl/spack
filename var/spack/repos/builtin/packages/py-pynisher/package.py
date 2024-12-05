# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPynisher(PythonPackage):
    """A small Python library to limit the resources used by a
    function by executing it inside a subprocess."""

    homepage = "https://github.com/automl/pynisher"
    pypi = "pynisher/pynisher-0.6.4.tar.gz"

    license("MIT")

    version("0.6.4", sha256="111d91aad471375c0509a912415ff90053ef909100facf412511383af107c124")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-psutil", type=("build", "run"))
