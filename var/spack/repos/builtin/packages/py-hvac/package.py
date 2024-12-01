# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHvac(PythonPackage):
    """HashiCorp Vault API client"""

    homepage = "https://github.com/hvac/hvac/"
    url = "https://github.com/hvac/hvac/archive/v0.2.17.tar.gz"

    license("Apache-2.0")

    version("0.9.6", sha256="ff60972edc512c73ac4811e91bcffccdb99f0d8975c0b41e44a4c79d73c711af")
    version("0.9.5", sha256="3e4af2d84833b8f61c9c3351d4a9799bf8e8e4344d0ad4e162609a7379961a16")
    version("0.9.4", sha256="ebb14b9a5b347c4f0b4dcea59f435dcc190d8ccb4cb9a20e5daf260af6509dd6")
    version("0.9.3", sha256="cac16bc089be9966f1fe5c108fb966949dc5bb4348cc1f5f54ebd8511c410ed4")
    version("0.2.17", sha256="a767be25fcb1165f4b28da3312a0bd196d1101c53c60fb99f899ff6c7b9aaa78")

    depends_on("py-setuptools", type="build")
    depends_on("py-requests@2.7.0:", type=("build", "run"))
    depends_on("py-requests@2.21.0:", type=("build", "run"), when="@0.9.3:")
    depends_on("py-six@1.5.0:", type=("build", "run"), when="@0.9.6:")
