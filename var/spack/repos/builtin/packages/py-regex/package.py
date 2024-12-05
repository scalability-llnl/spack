# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRegex(PythonPackage):
    """Alternative regular expression module, to replace re."""

    homepage = "https://github.com/mrabarnett/mrab-regex"
    pypi = "regex/regex-2020.11.13.tar.gz"

    license("Apache-2.0")

    version("2022.8.17", sha256="5c77eab46f3a2b2cd8bbe06467df783543bf7396df431eb4a144cc4b89e9fb3c")
    version(
        "2020.11.13", sha256="83d6b356e116ca119db8e7c6fc2983289d87b27b3fac238cfe5dca529d884562"
    )
    version("2019.11.1", sha256="720e34a539a76a1fedcebe4397290604cc2bdf6f81eca44adb9fb2ea071c0c69")
    version(
        "2019.02.07", sha256="4a1a1d963f462c13722b34ef1f82c4707091b0a3fb9b5fd79b6670c38b734095"
    )
    version(
        "2018.01.10", sha256="139678fc013b75e486e580c39b4c52d085ed7362e400960f8be1711a414f16b5"
    )
    version(
        "2017.07.11", sha256="dbda8bdc31a1c85445f1a1b29d04abda46e5c690f8f933a9cc3a85a358969616"
    )

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("python@3.6:", when="@2022.8.17:", type=("build", "run"))
