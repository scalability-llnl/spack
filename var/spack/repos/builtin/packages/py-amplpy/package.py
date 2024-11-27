# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAmplpy(PythonPackage):
    """AMPL API is an interface that allows developers to access the features of
    the AMPL interpreter from within a programming language. All model generation
    and solver interaction is handled directly by AMPL, which leads to great
    stability and speed; the library just acts as an intermediary, and the
    added overhead (in terms of memory and CPU usage) depends mostly on how
    much data is read back from AMPL, the size of the model as such is irrelevant."""

    homepage = "https://ampl.com/"
    pypi = "amplpy/amplpy-0.8.6.tar.gz"

    license("BSD-3-Clause")

    version("0.8.6", sha256="ad0945d69f75e7762802bb54849009717fbcf226a6da6f37b539d9534bdcf68d")

    depends_on("cxx", type="build")  # generated

    depends_on("py-future@0.15.0:", type=("build", "run"))
    depends_on("py-ampltools@0.4.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
