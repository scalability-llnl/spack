# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyUmalqurra(PythonPackage):
    """Date Api that support Hijri Umalqurra calendar."""

    homepage = "https://github.com/tytkal/python-hijiri-ummalqura"
    pypi = "umalqurra/umalqurra-0.2.tar.gz"

    version("0.2", sha256="719f6a36f908ada1c29dae0d934dd0f1e1f6e3305784edbec23ad719397de678")

    depends_on("py-setuptools", type="build")
