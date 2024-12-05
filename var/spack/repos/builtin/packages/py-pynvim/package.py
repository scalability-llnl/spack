# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPynvim(PythonPackage):
    """Neovim python client"""

    homepage = "https://pynvim.readthedocs.io/en/latest/"
    pypi = "pynvim/pynvim-0.4.3.tar.gz"

    maintainers("trws")

    license("Apache-2.0")

    version("0.4.3", sha256="3a795378bde5e8092fbeb3a1a99be9c613d2685542f1db0e5c6fd467eed56dff")

    depends_on("py-setuptools", type="build")
    depends_on("py-greenlet", type=("build", "run"))

    depends_on("py-msgpack@0.5:", type=("build", "run"))
