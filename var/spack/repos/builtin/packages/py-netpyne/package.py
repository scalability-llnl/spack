# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNetpyne(PythonPackage):
    """Netpyne: A python package to facilitate the development,
    parallel simulation, optimization and analysis of multiscale
    biological neuronal networks in NEURON."""

    homepage = "https://www.netpyne.org/"
    url = "https://github.com/suny-downstate-medical-center/netpyne/archive/refs/tags/v1.0.3.1.tar.gz"
    git = "https://github.com/suny-downstate-medical-center/netpyne.git"

    license("MIT")

    version("master", branch="master")
    version("1.0.3.1", sha256="4f8492d58ff1dd7ec5ba6ed1f58f94548b8c1e4e9fd50b8a6d2e9f8eb400736d")

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-matplotlib@:3.5.1", type=("build", "run"))
    depends_on("py-matplotlib-scalebar", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-bokeh", type=("build", "run"))
    depends_on("py-schema", type=("build", "run"))
    depends_on("py-lfpykit", type=("build", "run"))
