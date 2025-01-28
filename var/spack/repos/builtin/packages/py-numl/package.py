# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNuml(PythonPackage):
    """Standardised ML input processing for particle physics"""

    homepage = "https://github.com/nugraph/nugraph"
    git = "https://github.com/nugraph/nugraph"
    url = "https://github.com/nugraph/nugraph/archive/v24.7.1.tar.gz"
    build_directory = "pynuml"

    maintainers("vhewes")

    license("MIT", checked_by="vhewes")

    version("main", branch="main")
    version("24.7.1", sha256="a51c0576ab969c404024b734e5507712e5a9d1d29e14077fee121415779c78f0")
    version("24.7.0", sha256="7e44fbc1eb75a9302d57cabfffd559ddaddb44d0b7198168cbacbeed5e11dd7e")
    version("24.4.0", sha256="927da53b28630921d31ca3b71676ef392b9ff847796b76d593239c6af9276b4c")
    version("24.2.0", sha256="6ff9204bc0817619e7317e7a0d7ddfbea1842b261938f1718c3949539c8719df")
    version("23.11.0", sha256="db77e0c723caf4ac9fb5c41d250aee1d03e623e861c73120b23aff194902bf09")
    version("23.10.0", sha256="ee36625d5215406a199420d8fa262b720c5d191c0346d2b4aaab6808b47e80ad")
    version("23.9.0", sha256="2cc77356a1061b7271c3c5da69009f0d2ef0df09a18ab6466049ea901231909c")
    version("23.7.0", sha256="8598f65b7fcc76fc3f0f41f7ca44bfb134daa627693f1ada61c8106b26db4d84")
    version("23.6.1", sha256="74c41b34eba1d80548a0ec1b36aee5948f3ee0e9df80d6864b38aed99964263c")
    version("23.6.0", sha256="93ebbaf0a55e22d06fc06e8a93e29a0e875985f4b3801d391db853d1fceb3d6c")

    depends_on("py-flit-core", type="build")

    depends_on("mpich")
    depends_on("py-h5py +mpi")
    depends_on("py-pandas")
    depends_on("py-particle")
    depends_on("py-plotly")
    depends_on("py-torch-geometric")

    extends("python")
