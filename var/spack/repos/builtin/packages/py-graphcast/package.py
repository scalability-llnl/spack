# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGraphcast(PythonPackage):
    """GraphCast: Learning skillful medium-range global weather forecasting."""

    homepage = "https://github.com/google-deepmind/graphcast"
    url = "https://github.com/google-deepmind/graphcast/archive/refs/tags/v0.1.tar.gz"

    license("Apache-2.0")

    version("0.1", sha256="a51a59b9ee42586ec2883257ae42a23b5653f643a47c608096f497524a17af48")

    depends_on("py-setuptools", type="build")
    with default_args(type=("build", "run")):
        depends_on("py-cartopy")
        depends_on("py-chex")
        depends_on("py-colabtools")
        depends_on("py-dask")
        depends_on("py-dm-haiku")
        depends_on("py-jax")
        depends_on("py-jraph")
        depends_on("py-matplotlib")
        depends_on("py-numpy")
        depends_on("py-pandas")
        depends_on("py-rtree")
        depends_on("py-scipy")
        depends_on("py-tree")
        depends_on("py-trimesh")
        depends_on("py-typing-extensions")
        depends_on("py-xarray")
