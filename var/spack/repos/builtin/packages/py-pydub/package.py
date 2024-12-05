# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydub(PythonPackage):
    """Manipulate audio with an simple and easy high level interface"""

    homepage = "http://pydub.com/"
    pypi = "pydub/pydub-0.25.1.tar.gz"

    license("MIT")

    version("0.25.1", sha256="980a33ce9949cab2a569606b65674d748ecbca4f0796887fd6f46173a7b0d30f")

    depends_on("py-setuptools", type="build")
    depends_on("ffmpeg", type="run")
