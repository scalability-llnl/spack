# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBitstruct(PythonPackage):
    """This module is intended to have a similar interface as the python
    struct module, but working on bits instead of primitive data types
    (char, int, ...)"""

    homepage = "https://github.com/eerimoq/bitstruct"
    pypi = "bitstruct/bitstruct-8.17.0.tar.gz"

    maintainers("DaxLynch")

    license("MIT")

    version("8.17.0", sha256="eb94b40e4218a23aa8f90406b836a9e6ed83e48b8d112ce3f96408463bd1b874")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
