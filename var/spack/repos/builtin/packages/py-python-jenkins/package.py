# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonJenkins(PythonPackage):
    """Python bindings for the remote Jenkins API"""

    homepage = "https://opendev.org/jjb/python-jenkins/"
    pypi = "python-jenkins/python-jenkins-1.5.0.tar.gz"

    version("1.5.0", sha256="0b11f7c1dffc48579afefa8a310cba5b1c98785b9132892ff8cf5312f32ebc90")
    version("1.0.2", sha256="54aba30cf49f78f9eb64e9717ad8049dacf090731a3e0c27e6035f9ec52ff78e")

    depends_on("py-setuptools", type="build")
    depends_on("py-pbr@0.8.2:", type=("build", "run"))
    depends_on("py-six@1.3.0:", type="run")
    depends_on("py-multi-key-dict", type="run")
    depends_on("py-requests", type="run")
