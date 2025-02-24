# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySimpervisor(PythonPackage):
    """
    simpervisor provides the SupervisedProcess class that provides async methods
    start, ready, terminate, and kill to manage it.
    """

    homepage = "https://github.com/jupyterhub/simpervisor"
    pypi = "simpervisor/simpervisor-0.4.tar.gz"

    license("BSD-3-Clause")

    version("0.4", sha256="cec79e13cdbd6edb04a5c98c1ff8d4bd9713e706c069226909a1ef0e89d393c5")

    depends_on("py-setuptools", type="build")
