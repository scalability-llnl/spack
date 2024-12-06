# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNitransforms(PythonPackage):
    """NiTransforms -- Neuroimaging spatial transforms in Python."""

    homepage = "https://github.com/poldracklab/nitransforms"
    pypi = "nitransforms/nitransforms-21.0.0.tar.gz"

    license("MIT")

    version("21.0.0", sha256="9e326a1ea5d5c6577219f99d33c1a680a760213e243182f370ce7e6b2476103a")
    version("20.0.0rc5", sha256="650eb12155f01fae099298445cc33721b9935d9c880f54ec486ec4adf3bffe6e")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools@42.0:", type="build")
    depends_on("py-setuptools-scm+toml@3.4:", type="build")
    depends_on("py-setuptools-scm-git-archive", type="build")
    depends_on("py-toml", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-nibabel@3.0:", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
