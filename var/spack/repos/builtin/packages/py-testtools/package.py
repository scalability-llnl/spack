# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTesttools(PythonPackage):
    """Extensions to the Python standard library unit testing framework."""

    homepage = "https://github.com/testing-cabal/testtools"
    pypi = "testtools/testtools-2.3.0.tar.gz"

    license("MIT")

    version("2.3.0", sha256="5827ec6cf8233e0f29f51025addd713ca010061204fdea77484a2934690a0559")

    depends_on("py-setuptools", type="build")
