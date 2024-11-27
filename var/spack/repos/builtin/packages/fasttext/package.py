# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fasttext(CMakePackage):
    """fastText is a library for efficient learning of word representations
    and sentence classification"""

    homepage = "https://github.com/facebookresearch/fastText"
    url = "https://github.com/facebookresearch/fastText/archive/v0.9.2.tar.gz"

    license("MIT")

    version("0.9.2", sha256="7ea4edcdb64bfc6faaaec193ef181bdc108ee62bb6a04e48b2e80b639a99e27e")
    version("0.9.1", sha256="254ace2fc8dc3bea0fc6ad4897a221eb85c1e9adfa61d130b43398193ca1f061")
    version("0.2.0", sha256="71d24ffec9fcc4364554ecac2b3308d834178c903d16d090aa6be9ea6b8e480c")
    version("0.1.0", sha256="d6b4932b18d2c8b3d50905028671aadcd212b7aa31cbc6dd6cac66db2eff1397")

    depends_on("cxx", type="build")  # generated
