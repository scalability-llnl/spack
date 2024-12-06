# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDataclassesJson(PythonPackage):
    """Easily serialize dataclasses to and from JSON."""

    homepage = "https://github.com/lidatong/dataclasses-json"
    pypi = "dataclasses_json/dataclasses_json-0.5.12.tar.gz"

    license("MIT")

    version("0.5.12", sha256="70e28da52e36f4be6b724e1f1e77fbcd19e0e0a6bf9a4c4c6e5abf713d4dab5a")

    depends_on("python@3.7:3.11", type=("build", "run"))
    depends_on("py-poetry-core@1.2:", type="build")
    depends_on("py-typing-inspect@0.4:0", type=("build", "run"))
    depends_on("py-marshmallow@3.18:3", type=("build", "run"))
