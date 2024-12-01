# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLibrosa(PythonPackage):
    """A python package for music and audio analysis."""

    homepage = "https://github.com/librosa/librosa"
    pypi = "librosa/librosa-0.7.2.tar.gz"

    license("ISC")

    version("0.9.1", sha256="7ed5d6e3f4546e5e3c2840691f9ddc56878f914a35a50060df5fca2b26d4b614")
    version("0.7.2", sha256="656bbda80e98e6330db1ead79cd084b13a762284834d7603fcf7cf7c0dc65f3c")

    depends_on("python@3.6:", type=("build", "run"), when="@0.9.1:")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@48:", type="build", when="@0.9.1:")
    depends_on("py-wheel@0.29:", type="build", when="@0.9.1:")
    depends_on("py-audioread@2.0.0:", type=("build", "run"))
    depends_on("py-audioread@2.1.5:", type=("build", "run"), when="@0.9.1:")
    depends_on("py-numpy@1.15.0:", type=("build", "run"))
    depends_on("py-numpy@1.17.0:", type=("build", "run"), when="@0.9.1:")
    depends_on("py-scipy@1.0.0:", type=("build", "run"))
    depends_on("py-scipy@1.2.0:", type=("build", "run"), when="@0.9.1:")
    depends_on("py-scikit-learn@0.14.0:0.18,0.19.1:", type=("build", "run"))
    depends_on("py-scikit-learn@0.19.1:", type=("build", "run"), when="@0.9.1:")
    depends_on("py-joblib@0.12:", type=("build", "run"))
    depends_on("py-joblib@0.14:", type=("build", "run"), when="@0.9.1:")
    depends_on("py-decorator@3.0.0:", type=("build", "run"))
    depends_on("py-decorator@4.0.10:", type=("build", "run"), when="@0.9.1:")
    depends_on("py-six@1.3:", type=("build", "run"), when="@0.7.2")
    depends_on("py-resampy@0.2.2:", type=("build", "run"))
    depends_on("py-numba@0.43.0:", type=("build", "run"))
    depends_on("py-numba@0.45.1:", type=("build", "run"), when="@0.9.1:")
    depends_on("py-soundfile@0.9.0:", type=("build", "run"))
    depends_on("py-soundfile@0.10.2:", type=("build", "run"), when="@0.9.1:")
    depends_on("py-pooch@1:", type=("build", "run"), when="@0.9.1:")
    depends_on("py-packaging@20:", type=("build", "run"), when="@0.9.1:")
