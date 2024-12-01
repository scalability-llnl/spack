# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIopath(PythonPackage):
    """A library for providing I/O abstraction."""

    homepage = "https://github.com/facebookresearch/iopath"
    pypi = "iopath/iopath-0.1.10.tar.gz"

    license("MIT")

    version("0.1.10", sha256="3311c16a4d9137223e20f141655759933e1eda24f8bff166af834af3c645ef01")

    depends_on("py-setuptools", type="build")
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
    depends_on("py-portalocker", type=("build", "run"))
