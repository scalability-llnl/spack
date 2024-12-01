# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyworld(PythonPackage):
    """PyWorld wrappers WORLD, which is a free software for high-quality speech
    analysis, manipulation and synthesis. It can estimate fundamental frequency
    (F0), aperiodicity and spectral envelope and also generate the speech like
    input speech with only estimated parameters.i"""

    homepage = "https://github.com/JeremyCCHsu/Python-Wrapper-for-World-Vocoder"
    pypi = "pyworld/pyworld-0.3.0.tar.gz"

    license("MIT")

    version("0.3.0", sha256="e19b5d8445e0c4fc45ded71863aeaaf2680064b4626b0e7c90f72e9ace9f6b5b")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@:1.19", type=("build", "run"))
    depends_on("py-cython@0.24.0:", type="build")
