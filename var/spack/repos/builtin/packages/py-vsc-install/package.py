# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVscInstall(PythonPackage):
    """Shared setuptools functions and classes
    for Python libraries developed by HPC-UGent.
    """

    homepage = "https://github.com/hpcugent/vsc-install/"
    pypi = "vsc-install/vsc-install-0.10.25.tar.gz"

    license("LGPL-2.0-only")

    version("0.10.25", sha256="744fa52b45577251d94e9298ecb115afd295f2530eba64c524f469b5e283f19c")

    depends_on("py-setuptools", type=("build", "run"))
