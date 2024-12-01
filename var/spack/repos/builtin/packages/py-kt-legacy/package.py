# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKtLegacy(PythonPackage):
    """This repository is to support the deprecated import name of Keras Tuner.
    With this repo, you can import Keras Tuner as kerastuner. In the main Keras
    Tuner repository the import name has been changed to keras_tuner."""

    homepage = "https://github.com/haifeng-jin/kt-legacy"
    pypi = "kt-legacy/kt-legacy-1.0.4.tar.gz"

    license("Apache-2.0")

    version("1.0.4", sha256="a94112e42a50e7cc3aad31f3287aa384c23555ea1432c55b5823852e09e706cf")

    depends_on("py-setuptools", type="build")
