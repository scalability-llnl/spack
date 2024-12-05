# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNum2words(PythonPackage):
    """Modules to convert numbers to words. Easily extensible."""

    homepage = "https://github.com/savoirfairelinux/num2words"
    pypi = "num2words/num2words-0.5.10.tar.gz"

    license("LGPL-2.1-or-later")

    version("0.5.12", sha256="7e7c0b0f080405aa3a1dd9d32b1ca90b3bf03bab17b8e54db05e1b78301a0988")
    version("0.5.10", sha256="37cd4f60678f7e1045cdc3adf6acf93c8b41bf732da860f97d301f04e611cc57")

    depends_on("py-setuptools", type="build")
    depends_on("py-docopt@0.6.2:", type=("build", "run"))
