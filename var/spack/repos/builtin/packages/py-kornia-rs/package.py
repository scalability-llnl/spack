# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKorniaRs(PythonPackage):
    """Low level implementations for computer vision in Rust."""

    homepage = "http://www.kornia.org/"
    url = "https://github.com/kornia/kornia-rs/archive/refs/tags/v0.1.1.tar.gz"

    license("Apache-2.0")
    maintainers(
        "edgarriba",
        "ducha-aiki",
        "lferraz",
        "shijianjian",
        "cjpurackal",
        "johnnv1",
        "adamjstewart",
    )

    version("0.1.1", sha256="b9ac327fae6e982e6d7df9faeadd1d4f6453e65521819ae9ae5b90e9da0ed1a5")
    version("0.1.0", sha256="0fca64f901dddff49b72e51fc92a25f0a7606e9a1a72ef283606245ea6b4f90d")

    build_directory = "py-kornia"

    depends_on("py-maturin@1.3.2:", type="build")

    # rav1e needs rustdoc
    depends_on("rust+dev", type="build")

    # pyo3 needs cmake
    depends_on("cmake", type="build")

    # turbojpeg-sys needs an assembly compiler
    depends_on("nasm", type="build")

    # dlpack-rs needs libclang
    depends_on("llvm+clang")
