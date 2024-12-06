# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyImageioFfmpeg(PythonPackage):
    """The purpose of this project is to provide a simple and
    reliable ffmpeg wrapper for working with video files. It
    implements two simple generator functions for reading and
    writing data from/to ffmpeg, which reliably terminate the
    ffmpeg process when done. It also takes care of publishing
    platform-specific wheels that include the binary ffmpeg
    executables."""

    homepage = "https://github.com/imageio/imageio-ffmpeg"
    pypi = "imageio-ffmpeg/imageio-ffmpeg-0.4.3.tar.gz"

    license("BSD-2-Clause")

    version("0.4.5", sha256="f2ea4245a2adad25dedf98d343159579167e549ac8c4691cef5eff980e20c139")
    version("0.4.3", sha256="f826260a3207b872f1a4ba87ec0c8e02c00afba4fd03348a59049bdd8215841e")

    depends_on("python@3.4:", type=("build", "run"))
    depends_on("py-pip@19:", type="build")
    # Needs setuptools at runtime so that `import pkg_resources` succeeds
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("ffmpeg", type="run")
