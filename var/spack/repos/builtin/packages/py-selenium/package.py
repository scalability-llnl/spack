# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySelenium(PythonPackage):
    """Python language bindings for Selenium WebDriver.

    The selenium package is used to automate web browser interaction from
    Python."""

    homepage = "https://github.com/SeleniumHQ/selenium/"
    pypi = "selenium/selenium-3.141.0.tar.gz"

    license("Apache-2.0")

    version("3.141.0", sha256="deaf32b60ad91a4611b98d8002757f29e6f2c2d5fcaf202e1c9ad06d6772300d")

    depends_on("py-setuptools", type="build")
    depends_on("py-urllib3", type=("build", "run"))
