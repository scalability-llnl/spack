# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBmapTools(PythonPackage):
    """Bmaptool is a generic tool for creating the block map (bmap) for a file and
    copying files using the block map. The idea is that large files, like raw
    system image files, can be copied or flashed a lot faster and more reliably
    with bmaptool than with traditional tools, like "dd" or "cp"."""

    homepage = "https://github.com/intel/bmap-tools/"
    url = "https://github.com/intel/bmap-tools/archive/v3.4.tar.gz"

    license("GPL-2.0-only")

    version("3.5", sha256="d410e2d97192d0fc2f88ef160a0bb6ed83fce99da97a606d7f6890cc654ec594")
    version("3.4", sha256="483c5dd9589920b5bdec85d4cdbe150adb3ca404d205504f85c0fb03edc69c2a")
    version("3.2", sha256="4cf2adcd34be99cd4b892accaef6942cd9c67a4d09f5b1a5377d1e37ca5a2cd0")
    version("3.1", sha256="91b06562768ef884d8550649578b152937706bce3cf4c1b7931d5bdf22012813")
    version("3.0", sha256="28e3d83743a7ab641f64fbfead2ae332d3df811b5567c82e6e40d1c3e28932dc")
    version("2.6", sha256="01ed095037d64021750c6aa81af2786d872dc661615c240649101b79decad241")

    depends_on("py-setuptools", type="build")
