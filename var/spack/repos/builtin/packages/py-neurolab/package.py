# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNeurolab(PythonPackage):
    """Simple and powerfull neural network library for python"""

    homepage = "http://neurolab.googlecode.com/"
    pypi = "neurolab/neurolab-0.3.5.tar.gz"

    version("0.3.5", sha256="96ec311988383c63664f3325668f27c30561cf4349e3bc5420665c042a3b9191")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
