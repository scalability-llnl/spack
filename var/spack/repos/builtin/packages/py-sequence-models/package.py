# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySequenceModels(PythonPackage):
    """Pytorch modules and utilities for modeling biological sequence data."""

    homepage = "https://github.com/microsoft/protein-sequence-models"
    pypi = "sequence-models/sequence-models-1.8.0.tar.gz"

    license("BSD-1-Clause")

    version("1.8.0", sha256="b031e8bc3edce60311000c2cfe237e533929ecffe6cf4364bd57f0178f541beb")
    depends_on("py-setuptools", type="build")
