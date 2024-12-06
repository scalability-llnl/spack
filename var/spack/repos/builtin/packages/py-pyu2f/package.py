# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyu2f(PythonPackage):
    """U2F host library for interacting with a U2F device over USB."""

    homepage = "https://github.com/google/pyu2f"
    pypi = "pyu2f/pyu2f-0.1.5.tar.gz"

    license("Apache-2.0")

    version("0.1.5", sha256="a3caa3a11842fc7d5746376f37195e6af5f17c0a15737538bb1cebf656fb306b")

    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))
