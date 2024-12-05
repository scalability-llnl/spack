# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyColabtools(PythonPackage):
    """Tools to work with colab from google."""

    homepage = "https://github.com/zuuuhkrit/colabtools"
    pypi = "colabtools/colabtools-0.0.1.tar.gz"

    license("LGPL-3.0-only")

    version("0.0.1", sha256="b6f7c0050e5924f4ad7e4762d46be663e21d417a39fc4adf6c6c90e8d9be47ec")

    depends_on("py-setuptools", type="build")
