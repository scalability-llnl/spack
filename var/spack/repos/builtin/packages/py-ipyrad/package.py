# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpyrad(PythonPackage):
    """An interactive toolkit for assembly and analysis of restriction-site
    associated genomic data sets (e.g., RAD, ddRAD, GBS) for population
    genetic and phylogenetic studies."""

    homepage = "https://github.com/dereneaton/ipyrad"

    url = "https://github.com/dereneaton/ipyrad/archive/refs/tags/0.9.85.tar.gz"

    license("GPL-3.0-only")

    version("0.9.93", sha256="7f42396c0baa284dde0e9896270006f3c7e2211fa93bb149decccd39b4ab557e")
    version("0.9.92", sha256="f9cb5eca40d5fc1d93364815af7608d0b2e89fcf675724541a50e7159617395f")
    version("0.9.91", sha256="0308b829a8995db90608e8f45b76709d394d9153ec5edee568acdd41ecfab59c")
    version("0.9.90", sha256="8b95aa3bae30da15baba90abb03176932411ff708c54d5e4481b811cceb8a4a8")
    version("0.9.85", sha256="17b07466531655db878919e426743ac649cfab2e92c06c4e45f76ee1517633f9")

    depends_on("py-setuptools", type="build")

    # Dependencies found at
    # https://ipyrad.readthedocs.io/en/master/3-installation.html#details-dependencies
    depends_on("bedtools2", type=("build", "run"))
    depends_on("bwa", type=("build", "run"))
    depends_on("muscle", type=("build", "run"))
    depends_on("py-notebook", type=("build", "run"))
    depends_on("samtools", type=("build", "run"))
    depends_on("vsearch", type=("build", "run"))
    depends_on("py-numpy@:1.23", when="@:0.9.90", type=("build", "run"))
    # https://github.com/spack/spack/pull/42098 indicates 0.9.90 and below use
    # np.int and related functions, deprecated in 1.20 and expired in 1.24.
    depends_on("py-numpy", when="@0.9.91:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-numba", type=("build", "run"))
    depends_on("py-ipyparallel", type=("build", "run"))
    depends_on("py-pysam", type=("build", "run"))
    depends_on("py-cutadapt", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))

    def patch(self):
        # ipyrad/core/Parallel.py assumes that ipcluster will always be
        # in the python root
        filter_file(
            r"^IPCLUSTER_BIN\s*=.*$",
            'IPCLUSTER_BIN = "{}"'.format(self.spec["py-ipyparallel"].prefix.bin.ipcluster),
            join_path("ipyrad", "core", "Parallel.py"),
        )
