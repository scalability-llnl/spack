# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytoml(PythonPackage):
    """A parser for TOML-0.4.0.

    Deprecated: use py-toml instead."""

    homepage = "https://github.com/avakar/pytoml"
    pypi = "pytoml/pytoml-0.1.21.tar.gz"

    license("MIT")

    version("0.1.21", sha256="8eecf7c8d0adcff3b375b09fe403407aa9b645c499e5ab8cac670ac4a35f61e7")

    depends_on("py-setuptools", type="build")
