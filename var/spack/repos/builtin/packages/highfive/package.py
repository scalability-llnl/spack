# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.pkg.builtin.boost import Boost


class Highfive(CMakePackage):
    """HighFive - Header only C++ HDF5 interface"""

    homepage = "https://github.com/BlueBrain/HighFive"
    url = "https://github.com/BlueBrain/HighFive/archive/v1.2.tar.gz"
    git = "https://github.com/BlueBrain/HighFive.git"
    maintainers("alkino")

    license("BSL-1.0")

    version("develop", branch="master")
    version("2.10.0", sha256="c29e8e1520e7298fabb26545f804e35bb3af257005c1c2df62e39986458d7c38")
    version("2.9.0", sha256="6301def8ceb9f4d7a595988612db288b448a3c0546f6c83417dab38c64994d7e")
    version("2.8.0", sha256="cd2502cae61bfb00e32dd18c9dc75289e09ad1db5c2a46d3b0eefd32e0df983b")
    version("2.7.1", sha256="25b4c51a94d1e670dc93b9b73f51e79b65d8ff49bcd6e5d5582d5ecd2789a249")
    version("2.7.0", sha256="8e05672ddf81a59ce014b1d065bd9a8c5034dbd91a5c2578e805ef880afa5907")
    version("2.6.2", sha256="ab51b9fbb49e877dd1aa7b53b4b26875f41e4e0b8ee0fc2f1d735e0d1e43d708")
    version("2.6.1", sha256="b5002c1221cf1821e02fb2ab891b0160bac88b43f56655bd844a472106ca3397")
    version("2.6.0", sha256="9f9828912619ba27d6f3a30e77c27669d9f19f6ee9170f79ee5f1ea96f85a4cd")
    version("2.5.0", sha256="27f55596570df3cc8b878a1681a0d4ba0fe2e3da4a0ef8d436722990d77dc93a")
    version("2.4.1", sha256="6826471ef5c645ebf947d29574b302991525a8a8ff1ef687aba7311d9a0ea36f")
    version("2.4.0", sha256="ba0ed6d8e2e09e80849926f38c15a26cf4b80772084cea0555269a25fec02149")
    version("2.3.1", sha256="41728a1204bdfcdcef8cbc3ddffe5d744c5331434ce3dcef35614b831234fcd7")
    version("2.3", sha256="7da6815646eb4294f210cec6be24c9234d7d6ceb2bf92a01129fbba6583c5349")
    version("2.2.2", sha256="5bfb356705c6feb9d46a0507573028b289083ec4b4607a6f36187cb916f085a7")
    version("2.2.1", sha256="964c722ba916259209083564405ef9ce073b15e9412955fef9281576ea9c5b85")
    version("2.2", sha256="fe065f2443e38444100b43999a96916e81a0aa7e500cf768d3bf6f8392b8efee")
    version("2.1.1", sha256="52cffeda0d018f020f48e5460c051d5c2031c3a3c82133a21527f186a0c1650e")
    version("2.0", sha256="deee33d7f578e33dccb5d04771f4e01b89a980dd9a3ff449dd79156901ee8d25")
    version("1.5", sha256="f194bda482ab15efa7c577ecc4fb7ee519f6d4bf83470acdb3fb455c8accb407")
    version("1.2", sha256="4d8f84ee1002e8fd6269b62c21d6232aea3d56ce4171609e39eb0171589aab31")
    version("1.1", sha256="430fc312fc1961605ffadbfad82b9753a5e59482e9fbc64425fb2c184123d395")
    version("1.0", sha256="d867fe73d00817f686d286f3c69a23731c962c3e2496ca1657ea7302cd0bb944")

    depends_on("cxx", type="build")  # generated

    variant("boost", default=False, description="Support Boost")
    variant("mpi", default=True, description="Support MPI")

    depends_on("boost @1.41:", when="+boost")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when="+boost")
    depends_on("hdf5")
    depends_on("hdf5 +mpi", when="+mpi")

    def cmake_args(self):
        args = [
            "-DUSE_BOOST:Bool={0}".format(self.spec.satisfies("+boost")),
            "-DHIGHFIVE_PARALLEL_HDF5:Bool={0}".format(self.spec.satisfies("+mpi")),
            "-DHIGHFIVE_UNIT_TESTS:Bool=false",
            "-DHIGHFIVE_EXAMPLES:Bool=false",
        ]
        return args
