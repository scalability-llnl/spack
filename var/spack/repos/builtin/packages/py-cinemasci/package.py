# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCinemasci(PythonPackage):
    """A set of python tools for reading, writing and viewing Cinema
    databases"""

    homepage = "https://github.com/cinemascience"
    pypi = "cinemasci/cinemasci-1.7.0.tar.gz"

    tags = ["e4s"]

    maintainers("EthanS94")

    version("1.7.0", sha256="70e1fa494bcbefdbd9e8859cdf1b01163a94ecffcdfa3da1011e4ef2fcee6169")
    version("1.3", sha256="c024ca9791de9d78e5dad3fd11e8f87d8bc1afa5830f2697d7ec4116a5d23c20")

    variant("mpi", default=False, description="Enable MPI")

    depends_on("hdf5 ~mpi", when="~mpi")
    depends_on("hdf5 +mpi", when="+mpi")
    depends_on("pil", type=("build", "run"))
    depends_on("python@3:", type=("build", "run"))
    depends_on("py-h5py~mpi", when="~mpi", type=("build", "run"))
    depends_on("py-h5py+mpi", when="+mpi", type=("build", "run"))
    depends_on("py-ipywidgets", type=("build", "run"))
    depends_on("py-jupyterlab", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"), when="@1.7.0:")
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"), when="@1.7.0:")
    depends_on("py-scikit-image", type=("build", "run"), when="@1.7.0:")
    depends_on("py-scipy", type=("build", "run"), when="@1.7.0:")
    depends_on("py-setuptools", type=("build"))
