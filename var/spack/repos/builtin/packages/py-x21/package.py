# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class PyX21(PythonPackage):
    """Used for unpacking this author's obfuscated libraries"""

    homepage = "https://pypi.org/project/x21/"
    list_url = "https://pypi.org/simple/x21/"

    def url_for_version(self, version):
        url = "https://pypi.io/packages/cp{1}/x/x21/x21-{0}-cp{1}-cp{1}-{2}.whl"

        if sys.platform == "darwin":
            platform_string = "macosx_10_9_x86_64"
        elif sys.platform.startswith("linux"):
            platform_string = "manylinux_2_17_x86_64.manylinux2014_x86_64"

        py_ver = Version(version.string.split("y")[1])

        return url.format(version.string.split("-")[0], py_ver.joined, platform_string)

    if sys.platform == "darwin":
        version(
            "0.2.6-py3.8",
            sha256="bbbfdb6b56562ecc81f0dc39e009713157011fbb50d47353eb25f633acf77204",
        )
        version(
            "0.2.6-py3.9",
            sha256="d7b4f06a71ac27d05ae774752b3ca396134916427f371b5995b07f0f43205043",
        )
        version(
            "0.2.6-py3.10",
            sha256="2cbda690757f1fc80edfe48fcb13f168068f1784f0cb8c300a0d8051714d0452",
        )
    elif sys.platform.startswith("linux"):
        version(
            "0.2.6-py3.8",
            sha256="64275052bcda784395bc613f750b8b5a6b1ddbfa4e7a590cb8e209543f0ca0c4",
        )
        version(
            "0.2.6-py3.9",
            sha256="e20b29650fcbf0be116ac93511033bf10debc76261b7350e018ff91b92ff950d",
        )
        version(
            "0.2.6-py3.10",
            sha256="7c5c58ff6dc81caac6815578f78cf545e719beb0bf4017f77120d38025d2bc7d",
        )

    depends_on("python@3.8.0:3.8", type=("build", "run"), when="@0.2.6-py3.8")
    depends_on("python@3.9.0:3.9", type=("build", "run"), when="@0.2.6-py3.9")
    depends_on("python@3.10.0:3.10", type=("build", "run"), when="@0.2.6-py3.10")
    depends_on("py-pynacl", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-tomli", type=("build", "run"))
    depends_on("py-tomli-w", type=("build", "run"))
