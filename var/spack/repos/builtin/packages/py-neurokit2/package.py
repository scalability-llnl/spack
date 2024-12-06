# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNeurokit2(PythonPackage):
    """The Python Toolbox for Neurophysiological Signal Processing.

    This package is the continuation of NeuroKit 1. It's a user-friendly
    package providing easy access to advanced biosignal processing routines.
    Researchers and clinicians without extensive knowledge of programming or
    biomedical signal processing can analyze physiological data with only two
    lines of code.
    """

    homepage = "https://github.com/neuropsychology/NeuroKit"
    pypi = "neurokit2/neurokit2-0.1.2.tar.gz"

    license("MIT")

    version("0.2.4", sha256="4699704f6890ae3510d5abf1deec86a59d793d31cda51b627f6eae65360d298f")
    version("0.2.2", sha256="0c33b060f9ac5ec8a6a0e23261fdbc36a98cb48e06142a1653fd12698806a952")
    version("0.1.5", sha256="4df48c0ce8971e32e32f36c2263986b00fd83da5eadaaa98e4bb5ab6bcd930e5")
    version("0.1.4.1", sha256="226bb04bb369d8bb87d99831f0a93cd8d0ed96fdc500f63de0b3550082876f6e")
    version("0.1.2", sha256="5ef40037c2d7078ecb713ab0b77b850267babf133856b59595de9613f29787bc")

    depends_on("py-setuptools@40.6.0:", type="build")
    depends_on("py-pytest-runner", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-scikit-learn@1:", when="@0.2:", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
