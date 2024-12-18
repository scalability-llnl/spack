# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWarpx(PythonPackage):
    """This package is deprecated. Please use `warpx +python`.

    WarpX is an advanced electromagnetic Particle-In-Cell code. It supports
    many features including Perfectly-Matched Layers (PML) and mesh refinement.
    In addition, WarpX is a highly-parallel and highly-optimized code and
    features hybrid OpenMP/MPI parallelization, advanced vectorization
    techniques and load balancing capabilities.

    These are the Python bindings of WarpX with PICMI input support.
    See the C++ 'warpx' package for the WarpX application and library.
    """

    homepage = "https://ecp-warpx.github.io"
    url = "https://github.com/ECP-WarpX/WarpX/archive/refs/tags/23.08.tar.gz"
    git = "https://github.com/ECP-WarpX/WarpX.git"

    maintainers("ax3l", "dpgrote", "EZoni", "RemiLehe")

    tags = ["e4s", "ecp"]

    license("BSD-3-Clause-LBNL")

    # NOTE: if you update the versions here, also see warpx
    version("develop", branch="development", deprecated=True)
    version(
        "23.08",
        sha256="67695ff04b83d1823ea621c19488e54ebaf268532b0e5eb4ea8ad293d7ab3ddc",
        deprecated=True,
    )
    version(
        "23.07",
        sha256="511633f94c0d0205013609bde5bbf92a29c2e69f6e69b461b80d09dc25602945",
        deprecated=True,
    )
    version(
        "23.06",
        sha256="75fcac949220c44dce04de581860c9a2caa31a0eee8aa7d49455fa5fc928514b",
        deprecated=True,
    )
    version(
        "23.05",
        sha256="34306a98fdb1f5f44ab4fb92f35966bfccdcf1680a722aa773af2b59a3060d73",
        deprecated=True,
    )
    version(
        "23.04",
        sha256="e5b285c73e13a0d922eba5d83760c168d4fd388e54a519830003b2e692dab823",
        deprecated=True,
    )
    version(
        "23.03",
        sha256="e1274aaa2a2c83d599d61c6e4c426db4ed5d4c5dc61a2002715783a6c4843718",
        deprecated=True,
    )
    version(
        "23.02",
        sha256="a6c63ebc38cbd224422259a814be501ac79a3b734dab7f59500b6957cddaaac1",
        deprecated=True,
    )
    version(
        "23.01",
        sha256="e853d01c20ea00c8ddedfa82a31a11d9d91a7f418d37d7f064cf8a241ea4da0c",
        deprecated=True,
    )
    version(
        "22.12",
        sha256="96019902cd6ea444a1ae515e8853048e9074822c168021e4ec1687adc72ef062",
        deprecated=True,
    )
    version(
        "22.11",
        sha256="528f65958f2f9e60a094e54eede698e871ccefc89fa103fe2a6f22e4a059515e",
        deprecated=True,
    )
    version(
        "22.10",
        sha256="3cbbbbb4d79f806b15e81c3d0e4a4401d1d03d925154682a3060efebd3b6ca3e",
        deprecated=True,
    )
    version(
        "22.09",
        sha256="dbef1318248c86c860cc47f7e18bbb0397818e3acdfb459e48075004bdaedea3",
        deprecated=True,
    )
    version(
        "22.08",
        sha256="5ff7fd628e8bf615c1107e6c51bc55926f3ef2a076985444b889d292fecf56d4",
        deprecated=True,
    )
    version(
        "22.07",
        sha256="0286adc788136cb78033cb1678d38d36e42265bcfd3d0c361a9bcc2cfcdf241b",
        deprecated=True,
    )
    version(
        "22.06",
        sha256="e78398e215d3fc6bc5984f5d1c2ddeac290dcbc8a8e9d196e828ef6299187db9",
        deprecated=True,
    )
    version(
        "22.05",
        sha256="2fa69e6a4db36459b67bf663e8fbf56191f6c8c25dc76301dbd02a36f9b50479",
        deprecated=True,
    )
    version(
        "22.04",
        sha256="9234d12e28b323cb250d3d2cefee0b36246bd8a1d1eb48e386f41977251c028f",
        deprecated=True,
    )
    version(
        "22.03",
        sha256="ddbef760c8000f2f827dfb097ca3359e7aecbea8766bec5c3a91ee28d3641564",
        deprecated=True,
    )
    version(
        "22.02",
        sha256="d74b593d6f396e037970c5fbe10c2e5d71d557a99c97d40e4255226bc6c26e42",
        deprecated=True,
    )
    version(
        "22.01",
        sha256="e465ffadabb7dc360c63c4d3862dc08082b5b0e77923d3fb05570408748b0d28",
        deprecated=True,
    )

    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="Enable MPI support")

    for v in [
        "23.08",
        "23.07",
        "23.06",
        "23.05",
        "23.04",
        "23.03",
        "23.02",
        "23.01",
        "22.12",
        "22.11",
        "22.10",
        "22.09",
        "22.08",
        "22.07",
        "22.06",
        "22.05",
        "22.04",
        "22.03",
        "22.02",
        "22.01",
        "develop",
    ]:
        depends_on("warpx@{0}".format(v), when="@{0}".format(v), type=["build", "link"])

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("python@3.8:", type=("build", "run"), when="@23.09:")
    depends_on("py-numpy@1.15.0:1", type=("build", "run"))
    depends_on("py-mpi4py@2.1.0:", type=("build", "run"), when="+mpi")
    depends_on("py-periodictable@1.5:1", type=("build", "run"))
    depends_on("py-picmistandard@0.25.0", type=("build", "run"), when="@23.07:")
    depends_on("py-picmistandard@0.24.0", type=("build", "run"), when="@23.06")
    depends_on("py-picmistandard@0.23.2", type=("build", "run"), when="@23.04:23.05")
    depends_on("py-picmistandard@0.0.22", type=("build", "run"), when="@22.12:23.03")
    depends_on("py-picmistandard@0.0.20", type=("build", "run"), when="@22.10:22.11")
    depends_on("py-picmistandard@0.0.19", type=("build", "run"), when="@22.02:22.09")
    depends_on("py-picmistandard@0.0.18", type=("build", "run"), when="@22.01")
    depends_on("py-setuptools@42:", type="build")
    # Since we use PYWARPX_LIB_DIR to pull binaries out of the
    # 'warpx' spack package, we don't need cmake as declared
    depends_on("warpx +lib ~mpi +shared", type=("build", "link"), when="~mpi")
    depends_on("warpx +lib +mpi +shared", type=("build", "link"), when="+mpi")

    def setup_build_environment(self, env):
        env.set("PYWARPX_LIB_DIR", self.spec["warpx"].prefix.lib)
