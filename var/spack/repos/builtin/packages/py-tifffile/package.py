# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTifffile(PythonPackage):
    """Read and write image data from and to TIFF files."""

    homepage = "https://github.com/cgohlke/tifffile"
    pypi = "tifffile/tifffile-0.12.1.tar.gz"

    license("BSD-3-Clause")

    version("2024.8.30", sha256="2c9508fe768962e30f87def61819183fb07692c258cb175b3c114828368485a4")
    version("2023.8.30", sha256="6a8c53b012a286b75d09a1498ab32f202f24cc6270a105b5d5911dc4426f162a")
    version(
        "2022.10.10", sha256="50b61ba943b866d191295bc38a00191c9fdab23ece063544c7f1a264e3f6aa8e"
    )
    version("2022.4.8", sha256="d4a4057e5cb7afe6e24cf7bde42a163970b593afe44c17249894ede755cf3faa")
    version("2021.11.2", sha256="153e31fa1d892f482fabb2ae9f2561fa429ee42d01a6f67e58cee13637d9285b")
    version("2020.10.1", sha256="799feeccc91965b69e1288c51a1d1118faec7f40b2eb89ad2979591b85324830")
    version("0.12.1", sha256="802367effe86b0d1e64cb5c2ed886771f677fa63260b945e51a27acccdc08fa1")

    depends_on("python@3.9:", when="@2023.7.18:", type=("build", "run"))
    depends_on("python@3.8:", when="@2022.2.2:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    # py-tifffile@2023.1.23: don't have a lower bound on py-numpy anymore
    # -> leave it in nonetheless
    depends_on("py-numpy@1.19.2:", when="@2022.2.2:", type=("build", "run"))
    depends_on("py-numpy@1.15.1:", when="@2020.10.1:", type=("build", "run"))
    depends_on("py-numpy@1.8.2:", type=("build", "run"))
    # https://github.com/cgohlke/tifffile/issues/252
    depends_on("py-numpy@:1", when="@:2024.4.23", type=("build", "run"))
