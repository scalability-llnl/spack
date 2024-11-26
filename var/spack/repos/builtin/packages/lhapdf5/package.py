# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lhapdf5(AutotoolsPackage):
    """LHAPDF is a general purpose Fortran 77/90 interpolator,
    used for evaluating PDFs from discretised data files."""

    homepage = "https://lhapdf.hepforge.org/lhapdf5/"
    url = "https://lhapdf.hepforge.org/downloads?f=old/lhapdf-5.9.1.tar.gz"

    license("GPL-2.0-or-later")

    version("5.9.1", sha256="86b9b046d7f25627ce2aab6847ef1c5534972f4bae18de98225080cf5086919c")
    version("5.9.0", sha256="64b9018ce6102ae7b6a92c990ca6afa841fb992d87b1abf5756c3d04c4d46b9c")
    version("5.8.9", sha256="b90a83512fc5f51e4cd419f1e79ad6e6fcd0e19636bb07464e41f47ee0509d3c")
    version("5.8.8", sha256="fe4c7148b1858c3c534c5e80ea1a8766b4407d19c44c40578da54e390af228f8")
    version("5.8.7", sha256="4c6effdcc74c8b60aaa18bf60e224de3c5f3c2e5b0efc08d38338f01bec7db47")
    version("5.8.6", sha256="689800b2ad6d822e2da0435f9303457feaa9102bff8ef9dbfd708e13afceeef2")
    version("5.8.5", sha256="f37d87c70a65a770bb2d013c4d1d9aa5d90c0f52b9430d56bab578fd221e8e41")
    version("5.8.4", sha256="75a3b44bd4509bec47806fb5ad4baaa6334a2aa8f51cf2f7195d4f08bd353ca2")
    version("5.8.3", sha256="e9b5e72bab65adef9ef78a5e0ee526a6ee673bed142f5e3617c0a27029b84275")
    version("5.8.2", sha256="c54b4153b43453426510fd8aa322de66a80a33137ad251124345309615f6a3a6")
    version("5.8.1", sha256="e113818541e976be69a9524007c2db19059da9af7abfebf7c53d86eafa2109c9")
    version("5.8.0", sha256="8381ea5f785dde95772a2b6d5890f1cb72012e223e6861823fd81b09eedaa7a3")
    version("5.7.1", sha256="40529629351598317fbf7b5905661e51b23778019d50451eee78d7b1118e2559")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    def setup_build_environment(self, env):
        env.append_flags("FFLAGS", "-std=legacy")

    def configure_args(self):
        return ["--disable-pyext"]
