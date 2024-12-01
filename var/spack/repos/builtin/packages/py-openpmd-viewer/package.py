# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpenpmdViewer(PythonPackage):
    """Python visualization tools for openPMD files"""

    homepage = "https://www.openPMD.org"
    git = "https://github.com/openPMD/openPMD-viewer.git"
    pypi = "openPMD-viewer/openPMD-viewer-1.2.0.tar.gz"

    maintainers("RemiLehe", "ax3l")

    license("BSD-3-Clause-LBNL")

    version("1.4.0", sha256="53b4c10a508a012b9609f079a1d419aaeac769852117c676faf43e6cd9369f8b")
    version("1.3.0", sha256="236c065a37881fcb7603efde0bf2d61acc355a8acc595bebc3d6b9d03251b081")
    version("1.2.0", sha256="a27f8ac522c4c76fd774095e156a8b280c9211128f50aa07f16ac70d8222384d")

    variant(
        "backend",
        default="h5py,openpmd-api",
        description="Visualization backend",
        multi=True,
        values=("h5py", "openpmd-api"),
    )
    variant("jupyter", default=False, description="Enable Jupyter Widget GUI")
    variant("numba", default=False, description="Enable accelerated depositions for histograms")
    variant("plot", default=True, description="Enable plotting support")
    variant("tutorials", default=True, description="Enable dependencies for tutorials")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-numpy@1.15:1", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-tqdm", type=("build", "run"))

    depends_on("py-h5py@2.8.0:", type=("build", "run"))
    with when("backend=openpmd-api"):
        depends_on("openpmd-api +python -mpi", type=("build", "run"))

    with when("+jupyter"):
        depends_on("py-ipywidgets", type=("build", "run"))
        depends_on("py-jupyter", type=("build", "run"))
        depends_on("py-tqdm +notebook", type=("build", "run"))

    with when("+numba"):
        depends_on("py-numba", type=("build", "run"))

    with when("+plot"):
        depends_on("py-matplotlib", type=("build", "run"))
        # missing in Spack:
        # with when('+jupyter'):
        #     depends_on('py-ipympl', type=('build', 'run'))

    with when("+tutorials"):
        depends_on("py-wget", type=("build", "run"))
