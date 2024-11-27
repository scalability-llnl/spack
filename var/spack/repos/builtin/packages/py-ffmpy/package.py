# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFfmpy(PythonPackage):
    """A simple Python wrapper for ffmpeg"""

    homepage = "https://github.com/Ch00k/ffmpy"
    pypi = "ffmpy/ffmpy-0.3.0.tar.gz"

    license("MIT")

    version("0.3.0", sha256="757591581eee25b4a50ac9ffb9b58035a2794533db47e0512f53fb2d7b6f9adc")

    depends_on("py-setuptools", type="build")
    depends_on("ffmpeg", type="run")
