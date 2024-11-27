# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpythonClusterHelper(PythonPackage):
    """Quickly and easily parallelize Python functions using IPython on
    a cluster, supporting multiple schedulers. Optimizes IPython defaults
    to handle larger clusters and simultaneous processes.
    """

    homepage = "https://github.com/roryk/ipython-cluster-helper"
    url = "https://github.com/roryk/ipython-cluster-helper/archive/v0.6.4.tar.gz"

    license("MIT")

    version("0.6.4", sha256="6c8b42e1428305eeb0c54d1a8ecf3c551ec9ee02e1f039b4b12260bef66fc446")
    version("0.6.3", sha256="0256e6f72c31f846fd3bf7ed0a87bc362d77a0731cb52dbdc19c41686e44faeb")

    depends_on("py-setuptools@18.5:", type=("build", "run"))
    depends_on("py-pyzmq@2.1.11:", type=("build", "run"))
    depends_on("py-ipython@:5", type=("build", "run"))
    depends_on("py-ipyparallel@6.0.2:", type=("build", "run"))
    depends_on("py-netifaces@0.10.3:", type=("build", "run"))
    depends_on("py-six@1.10.0:", type=("build", "run"))
