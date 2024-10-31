# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Maven(Package):
    """Apache Maven is a software project management and comprehension tool."""

    homepage = "https://maven.apache.org/index.html"
    url = "https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/3.3.9/apache-maven-3.3.9-bin.tar.gz"
    list_url = "https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/"
    list_depth = 1

    license("Apache-2.0", checked_by="wdconinc")

    version("3.9.8", sha256="067672629075b740e3d0a928e21021dd615a53287af36d4ccca44e87e081d102")
    version("3.8.8", sha256="17811e108701af5985bf5167abbd47c06e92c6c6bd1c13a1a1c095c9b4ecc32a")
    version("3.8.4", sha256="2cdc9c519427bb20fdc25bef5a9063b790e4abd930e7b14b4e9f4863d6f9f13c")
    version("3.6.3", sha256="26ad91d751b3a9a53087aefa743f4e16a17741d3915b219cf74112bf87a438c5")
    version("3.6.2", sha256="3fbc92d1961482d6fbd57fbf3dd6d27a4de70778528ee3fb44aa7d27eb32dfdc")
    version("3.6.1", sha256="2528c35a99c30f8940cc599ba15d34359d58bec57af58c1075519b8cd33b69e7")
    version("3.6.0", sha256="6a1b346af36a1f1a491c1c1a141667c5de69b42e6611d3687df26868bc0f4637")
    version("3.5.0", sha256="beb91419245395bd69a4a6edad5ca3ec1a8b64e41457672dc687c173a495f034")
    version("3.3.9", sha256="6e3e9c949ab4695a204f74038717aa7b2689b1be94875899ac1b3fe42800ff82")
    version("3.0.4", sha256="d35a876034c08cb7e20ea2fbcf168bcad4dff5801abad82d48055517513faa2f")

    depends_on("java", type="run")

    executables = ["^mvn$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"Apache Maven (\S+)", output)
        return match.group(1) if match else None

    def install(self, spec, prefix):
        # install pre-built distribution
        install_tree(".", prefix)
