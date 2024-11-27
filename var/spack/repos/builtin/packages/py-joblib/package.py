# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJoblib(PythonPackage):
    """Lightweight pipelining with Python functions."""

    homepage = "https://joblib.readthedocs.io/"
    pypi = "joblib/joblib-0.14.0.tar.gz"
    git = "https://github.com/joblib/joblib"

    # 'joblib.test' requires 'pytest'. Leave out of 'import_modules' to avoid
    # unnecessary dependencies.
    skip_modules = ["joblib.test"]

    license("BSD-3-Clause")

    version("1.2.0", sha256="e1cee4a79e4af22881164f218d4311f60074197fb707e082e803b61f6d137018")
    version("1.1.0", sha256="4158fcecd13733f8be669be0683b96ebdbbd38d23559f54dca7205aea1bf1e35")
    version("1.0.1", sha256="9c17567692206d2f3fb9ecf5e991084254fe631665c450b443761c4186a613f7")
    version("1.0.0", sha256="7ad866067ac1fdec27d51c8678ea760601b70e32ff1881d4dc8e1171f2b64b24")
    version("0.17.0", sha256="9e284edd6be6b71883a63c9b7f124738a3c16195513ad940eae7e3438de885d5")
    version("0.16.0", sha256="8f52bf24c64b608bf0b2563e0e47d6fcf516abc8cfafe10cfd98ad66d94f92d6")
    version("0.15.1", sha256="61e49189c84b3c5d99a969d314853f4d1d263316cc694bec17548ebaa9c47b6e")
    version("0.15.0", sha256="f8f84dcef519233be4ede1c64fd1f2d48b1e8bbb632d1013ebca75f8b678ee72")
    version("0.14.1", sha256="0630eea4f5664c463f23fbf5dcfc54a2bc6168902719fa8e19daf033022786c8")
    version("0.14.0", sha256="6fcc57aacb4e89451fd449e9412687c51817c3f48662c3d8f38ba3f8a0a193ff")
    version("0.13.2", sha256="315d6b19643ec4afd4c41c671f9f2d65ea9d787da093487a81ead7b0bac94524")
    version("0.11", sha256="7b8fd56df36d9731a83729395ccb85a3b401f62a96255deb1a77220c00ed4085")
    version("0.10.3", sha256="29b2965a9efbc90a5fe66a389ae35ac5b5b0c1feabfc7cab7fd5d19f429a071d")
    version("0.10.2", sha256="3123553bdad83b143428033537c9e1939caf4a4d8813dade6a2246948c94494b")
    version("0.10.0", sha256="49b3a0ba956eaa2f077e1ebd230b3c8d7b98afc67520207ada20a4d8b8efd071")

    depends_on("python@3.7:", when="@1.2:", type=("build", "run"))
    depends_on("python@3.6:", when="@0.15:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
