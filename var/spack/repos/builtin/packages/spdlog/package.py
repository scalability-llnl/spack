# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Spdlog(CMakePackage):
    """Very fast, header only, C++ logging library"""

    homepage = "https://github.com/gabime/spdlog"
    url = "https://github.com/gabime/spdlog/archive/v0.9.0.tar.gz"

    license("MIT")

    version("1.14.1", sha256="1586508029a7d0670dfcb2d97575dcdc242d3868a259742b69f100801ab4e16b")
    version("1.13.0", sha256="534f2ee1a4dcbeb22249856edfb2be76a1cf4f708a20b0ac2ed090ee24cfdbc9")
    version("1.12.0", sha256="4dccf2d10f410c1e2feaff89966bfc49a1abb29ef6f08246335b110e001e09a9")
    version("1.11.0", sha256="ca5cae8d6cac15dae0ec63b21d6ad3530070650f68076f3a4a862ca293a858bb")
    version("1.10.0", sha256="697f91700237dbae2326b90469be32b876b2b44888302afbc7aceb68bcfe8224")
    version("1.9.2", sha256="6fff9215f5cb81760be4cc16d033526d1080427d236e86d70bb02994f85e3d38")
    version("1.9.1", sha256="9a452cfa24408baccc9b2bc2d421d68172a7630c99e9504a14754be840d31a62")
    version("1.9.0", sha256="9ad181d75aaedbf47c8881e7b947a47cac3d306997e39de24dba60db633e70a7")
    version("1.8.5", sha256="944d0bd7c763ac721398dca2bb0f3b5ed16f67cef36810ede5061f35a543b4b8")
    version("1.8.4", sha256="d19cff06a3d235efcb451e04193a925bebc6ef7e7bd4a56ca27096acbab3cf3b")
    version("1.8.3", sha256="6f5b88ca4c9b96264e6c961716fec6f1a7b94c80a5edce667c3e42507caa8a82")
    version("1.8.2", sha256="e20e6bd8f57e866eaf25a5417f0a38a116e537f1a77ac7b5409ca2b180cec0d5")
    version("1.8.1", sha256="5197b3147cfcfaa67dd564db7b878e4a4b3d9f3443801722b3915cdeced656cb")
    version("1.8.0", sha256="1e68e9b40cf63bb022a4b18cdc1c9d88eb5d97e4fd64fa981950a9cacf57a4bf")
    version("1.7.0", sha256="f0114a4d3c88be9e696762f37a7c379619443ce9d668546c61b21d41affe5b62")
    version("1.6.1", sha256="378a040d91f787aec96d269b0c39189f58a6b852e4cbf9150ccfacbe85ebbbfc")
    version("1.6.0", sha256="0421667c9f2fc78e6548d44f7bc5921be0f03e612df384294c16cedb93d967f8")
    version("1.5.0", sha256="b38e0bbef7faac2b82fed550a0c19b0d4e7f6737d5321d4fd8f216b80f8aee8a")
    version("1.4.2", sha256="821c85b120ad15d87ca2bc44185fa9091409777c756029125a02f81354072157")
    version("1.4.1", sha256="3291958eb54ed942d1bd3aef1b4f8ccf70566cbc04d34296ec61eb96ceb73cff")
    version("1.2.1", sha256="867a4b7cedf9805e6f76d3ca41889679054f7e5a3b67722fe6d0eae41852a767")
    version("1.2.0", sha256="0ba31b9e7f8e43a7be328ab0236d57810e5d4fc8a1a7842df665ae22d5cbd128")
    version("1.1.0", sha256="3dbcbfd8c07e25f5e0d662b194d3a7772ef214358c49ada23c044c4747ce8b19")
    version("1.0.0", sha256="90d5365121bcd2c41ce94dfe6a460e89507a2dfef6133fe5fad5bb35ac4ef0a1")
    version("0.17.0", sha256="94f74fd1b3344733d1db3de2ec22e6cbeb769f93a8baa0d4a22b1f62dc7369f8")
    version("0.16.3", sha256="b88d7be261d9089c817fc8cee6c000d69f349b357828e4c7f66985bc5d5360b8")
    version("0.16.2", sha256="2081e5df5e87402398847431e16b87c71dd5c4d632314bb976ace8161f4d32de")
    version("0.16.1", sha256="733260e1fbdcf1b3dc307fc585e4476240026de8be28eb905731d2ab0942deae")
    version("0.16.0", sha256="9e64e3b10c2a3c54dfff63aa056057cf1db8a5fd506b3d9cf77207511820baac")
    version("0.14.0", sha256="eb5beb4e53f4bfff5b32eb4db8588484bdc15a17b90eeefef3a9fc74fec1d83d")
    version("0.13.0", sha256="d798a6ca19165f0a18a43938859359269f5a07fd8e0eb83ab8674739c9e8f361")
    version("0.12.0", sha256="5cfd6a0b3182a88e1eb35bcb65a7ef9035140d7c73b16ba6095939dbf07325b9")
    version("0.11.0", sha256="8c0f1810fb6b7d23fef70c2ea8b6fa6768ac8d18d6e0de39be1f48865e22916e")
    version("0.10.0", sha256="fbbc53c1cc09b93b4c3d76b683bbe9315e2efe3727701227374dce6aa4264075")
    version("0.9.0", sha256="bbbe5a855c8b309621352921d650449eb2f741d35d55ec50fb4d8122ddfb8f01")

    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Build shared libraries (v1.4.0+)")

    depends_on("cmake@3.2:", when="@:1.7.0", type="build")
    depends_on("cmake@3.10:", when="@1.8.0:", type="build")
    depends_on("cmake@3.11:", when="@1.13.0:", type="build")

    depends_on("fmt@5.3:")
    depends_on("fmt@7:", when="@1.7:")
    depends_on("fmt@8:", when="@1.9:")
    depends_on("fmt@9:", when="@1.11:")

    # spdlog@1.11.0 with fmt@10  https://github.com/gabime/spdlog/pull/2694
    patch(
        "https://github.com/gabime/spdlog/commit/0ca574ae168820da0268b3ec7607ca7b33024d05.patch?full_index=1",
        sha256="31b22a9bfa6790fdabff186c0a9b0fd588439485f05cbef5e661231d15fec49b",
        when="@1.11.0 ^fmt@10:",
    )

    def cmake_args(self):
        args = []

        if self.spec.satisfies("@1.4.0:"):
            args.extend(
                [
                    self.define_from_variant("SPDLOG_BUILD_SHARED", "shared"),
                    self.define("SPDLOG_FMT_EXTERNAL", True),
                    # tests and examples
                    self.define("SPDLOG_BUILD_TESTS", self.run_tests),
                    self.define("SPDLOG_BUILD_EXAMPLE", self.run_tests),
                ]
            )

        return args
