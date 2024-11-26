# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKiwisolver(PythonPackage):
    """A fast implementation of the Cassowary constraint solver"""

    homepage = "https://github.com/nucleic/kiwi"
    pypi = "kiwisolver/kiwisolver-1.1.0.tar.gz"

    version("1.4.5", sha256="e57e563a57fb22a142da34f38acc2fc1a5c864bc29ca1517a88abc963e60d6ec")
    version("1.4.4", sha256="d41997519fcba4a1e46eb4a2fe31bc12f0ff957b2b81bac28db24744f333e955")
    version("1.3.2", sha256="fc4453705b81d03568d5b808ad8f09c77c47534f6ac2e72e733f9ca4714aa75c")
    version("1.3.1", sha256="950a199911a8d94683a6b10321f9345d5a3a8433ec58b217ace979e18f16e248")
    version("1.3.0", sha256="14f81644e1f3bf01fbc8b9c990a7889e9bb4400c4d0ff9155aa0bdd19cce24a9")
    version("1.2.0", sha256="247800260cd38160c362d211dcaf4ed0f7816afb5efe56544748b21d6ad6d17f")
    version("1.1.0", sha256="53eaed412477c836e1b9522c19858a8557d6e595077830146182225613b11a75")
    version("1.0.1", sha256="ce3be5d520b4d2c3e5eeb4cd2ef62b9b9ab8ac6b6fedbaa0e39cdb6f50644278")

    depends_on("cxx", type="build")  # generated

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"), when="@1.2.0:")
    depends_on("python@3.7:", type=("build", "run"), when="@1.3.2:")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@61.2:", when="@1.4.4:", type="build")
    depends_on("py-setuptools-scm@3.4.3:+toml", when="@1.4.4:", type="build")
    depends_on("py-cppy@1.1.0:", type="build", when="@1.2.0:")
    depends_on("py-cppy@1.2.0:", type="build", when="@1.4.4:")
    depends_on("py-typing-extensions", when="@1.4.4: ^python@:3.7", type=("build", "run"))
