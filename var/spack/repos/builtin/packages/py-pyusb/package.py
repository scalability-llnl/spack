# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyusb(PythonPackage):
    """Easy USB access from Python."""

    homepage = "https://github.com/pyusb/pyusb"
    pypi = "pyusb/pyusb-1.0.2.tar.gz"

    license("BSD-3-Clause")

    version("1.0.2", sha256="4e9b72cc4a4205ca64fbf1f3fff39a335512166c151ad103e55c8223ac147362")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools-scm@:1", type="build", when="^py-setuptools@:11")
    depends_on("py-setuptools-scm", type="build")
    depends_on("libusb")
