# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySdv(PythonPackage):
    """The Synthetic Data Vault (SDV) is a Synthetic Data
    Generation ecosystem of libraries that allows users to
    easily learn single-table, multi-table and timeseries
    datasets to later on generate new Synthetic Data that
    has the same format and statistical properties as the
    original dataset."""

    maintainers("Kerilk", "jke513")

    homepage = "https://github.com/sdv-dev/SDV"
    pypi = "sdv/sdv-0.13.1.tar.gz"

    license("MIT")

    version("0.14.0", sha256="a62714b73a7e14b95ffbda0920a3a5a6fe891a17d8611380af5f9ca1ff8fc234")
    version("0.13.1", sha256="c0a0dbc4a64e5f60cabd123a8c19b3f99594f5a0911de83e08d172b810222c93")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-faker@3.0.0:9", type=("build", "run"))
    depends_on("py-graphviz@0.13.2:0", type=("build", "run"))
    depends_on("py-numpy@1.20:1", type=("build", "run"))
    depends_on("py-pandas@1.1.3:1.1.4", type=("build", "run"))
    depends_on("py-tqdm@4.15:4", type=("build", "run"))
    depends_on("py-copulas@0.6.0:0.6", type=("build", "run"))
    depends_on("py-ctgan@0.5.0:0.5", type=("build", "run"))
    depends_on("py-deepecho@0.3.0.post1:0.3", type=("build", "run"))
    depends_on("py-rdt@0.6.1:0.6", type=("build", "run"))
    depends_on("py-sdmetrics@0.4.1:0.4", type=("build", "run"))
