# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAudioread(PythonPackage):
    """cross-library (GStreamer + Core Audio + MAD + FFmpeg) audio decoding for
    Python."""

    homepage = "https://github.com/beetbox/audioread"
    pypi = "audioread/audioread-2.1.8.tar.gz"

    license("MIT")

    version("2.1.8", sha256="073904fabc842881e07bd3e4a5776623535562f70b1655b635d22886168dd168")

    depends_on("py-setuptools", type="build")
    # the following does not seem to be used for building but is listed in
    # setup.py
    depends_on("py-pytest-runner", type="build")
