# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySubwordNmt(PythonPackage):
    """This repository contains preprocessing scripts to segment text into
    subword units."""

    # pypi only has the whl file.
    homepage = "https://github.com/joeynmt/joeynmt"
    url = "https://github.com/rsennrich/subword-nmt/archive/refs/tags/v0.3.7.zip"

    license("MIT")

    version("0.3.7", sha256="5c3eafe8d85d872a3bbde722b130fb25db19cc7942561936bfae26b6daf51ba0")

    depends_on("py-setuptools", type="build")
