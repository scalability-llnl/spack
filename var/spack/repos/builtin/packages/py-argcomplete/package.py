# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArgcomplete(PythonPackage):
    """Bash tab completion for argparse."""

    homepage = "https://github.com/kislyuk/argcomplete"
    pypi = "argcomplete/argcomplete-1.12.0.tar.gz"

    version("3.5.0", sha256="4349400469dccfb7950bb60334a680c58d88699bff6159df61251878dc6bf74b")
    version("3.1.6", sha256="3b1f07d133332547a53c79437527c00be48cca3807b1d4ca5cab1b26313386a6")
    version("3.1.2", sha256="d5d1e5efd41435260b8f85673b74ea2e883affcbec9f4230c582689e8e78251b")
    version("3.0.8", sha256="b9ca96448e14fa459d7450a4ab5a22bbf9cee4ba7adddf03e65c398b5daeea28")
    version("2.0.0", sha256="6372ad78c89d662035101418ae253668445b391755cfe94ea52f1b9d22425b20")
    version("1.12.3", sha256="2c7dbffd8c045ea534921e63b0be6fe65e88599990d8dc408ac8c542b72a5445")
    version("1.12.0", sha256="2fbe5ed09fd2c1d727d4199feca96569a5b50d44c71b16da9c742201f7cc295c")
    version("1.1.1", sha256="cca45b5fe07000994f4f06a0b95bd71f7b51b04f81c3be0b4ea7b666e4f1f084")

    depends_on("py-setuptools@67.7.2:", when="@3.1:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm+toml@6.2:", when="@3.1:", type="build")

    depends_on("py-importlib-metadata@0.23:6", when="@3.0.6: ^python@:3.7", type=("build", "run"))
    depends_on(
        "py-importlib-metadata@0.23:4", when="@1.12.3:2 ^python@:3.7", type=("build", "run")
    )
    depends_on("py-importlib-metadata@0.23:3", when="@1.12.2 ^python@:3.7", type=("build", "run"))
    depends_on("py-importlib-metadata@0.23:2", when="@1.12.1 ^python@:3.7", type=("build", "run"))
    depends_on("py-importlib-metadata@0.23:1", when="@1.12.0 ^python@:3.7", type=("build", "run"))
