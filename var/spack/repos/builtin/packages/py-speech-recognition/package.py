# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySpeechRecognition(PythonPackage):
    """Library for performing speech recognition, with support
    for several engines and APIs, online and offline."""

    homepage = "https://github.com/Uberi/speech_recognition"
    url = "https://github.com/Uberi/speech_recognition/archive/refs/tags/3.8.1.tar.gz"

    license("BSD-3-Clause")

    version("3.8.1", sha256="82d3313db383409ddaf3e42625fb0c3518231a1feb5e2ed5473b10b3d5ece7bd")

    depends_on("python@2.6:2,3.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
