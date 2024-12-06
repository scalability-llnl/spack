# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMultiecho(PythonPackage):
    """Combine multi-echoes from a multi-echo fMRI acquisition."""

    homepage = "https://github.com/Donders-Institute/multiecho"
    pypi = "multiecho/multiecho-0.28.tar.gz"

    license("MIT")

    version("0.29", sha256="df4860fe4478c162f976bdc4bdd2dc1c51ba2c33cb23658ac7218cf1597c4f0a")
    version("0.28", sha256="d0459bd03398547116d8e989b2d2b7922af0ae7ae77e233794dd7253a2abced3")

    depends_on("py-setuptools@62.2.0:", type="build", when="@0.29:")
    depends_on("py-setuptools", type="build")
    depends_on("py-argparse-manpage+setuptools", type="build", when="@0.29:")

    depends_on("py-coloredlogs", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-nibabel", type=("build", "run"))

    # Historical dependencies
    depends_on("python@3.6:3.9", type=("build", "run"), when="@0.28")
