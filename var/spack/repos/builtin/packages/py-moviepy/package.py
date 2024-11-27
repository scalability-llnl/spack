# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMoviepy(PythonPackage):
    """MoviePy is a Python module for video editing, which can
    be used for basic operations (like cuts, concatenations,
    title insertions), video compositing (a.k.a. non-linear
    editing), video processing, or to create advanced effects.
    It can read and write the most common video formats,
    including GIF."""

    homepage = "https://zulko.github.io/moviepy/"
    pypi = "moviepy/moviepy-1.0.3.tar.gz"

    license("MIT")

    version("1.0.3", sha256="2884e35d1788077db3ff89e763c5ba7bfddbd7ae9108c9bc809e7ba58fa433f5")
    version("1.0.1", sha256="9d5b0a0e884c0eb92c431baa110e560059720aab15d2ef3e4cba3892c34cf1ed")

    depends_on("py-setuptools", type="build")
    depends_on("py-decorator@4.0.2:4", type=("build", "run"))
    depends_on("py-imageio@2.5:2", type=("build", "run"))
    depends_on("py-imageio-ffmpeg@0.2.0:", type=("build", "run"))
    depends_on("py-tqdm@4.11.2:4", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-requests@2.8.1:2", type=("build", "run"))
    depends_on("py-proglog@:1.0.0", type=("build", "run"))
