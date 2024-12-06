# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class MochiThallium(CMakePackage):
    """A Mochi C++14 library wrapping Margo, Mercury,
    and Argobots and providing an object-oriented way to use these libraries."""

    homepage = "https://github.com/mochi-hpc/mochi-thallium"
    url = "https://github.com/mochi-hpc/mochi-thallium/archive/refs/tags/v0.8.5.tar.gz"
    git = "https://github.com/mochi-hpc/mochi-thallium.git"

    maintainers("mdorier")

    version("main", branch="main")
    version("0.11.3", sha256="d1ffd7ee1ccbcfb00f246cb29c5bc2560e59f8808609cbc19b7098aa8fc903c4")
    version("0.11.2", sha256="4f1e57ca843b7592525c179dec73bfb603a27fbda4feaf028d636e05c1b38e36")
    version("0.11.1", sha256="be99bec2309ce1945a777fba720175f409972cbf27b73388728a740d6406a040")
    version("0.11.0", sha256="c216310fdef9281e1c7e3264c148c560d7f5edd15816d35866efcc543185b7ee")
    version("0.10.1", sha256="5a8dc1f1622f4186b02fbabd47a8a33ca6be3d07757010f3d63d30e9f74fec8c")
    version("0.10.0", sha256="5319e25a42deab7c639e980885fe3be717cda2c2c693a1906f5a6c79b31edef8")
    version("0.9.1", sha256="dee884d0e054c838807f9c17781acfa99b26e3be1cc527bf09ceaa997336b3e4")
    version("0.9", sha256="6b867b73f5dd76ea160d83782980149f33ae3567c370cee63d945e2e94609331")
    version("0.8.5", sha256="2d6d1fd97ad5b38c848ece6428c27400f752d57254324bfd0f1ea660d6a815a6")
    version("0.8.4", sha256="cb3f98a399664f41917a9a046fac3058f6ec53c85174dd97d5befd361bec0727")
    version("0.8.3", sha256="47b7837796ebd362b993cda5131912372c4abbc17a6967d177e0c3687c44ab7d")
    version("0.8.2", sha256="c90e3551189bae3552aab9089ce6343995736d734199c762bb8fa790968092ed")
    version("0.8.1", sha256="3c7a72de3f77917432f9e751559f413845a68563477cc29bd127ca7126c5f64a")
    version("0.8", sha256="3032196b1e5d7031fa4f79e81a44503fd02bca3abdc25f6ae0a5f3943e6397e4")
    version("0.7", sha256="173be344445b36a6e21abc192ef228fb7ca9dbc33d4484f284b5f4d31c79b7de")
    version("0.6.1", sha256="3e13b7d615fca827baa7cbee518f33ee908752c394361ede7668f4c47770f9f3")
    version("0.6", sha256="849db7c6297f8dcbb7786a6c3a11db05b316b5f7f028e52fbab439a84986562f")
    version("0.5.4", sha256="e5dbd63c8ed9e5bb7548d9a5d04c240482115a245e1312052ca3c17b2fa4e21b")
    version("0.5.3", sha256="372567f4203840d98543da9f3d5ef3c7989735b46e60337205578d5c93cf4e02")
    version("0.5.2", sha256="fe4f92880a2e574456afd934cede109d973055db9ca2a4a915501d635e42b3e7")
    version("0.5.1", sha256="e43abe03c91e38eb865fe6179f389a66cc38f2962f6a5a7ac93b01259f15aa18")
    version("0.5", sha256="0f85bad3680e94af734eaf063ec08620d4c16e1c8f0c4f85ae1ba010fbac958c")
    version("0.4.2", sha256="cf04efbf01bcbecac121fbc5f5c0d40dca2074638c0682c86f55e72121f64829")
    version("0.4.1", sha256="65136c01f276be70592e600a8942cee76164ea4c9646f2deecc9fd83b3c5bcfc")
    version("0.4", sha256="51b7efe8706f47a1508624bbfba12d800a8374ac1db076897c7d01d85621d30f")
    version("0.3.4", sha256="1f0e56c4a8d1285dcc288a50dadd7803a9cd0a311dd7798fec0b0800877d933a")
    version("0.3.3", sha256="33a31d5ccba781343f0ec18396f895e5ed60d9a52b35d3667698754e2a8a639a")
    version("0.3.2", sha256="7d90269101c881af40b73b0ffe1d55baa7203075b277fe8763735cc52278cee5")
    version("0.3.1", sha256="61403b1ba5f4d205408e6a7e04c785df6dea02f59fe9fa1742db05aa752cc8a0")
    version("0.3", sha256="4f9f78e52c1725f6ea5f933d7548bde36729dd9eff08f58fe7fe40682bc5f748")

    depends_on("cxx", type="build")  # generated

    variant(
        "cereal",
        default=True,
        description="Use the cereal library for serialization",
        when="@0.4.1:",
    )

    depends_on("pkgconfig", type=("build"))
    depends_on("mochi-margo@0.12.0:", when="@0.11.2:")
    depends_on("mochi-margo@0.9.8:", when="@0.10.0:")
    depends_on("mochi-margo@0.7:", when="@0.7:")
    depends_on("mochi-margo@0.6:", when="@0.5:")
    depends_on("mochi-margo@0.5:", when="@0.4:0.4.2")
    depends_on("mochi-margo@0.4:", when="@:0.3.4")
    with when("+cereal"):
        depends_on("cereal@:1.3.0", when="@0.4.1:0.10.0")
        depends_on("cereal@1.3.1:", when="@0.10.1:")
    # thallium relies on std::decay_t
    conflicts("%gcc@:4.9.0")

    def cmake_args(self):
        args = []
        args.append(self.define_from_variant("ENABLE_CEREAL", "cereal"))
        return args
