# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hsakmt(AutotoolsPackage, XorgPackage):
    """hsakmt is a thunk library that provides a userspace interface to amdkfd
    (AMD's HSA Linux kernel driver). It is the HSA equivalent of libdrm."""

    homepage = "https://cgit.freedesktop.org/amd/hsakmt/"
    xorg_mirror_path = "lib/hsakmt-1.0.0.tar.gz"

    license("MIT")

    version("1.0.0", sha256="3d46af85c27091937618f5e92f7446cff3e9e6378888645e6e238806461e5b77")

    depends_on("c", type="build")  # generated
