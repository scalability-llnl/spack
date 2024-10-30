# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNuml(PythonPackage):
    """Standardised ML input processing for particle physics"""

    pypi = "pynuml/pynuml-24.7.1.tar.gz"

    maintainers("vhewes")

    license("MIT", checked_by="vhewes")

    version("24.7.1", sha256="20d2f1a07887473e67c79ecc3804b8012e22b78883199fdb0d07bb1b725b6ab0")
    version("24.7.0", sha256="d47f71ead6861278595b79d04c554da4998d5c4c50587e4c90231f50db0f2e81")
    version("24.6.0", sha256="357d2b0e0b9ca179514d177278620e5ac57bed37bfb6d145c172150126432613")
    version("23.11.0", sha256="1a7e61864cfeb0b27c6a93646c33e3f457bbc384eb86aee4df76b5e02898d02f")
    version("23.9.0", sha256="77ea8c9df541351adeb249594cce27d742973ee82a0d7f2ad8cdcffa9d3fa6b1")
    version("23.8.0", sha256="0896797f3f70b3a6d3d74f7a3e7fe5eaf59a2000a47ffc7ac08b73be0aa15706")
    version("23.7.0", sha256="5449dd09a7e046d036e12c7971e61d2862cdb79c7932144b038288fc05ca50a8")
    version("23.6.1", sha256="fdb23a9d4f1b83b06cc35b07608fe4c2e55f8307ac47851cccc21a20b69ab674")
    version("23.6.0", sha256="fcc1546b9489584f2635f6418c5e1a43f6bdf02dd5c46b7afa09ea5f247524a2")
    version("23.5.2", sha256="d83576c8e25e22cc9ba68a35b9690ea861f7a4c09db65ca134849c89fba9b330")
    version("23.5.1", sha256="73ef1bea1022b9ebddec35ac7d66c1394003aa5e63a4ec99bfa14d4f833e04a4")
    version("23.5.0", sha256="dccb774932813ddc788b1d27e52e251d9db6ea16b303596bfa0955ae51098674")

    depends_on("py-flit-core", type="build")

    depends_on("mpich")
    depends_on("py-h5py +mpi")
    depends_on("py-pandas")
    depends_on("py-particle")
    depends_on("py-plotly")
    depends_on("py-torch-geometric")

    extends("python")
