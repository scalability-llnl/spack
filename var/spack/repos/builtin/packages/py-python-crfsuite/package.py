# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonCrfsuite(PythonPackage):
    """python-crfsuite is a python binding to CRFsuite."""

    homepage = "https://github.com/scrapinghub/python-crfsuite"
    pypi = "python-crfsuite/python-crfsuite-0.9.7.tar.gz"

    license("MIT")

    version("0.9.7", sha256="3b4538d2ce5007e4e42005818247bf43ade89ef08a66d158462e2f7c5d63cee7")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type="build")
