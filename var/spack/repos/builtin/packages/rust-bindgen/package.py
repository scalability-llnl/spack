# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class RustBindgen(CargoPackage):
    """The rust programming language toolchain"""

    homepage = "https://rust-lang.github.io/rust-bindgen/"
    url = "https://github.com/rust-lang/rust-bindgen/archive/v0.20.5.tar.gz"

    license("BSD-3-Clause")

    version("0.69.4", sha256="c02ce18b95c4e5021b95b8b461e5dbe6178edffc52a5f555cbca35b910559b5e")
    version("0.69.3", sha256="5cdaa156403841e7b286ccbb7b31398c8b49b99f89ebf329457101819aa5eaf0")
    version("0.69.2", sha256="78fbb8bd100e145d1effc982eaab21b555ccc3fc1cbe6e734f17cdfe5c33af32")
    version("0.69.1", sha256="c10e2806786fb75f05ef32f3f03f4cb7e37bb8e06be5a4a0e95f974fdc567d87")
    version("0.69.0", sha256="10790bb9863bff6a6f877b89d9d7cff7eac2ff0f45c1482f5edc9d9d0a82488d")
    version("0.68.1", sha256="6a577026184a6f7a99b48f46f2074c83d272d3aadf91c7b94a4c6c34e6acd445")
    version("0.66.1", sha256="adedec96f2a00ce835a7c31656e09d6aae6ef55df9ca3d8d65d995f8f2542388")
    version("0.66.0", sha256="d2c8e8c1c9fbabecaa1146a02cc3bbbf968931136e7dc94614af06880d291685")
    version("0.20.5", sha256="4f5236e7979d262c43267afba365612b1008b91b8f81d1efc6a8a2199d52bb37")

    depends_on("cxx", type="build")  # generated

    def build(self, spec, prefix):
        # The carogopackage installer doesn't allow for an option to install from a subdir
        # see: https://github.com/rust-lang/cargo/issues/7599
        cargo("install", "--root", "out", "bindgen-cli")
