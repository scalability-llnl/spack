# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPypinyin(PythonPackage):
    """Chinese Pinyin conversion module/tool."""

    homepage = "https://github.com/mozillazg/python-pinyin"
    pypi = "pypinyin/pypinyin-0.46.0.tar.gz"

    license("MIT")

    version("0.46.0", sha256="0d2e41e95dbc20a232c0f5d3850654eebbfcba303d96358d2c46592725bb989c")

    depends_on("python@2.6:2,3.3:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
