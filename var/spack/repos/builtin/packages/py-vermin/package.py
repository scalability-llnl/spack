# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyVermin(PythonPackage):
    """Concurrently detect the minimum Python versions needed to run code."""

    homepage = "https://github.com/netromdk/vermin"
    url = "https://github.com/netromdk/vermin/archive/v1.6.0.tar.gz"

    maintainers("netromdk")

    license("MIT")

    version("1.6.0", sha256="31200b1e674e064c7473484372db2743f5abbf1409d994880486bca5bcf05bec")
    version("1.5.2", sha256="e4b6ca6f3e71b0d83a179dc4a4ba50682f60474cf8c948ba9f82e330f219ff4a")
    version("1.5.1", sha256="2d1c7601d054da9fa5c5eb6c817c714235f9d484b74011f7f86c98f0a25e93ea")
    version("1.5.0", sha256="77207385c9cea1f02053a8f2e7f2e8c945394cf37c44c70ce217cada077a2d17")
    version("1.4.2", sha256="c9a69420b610bfb25d5a2abd7da6edf0ae4329481a857ef6c5d71f602ed5c63d")
    version("1.4.1", sha256="ee69d5e84f0d446e0d6574ec60c428798de6e6c8d055589f65ac02f074a7da25")
    version("1.4.0", sha256="984773ed6af60329e700b39c58b7584032acbc908a00b5a76d1ce5468c825c70")
    version("1.3.3", sha256="35cd8bc3f54f651dbb162a7b35b4b091409154ce6d565df043f7f04bf9401d7d")
    version("1.3.2", sha256="2818eaea24c5be5dae1f374ddb2377e9cfaad04d0a3372ad129cffc46cec5404")
    version("1.3.1", sha256="ddcdaad5a708a483af192075f5d2eaaaf3aa4661b5101ddafa40d7837eeb5368")
    version("1.3.0", sha256="adf2b6ea34c01c3a81fc4fa78c2e5fa6c8dd6d35327a8e5a4caeeaef7ec21668")
    version("1.2.2", sha256="d0343b2a78d7e4de67dfd2d882eeaf8b241db724f7e67f83bdd4111edb97f1e2")
    version("1.2.1", sha256="b7b2c77cf67a27a432371cbc7f184151b6f3dd22bd9ccf3a7a10b7ae3532ac81")
    version("1.2.0", sha256="a3ab6dc6608b859f301b9a77d5cc0d03335aae10c49d47a91b82be5be48c4f1f")
    version("1.1.1", sha256="d13b2281ba16c9d5b0913646483771789552230a9ed625e2cd92c5a112e4ae80")
    version("1.1.0", sha256="62d9f1b6694f50c22343cead2ddb6e2b007d24243fb583f61ceed7540fbe660b")
    version("1.0.3", sha256="1503be05b55cacde1278a1fe55304d8ee889ddef8ba16e120ac6686259bec95c")
    version("1.0.2", sha256="e999d5f5455e1116b366cd1dcc6fecd254c7ae3606549a61bc044216f9bb5b55")
    version("1.0.1", sha256="c06183ba653b9d5f6687a6686da8565fb127fab035f9127a5acb172b7c445079")
    version("1.0.0", sha256="e598e9afcbe3fa6f3f3aa894da81ccb3954ec9c0783865ecead891ac6aa57207")
    version("0.10.5", sha256="00601356e8e10688c52248ce0acc55d5b45417b462d5aa6887a6b073f0d33e0b")
    version("0.10.4", sha256="bd765b84679fb3756b26f462d2aab4af3183fb65862520afc1517f6b39dea8bf")
    version("0.10.0", sha256="3458a4d084bba5c95fd7208888aaf0e324a07ee092786ee4e5529f539ab4951f")

    depends_on("py-setuptools", type=("build"))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def build_test(self):
        make("test")
