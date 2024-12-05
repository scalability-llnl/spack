# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUproot3(PythonPackage):
    """ROOT I/O in pure Python and Numpy.

    uproot is a reader and a writer of the ROOT file format using only Python
    and Numpy. Unlike the standard C++ ROOT implementation, uproot is only an
    I/O library, primarily intended to stream data into machine learning
    libraries in Python. Unlike PyROOT and root_numpy, uproot does not depend
    on C++ ROOT. Instead, it uses Numpy to cast blocks of data from the ROOT
    file as Numpy arrays."""

    homepage = "https://github.com/scikit-hep/uproot3"
    pypi = "uproot3/uproot3-3.14.4.tar.gz"

    version("3.14.4", sha256="4396746ba5ef9071bb0a9da53294e4613a7f4548218940f86496e79d682d20eb")

    depends_on("python@2.7:2.9,3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pytest-runner", type="build")
    depends_on("py-numpy@1.13.1:", type=("build", "run"))
    depends_on("py-awkward0", type=("build", "run"))
    depends_on("py-uproot3-methods", type=("build", "run"))
    depends_on("py-cachetools", type=("build", "run"))
