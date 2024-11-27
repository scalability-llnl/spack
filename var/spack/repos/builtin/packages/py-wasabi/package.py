# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyWasabi(PythonPackage):
    """wasabi: A lightweight console printing and formatting toolkit."""

    homepage = "https://github.com/explosion/wasabi"
    pypi = "wasabi/wasabi-0.6.0.tar.gz"

    license("MIT")

    version("1.1.2", sha256="1aaef3aceaa32edb9c91330d29d3936c0c39fdb965743549c173cb54b16c30b5")
    version("0.6.0", sha256="b8dd3e963cd693fde1eb6bfbecf51790171aa3534fa299faf35cf269f2fd6063")

    depends_on("py-setuptools", type="build")
    depends_on(
        "py-typing-extensions@3.7.4.1:4.4", type=("build", "run"), when="@1.1.2:^python@:3.7"
    )
    depends_on("py-colorama@0.4.6:", type=("build", "run"), when="@1.1.2:platform=windows")
