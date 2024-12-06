# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyImmutables(PythonPackage):
    """An immutable mapping type for Python."""

    homepage = "https://github.com/MagicStack/immutables"
    pypi = "immutables/immutables-0.14.tar.gz"

    license("Apache-2.0")

    version("0.20", sha256="1d2f83e6a6a8455466cd97b9a90e2b4f7864648616dfa6b19d18f49badac3876")
    version("0.19", sha256="df17942d60e8080835fcc5245aa6928ef4c1ed567570ec019185798195048dcf")
    version("0.18", sha256="5336c7974084cce62f7e29aaff81a3c3f75e0fd0a23a2faeb986ae0ea08d8cf4")
    version("0.16", sha256="d67e86859598eed0d926562da33325dac7767b7b1eff84e232c22abea19f4360")
    version("0.14", sha256="a0a1cc238b678455145bae291d8426f732f5255537ed6a5b7645949704c70a78")

    depends_on("c", type="build")  # generated

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"), when="@0.16:")
    depends_on("py-setuptools", type="build")
    # setuptools 68 is more strict about the format of pyproject.toml and fails to install older
    # versions of this package
    depends_on("py-setuptools@:67", type="build", when="@:0.18")
    depends_on("py-setuptools@42:", type="build", when="@0.16:")
    depends_on("py-typing-extensions@3.7.4.3:", when="@0.16: ^python@:3.7", type=("build", "run"))
