# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDoit(PythonPackage):
    """doit - Automation Tool."""

    homepage = "https://pydoit.org/"
    pypi = "doit/doit-0.36.0.tar.gz"

    license("MIT")

    version("0.36.0", sha256="71d07ccc9514cb22fe59d98999577665eaab57e16f644d04336ae0b4bae234bc")

    depends_on("c", type="build")  # generated

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-cloudpickle", type=("build", "run"))
    depends_on("py-importlib-metadata@4.4:", type=("build", "run"))
