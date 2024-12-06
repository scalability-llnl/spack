# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUvw(PythonPackage):
    """
    UVW is a small utility library to write VTK files
    from data contained in Numpy arrays.
    """

    homepage = "https://github.com/prs513rosewood/uvw"
    git = "https://github.com/prs513rosewood/uvw.git"
    pypi = "uvw/uvw-0.3.1.tar.gz"

    maintainers("prs513rosewood")

    license("MIT")

    version("master", branch="master")
    version("0.5.0", sha256="dd4501bc2f8c6080467f19d7537a282123a51d849c6b7ace18191ab751ec7621")
    version("0.4.0", sha256="688052832c96ac6ead93f15e577d4f1c2339376300e781520c43cf8652ed3dd8")
    version("0.3.2", sha256="24f0d0f116e55cd80bf8f29fb45eb515a659849623017587c654230eeee3c4d9")
    version("0.3.1", sha256="31e3347ec342bd5381091f3c782ea1a1bfa4709d1de41cd700509e0b813f2265")
    version("0.0.7", sha256="4bcb77cf9655f0dcd5f38f024210ac5ad7ebc6fcfb45f898468d29a927bcb7a5")

    variant("mpi", description="Use parallel writers", default=False)

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-mpi4py", type=("build", "run"), when="+mpi")
