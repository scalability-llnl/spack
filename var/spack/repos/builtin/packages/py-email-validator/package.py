# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEmailValidator(PythonPackage):
    """A robust email address syntax and deliverability validation library."""

    homepage = "https://github.com/JoshData/python-email-validator"
    pypi = "email_validator/email_validator-1.3.1.tar.gz"

    license("Unlicense", when="@2.1.1:", checked_by="wdconinc")
    license("CC0-1.0", when="@:2.1.0", checked_by="wdconinc")

    version("2.2.0", sha256="cb690f344c617a714f22e66ae771445a1ceb46821152df8e165c5f9a364582b7")
    version("1.3.1", sha256="d178c5c6fa6c6824e9b04f199cf23e79ac15756786573c190d2ad13089411ad2")

    depends_on("py-setuptools", type="build")
    depends_on("py-dnspython@2:", type=("build", "run"), when="@2:")
    depends_on("py-dnspython@1.15:", type=("build", "run"))
    depends_on("py-idna@2:", type=("build", "run"))
