# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonFmask(PythonPackage):
    """A set of command line utilities and Python modules that implement
    the FMASK algorithm for Landsat and Sentinel-2"""

    homepage = "https://www.pythonfmask.org/en/latest/"
    url = "https://github.com/ubarsc/python-fmask/releases/download/pythonfmask-0.5.8/python-fmask-0.5.8.tar.gz"

    maintainers("gillins", "neilflood")

    license("GPL-3.0-only")

    version("0.5.9", sha256="7e2875abab87da545d3ec06b9dad704105729977ad1e479a3d9d3b8294c49e44")
    version("0.5.8", sha256="d55f54d3fecde818374017fdbe0ad173c893ef74c79ba2a7bc1890b7ec416c2f")
    version("0.5.7", sha256="da9dad1b977a50599d068dedaed007100b20322a79ca5d78f702712647c2c3f3")
    version("0.5.6", sha256="a63abd12d36fb4ec010e618bcabd5e2f782a0479ebcbf40aec1bcef943c00c5c")
    version("0.5.5", sha256="8257227d2527ea5fbd229f726d06d05986914beafd090acef05772a27dbbf062")
    version("0.5.4", sha256="ed20776f6b63615f664da89a9e3951c79437b66c2bf88fe19a93c2cc7dc40c82")

    depends_on("c", type="build")  # generated

    # Note: Dependencies are listed here: https://github.com/ubarsc/python-fmask/blob/master/doc/source/index.rst#introduction

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("py-rios", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("gdal+python", type=("build", "run"))
