# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTensorboardx(PythonPackage):
    """The purpose of this package is to let researchers use
    a simple interface to log events within PyTorch (and
    then show visualization in tensorboard). This package
    currently supports logging scalar, image, audio,
    histogram, text, embedding, and the route of back-propagation."""

    homepage = "https://github.com/lanpa/tensorboardX"
    pypi = "tensorboardx/tensorboardX-1.8.tar.gz"

    license("MIT")

    version("2.6.2.2", sha256="c6476d7cd0d529b0b72f4acadb1269f9ed8b22f441e87a84f2a3b940bb87b666")
    version("2.5.1", sha256="ea85a3446f22ce8a917fe4fa4d8a7a96222ef84ac835267d038c34bb99f6d61b")
    version("2.1", sha256="9e8907cf2ab900542d6cb72bf91aa87b43005a7f0aa43126268697e3727872f9")
    version("2.0", sha256="835d85db0aef2c6768f07c35e69a74e3dcb122d6afceaf2b8504d7d16c7209a5")
    version("1.9", sha256="2505d0092e6212f04c4522eea7123e8886c4d0a0b2c406e480fa61ca3c1da7ea")
    version("1.8", sha256="13fe0abba27f407778a7321937190eedaf12bc8c544d9a4e294fcf0ba177fd76")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", when="@2.6.2.2:", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-protobuf@3.8.0:3.20.1", when="@:2.5.1", type=("build", "run"))
    depends_on("py-protobuf@3.20:", when="@2.6.2.2:", type=("build", "run"))
    depends_on("py-packaging", when="@2.6.2.2:", type=("build", "run"))

    depends_on("py-six", when="@:2.1", type=("build", "run"))
