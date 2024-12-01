# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAlabaster(PythonPackage):
    """Alabaster is a visually (c)lean, responsive, configurable theme
    for the Sphinx documentation system."""

    homepage = "https://alabaster.readthedocs.io/"
    pypi = "alabaster/alabaster-0.7.10.tar.gz"
    git = "https://github.com/sphinx-doc/alabaster.git"

    version("0.7.16", sha256="75a8b99c28a5dad50dd7f8ccdd447a121ddb3892da9e53d1ca5cca3106d58d65")
    version("0.7.13", sha256="a27a4a084d5e690e16e01e03ad2b2e552c61a65469419b907243193de1a84ae2")
    version("0.7.12", sha256="a661d72d58e6ea8a57f7a86e37d86716863ee5e92788398526d58b26a4e4dc02")
    version("0.7.10", sha256="37cdcb9e9954ed60912ebc1ca12a9d12178c26637abdf124e3cde2341c257fe0")
    version("0.7.9", sha256="47afd43b08a4ecaa45e3496e139a193ce364571e7e10c6a87ca1a4c57eb7ea08")

    depends_on("python@3.9:", when="@0.7.16:", type=("build", "run"))
    depends_on("py-flit-core@3.7:", when="@0.7.16:", type="build")
    depends_on("py-setuptools", when="@:0.7.13", type="build")
