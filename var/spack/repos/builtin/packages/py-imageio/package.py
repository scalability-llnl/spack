# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyImageio(PythonPackage):
    """Python library for reading and writing image data.

    Imageio is a Python library that provides an easy interface
    to read and write a wide range of image data, including animated
    images, video, volumetric data, and scientific formats. It is
    cross-platform, runs on Python 2.7 and 3.4+, and is easy to install."""

    homepage = "https://github.com/imageio/imageio"
    pypi = "imageio/imageio-2.3.0.tar.gz"

    license("BSD-2-Clause")

    version("2.35.1", sha256="4952dfeef3c3947957f6d5dedb1f4ca31c6e509a476891062396834048aeed2a")
    version("2.34.0", sha256="ae9732e10acf807a22c389aef193f42215718e16bd06eed0c5bb57e1034a4d53")
    version("2.30.0", sha256="7fc6ad5b5677cb1e58077875a72512aa8c392b6d40885eca0a6ab250efb4b8f4")
    version("2.22.0", sha256="a332d127ec387b2d3dca967fd065a90f1c1a4ba2343570b03fe2cebb6ed064ea")
    version("2.16.0", sha256="7f7d8d8e1eb6f8bb1d15e0dd93bee3f72026a4c3b96e9c690e42f403f7bdea3e")
    version("2.10.3", sha256="469c59fe71c81cdc41c84f842d62dd2739a08fac8cb85f5a518a92a6227e2ed6")
    version("2.9.0", sha256="52ddbaeca2dccf53ba2d6dec5676ca7bc3b2403ef8b37f7da78b7654bb3e10f0")
    version("2.5.0", sha256="42e65aadfc3d57a1043615c92bdf6319b67589e49a0aae2b985b82144aceacad")
    version("2.4.1", sha256="16b8077bc8a5fa7a58b3e744f7ecbb156d8c088132df31e0f4f546c98de3514a")
    version("2.3.0", sha256="c4fd5183c342d47fdc2e98552d14e3f24386021bbc3efedd1e3b579d7d249c07")

    # TODO: Add variants for plugins, and optional dependencies

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-numpy@1.20:", when="@2.16", type=("build", "run"))
    # https://github.com/imageio/imageio/issues/1077
    depends_on("py-numpy@:1", when="@:2.34.1", type=("build", "run"))
    depends_on("pil@8.3.2:", when="@2.10:", type=("build", "run"))
    depends_on("pil", type=("build", "run"))
    depends_on("ffmpeg", type="run")
