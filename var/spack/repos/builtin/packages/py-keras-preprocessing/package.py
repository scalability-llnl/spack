# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKerasPreprocessing(PythonPackage):
    """Utilities for working with image data, text data, and sequence data."""

    homepage = "https://github.com/keras-team/keras-preprocessing"
    pypi = "Keras-Preprocessing/Keras_Preprocessing-1.1.2.tar.gz"

    license("MIT")

    version("1.1.2", sha256="add82567c50c8bc648c14195bf544a5ce7c1f76761536956c3d2978970179ef3")
    version("1.1.0", sha256="5a8debe01d840de93d49e05ccf1c9b81ae30e210d34dacbcc47aeb3049b528e5")
    version("1.0.9", sha256="5e3700117981c2db762e512ed6586638124fac5842170701628088a11aeb51ac")
    version("1.0.5", sha256="ef2e482c4336fcf7180244d06f4374939099daa3183816e82aee7755af35b754")
    version("1.0.4", sha256="452f8af8b2865e9d7d2f0dd5a3d0afd9e2ae2c6504f235b2447831c63303449f")
    version("1.0.3", sha256="02ba0a3b31ed89c4b0c21d55ba7d87529097d56f394e3850b6d3c9e6c63ce7ae")
    version("1.0.2", sha256="f5306554d2b454d825b36f35e327744f5477bd2ae21017f1a93b2097bed6757e")
    version("1.0.1", sha256="8649ba6377ecc06ea10e0a8a954df5600d115b4b626861e33c79b41ec03c5194")

    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.9.0:", type=("build", "run"))
    depends_on("py-numpy@1.9.1:", type=("build", "run"))
