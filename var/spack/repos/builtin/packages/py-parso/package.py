# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyParso(PythonPackage):
    """Parso is a Python parser that supports error recovery and round-trip parsing
    for different Python versions (in multiple Python versions).
    Parso is also able to list multiple syntax errors
    in your python file."""

    pypi = "parso/parso-0.6.1.tar.gz"

    license("MIT")

    version("0.8.4", sha256="eb3a7b58240fb99099a345571deecc0f9540ea5f4dd2fe14c2a99d6b281ab92d")
    version("0.8.3", sha256="8c07be290bb59f03588915921e29e8a50002acaf2cdc5fa0e0114f91709fafa0")
    version("0.8.2", sha256="12b83492c6239ce32ff5eed6d3639d6a536170723c6f3f1506869f1ace413398")
    version("0.8.1", sha256="8519430ad07087d4c997fda3a7918f7cfa27cb58972a8c89c2a0295a1c940e9e")
    version("0.7.1", sha256="caba44724b994a8a5e086460bb212abc5a8bc46951bf4a9a1210745953622eb9")
    version("0.6.1", sha256="56b2105a80e9c4df49de85e125feb6be69f49920e121406f15e7acde6c9dfc57")
    version("0.4.0", sha256="2e9574cb12e7112a87253e14e2c380ce312060269d04bd018478a3c92ea9a376")

    with default_args(type=("build", "run")):
        depends_on("python@:3.13", when="@:0.8.4")
        # https://github.com/davidhalter/parso/commit/f7bea28bcc3a1862075e5b61a08d703d72be94aa
        depends_on("python@:3.12", when="@:0.8.3")
        # https://github.com/davidhalter/parso/commit/285492f4ed25f145859630ee6c5625e60aff6e2e
        depends_on("python@:3.11", when="@:0.8.2")

    depends_on("py-setuptools", type="build")
