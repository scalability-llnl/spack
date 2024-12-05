# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLfpykit(PythonPackage):
    """This Python module contain freestanding implementations of electrostatic forward models
    incorporated in LFPy"""

    homepage = "https://github.com/LFPy/LFPykit"
    pypi = "lfpykit/LFPykit-0.5.tar.gz"

    license("GPL-3.0-only")

    version("0.5", sha256="9a7ae80ad905bb8dd0eeab8517b43c3d5b4fff2b8766c9d5a36320a7a67bd545")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.15.2:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-meautility", type=("build", "run"))
