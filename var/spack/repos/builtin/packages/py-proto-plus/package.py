# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyProtoPlus(PythonPackage):
    """Beautiful, Pythonic protocol buffers."""

    homepage = "https://github.com/googleapis/proto-plus-python"
    pypi = "proto-plus/proto-plus-1.23.0.tar.gz"

    version("1.23.0", sha256="89075171ef11988b3fa157f5dbd8b9cf09d65fffee97e29ce403cd8defba19d2")

    depends_on("py-protobuf@3.19:4", type=("build", "run"))

    depends_on("py-setuptools", type="build")
