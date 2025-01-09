# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySafetensors(PythonPackage):
    """Fast and Safe Tensor serialization."""

    homepage = "https://github.com/huggingface/safetensors"
    pypi = "safetensors/safetensors-0.3.1.tar.gz"

    version("0.4.5", sha256="d73de19682deabb02524b3d5d1f8b3aaba94c72f1bbfc7911b9b9d5d391c0310")
    version("0.4.3", sha256="2f85fc50c4e07a21e95c24e07460fe6f7e2859d0ce88092838352b798ce711c2")
    version("0.3.1", sha256="571da56ff8d0bec8ae54923b621cda98d36dcef10feb36fd492c4d0c2cd0e869")

    # Based on PyPI wheel availability
    depends_on("python@:3.12", when="@:0.4.3", type=("build", "run"))
    depends_on("py-maturin@1", type="build", when="@0.4.3:")
    depends_on("py-setuptools", when="@0.3.1", type="build")
    depends_on("py-setuptools-rust", when="@0.3.1", type="build")
