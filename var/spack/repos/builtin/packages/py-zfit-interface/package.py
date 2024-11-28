# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyZfitInterface(PythonPackage):
    """
    zfit model fitting interface for HEP
    """

    homepage = "https://github.com/zfit/zfit-interface"
    pypi = "zfit_interface/zfit_interface-0.0.3.tar.gz"

    maintainers("jonas-eschle")
    license("BSD-3-Clause", checked_by="jonas-eschle")

    version("0.0.3", sha256="af7e8ed409f136187b2cd4def723504f9d619738668e963af388a79121239f74")

    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@3.4:+toml", type="build")
    depends_on("py-setuptools-scm-git-archive", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-uhi", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
