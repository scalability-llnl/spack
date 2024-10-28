# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.url
from spack.package import *


class Protobuf(CMakePackage):
    """Google's data interchange format."""

    homepage = "https://developers.google.com/protocol-buffers"
    url = "https://github.com/protocolbuffers/protobuf/archive/v3.18.0.tar.gz"
    maintainers("hyoklee")

    license("BSD-3-Clause")

    version("3.28.2", sha256="1b6b6a7a7894f509f099c4469b5d4df525c2f3c9e4009e5b2db5b0f66cb8ee0e")
    version("3.27.5", sha256="a4aa92d0a207298149bf553d9a3192f3562eb91740086f50fa52331e60fa480c")
    version("3.26.1", sha256="f3c0830339eaa5036eba8ff8ce7fca5aa3088f7d616f7c3713d946f611ae92bf")
    version("3.25.3", sha256="da82be8acc5347c7918ef806ebbb621b24988f7e1a19b32cd7fc73bc29b59186")
    version("3.24.3", sha256="2c23dee0bdbc36bd43ee457083f8f5560265d0815cc1c56033de3932843262fe")
    version("3.23.3", sha256="5e4b555f72a7e3f143a7aff7262292500bb02c49b174351684bb70fc7f2a6d33")
    version("3.22.2", sha256="2118051b4fb3814d59d258533a4e35452934b1ddb41230261c9543384cbb4dfc")
    version("3.21.12", sha256="930c2c3b5ecc6c9c12615cf5ad93f1cd6e12d0aba862b572e076259970ac3a53")
    version("3.21.9", sha256="1add10f9bd92775b91f326da259f243881e904dd509367d5031d4c782ba82810")
    version("3.21.7", sha256="ce2fbea3c78147a41b2a922485d283137845303e5e1b6cbd7ece94b96ade7031")
    version("3.21.5", sha256="d7d204a59fd0d2d2387bd362c2155289d5060f32122c4d1d922041b61191d522")
    version("3.21.4", sha256="85d42d4485f36f8cec3e475a3b9e841d7d78523cd775de3a86dba77081f4ca25")
    version("3.21.3", sha256="c29d8b4b79389463c546f98b15aa4391d4ed7ec459340c47bffe15db63eb9126")
    version("3.21.2", sha256="66e1156ac78290db81335c79d1fc5a54123ebb62a43eb2e5b42a44ca23087517")
    version("3.21.1", sha256="a295dd3b9551d3e2749a9969583dea110c6cdcc39d02088f7c7bb1100077e081")
    version("3.20.3", sha256="9c0fd39c7a08dff543c643f0f4baf081988129a411b977a07c46221793605638")
    version("3.20.2", sha256="88231778cffebf93bc905e76ea757fae0f2ef497cc00f64973e41f1acd4fc781")
    version("3.20.1", sha256="8b28fdd45bab62d15db232ec404248901842e5340299a57765e48abe8a80d930")
    version("3.20.0", sha256="b07772d38ab07e55eca4d50f4b53da2d998bb221575c60a4f81100242d4b4889")
    version("3.19.4", sha256="3bd7828aa5af4b13b99c191e8b1e884ebfa9ad371b0ce264605d347f135d2568")
    version("3.19.3", sha256="390191a0d7884b3e52bb812c440ad1497b9d484241f37bb8e2ccc8c2b72d6c36")
    version("3.19.2", sha256="4dd35e788944b7686aac898f77df4e9a54da0ca694b8801bd6b2a9ffc1b3085e")
    version("3.18.2", sha256="579cd41bf322adb2b1161a46e076e39d3d01d1e8c50b8b61ce444211dae4e632")
    version("3.18.0", sha256="14e8042b5da37652c92ef6a2759e7d2979d295f60afd7767825e3de68c856c54")
    version("3.17.3", sha256="c6003e1d2e7fefa78a3039f19f383b4f3a61e81be8c19356f85b6461998ad3db")
    version("3.17.0", sha256="eaba1dd133ac5167e8b08bc3268b2d33c6e9f2dcb14ec0f97f3d3eed9b395863")
    version("3.16.0", sha256="7892a35d979304a404400a101c46ce90e85ec9e2a766a86041bb361f626247f5")
    version("3.15.7", sha256="efdd6b932a2c0a88a90c4c80f88e4b2e1bf031e7514dbb5a5db5d0bf4f295504")
    version("3.15.5", sha256="bc3dbf1f09dba1b2eb3f2f70352ee97b9049066c9040ce0c9b67fb3294e91e4b")
    version("3.15.4", sha256="07f8a02afc14a657f727ed89a8ec5627b9ecc47116d60acaabaa1da233bd2e8f")
    version("3.15.2", sha256="3c85fdac243dab1f6cd725eb58e361cdbb3ec4480052ac90b1ab55c608112cd0")
    version("3.15.1", sha256="f18a40816260a9a3190a94efb0fc26270b244a2436681602f0a944739095d632")
    version("3.15.0", sha256="6aff9834fd7c540875e1836967c8d14c6897e3785a2efac629f69860fb7834ff")
    version("3.14.0", sha256="d0f5f605d0d656007ce6c8b5a82df3037e1d8fe8b121ed42e536f569dec16113")
    version("3.13.0", sha256="9b4ee22c250fe31b16f1a24d61467e40780a3fbb9b91c3b65be2a376ed913a1a")
    version("3.12.3", sha256="71030a04aedf9f612d2991c1c552317038c3c5a2b578ac4745267a45e7037c29")
    version("3.12.2", sha256="bb8ce9ba11eb7bccf080599fe7cad9cc461751c8dd1ba61701c0070d58cde973")
    version("3.12.1", sha256="cb9b3f9d625b5739a358268eb3421de11cacd90025f5f7672c3930553eca810e")
    version("3.12.0", sha256="946ba5371e423e1220d2cbefc1f65e69a1e81ca5bab62a03d66894172983cfcd")
    version("3.11.4", sha256="a79d19dcdf9139fa4b81206e318e33d245c4c9da1ffed21c87288ed4380426f9")
    version("3.11.3", sha256="cf754718b0aa945b00550ed7962ddc167167bd922b842199eeb6505e6f344852")
    version("3.11.2", sha256="e8c7601439dbd4489fe5069c33d374804990a56c2f710e00227ee5d8fd650e67")
    version("3.11.1", sha256="4f8e805825c53bbc3c9f6b6abc009b5b5679e4702bccfca1121c42ff5ec801c7")
    version("3.11.0", sha256="6d356a6279cc76d2d5c4dfa6541641264b59eae0bc96b852381361e3400d1f1c")
    version("3.10.1", sha256="6adf73fd7f90409e479d6ac86529ade2d45f50494c5c10f539226693cb8fe4f7")
    version("3.10.0", sha256="758249b537abba2f21ebc2d02555bf080917f0f2f88f4cbe2903e0e28c4187ed")
    version("3.9.2", sha256="1fbf1c2962af287607232b2eddeaec9b4f4a7a6f5934e1a9276e9af76952f7e0")
    version("3.9.1", sha256="98e615d592d237f94db8bf033fba78cd404d979b0b70351a9e5aaff725398357")
    version("3.8.0", sha256="03d2e5ef101aee4c2f6ddcf145d2a04926b9c19e7086944df3842b1b8502b783")
    version("3.7.1", sha256="f1748989842b46fa208b2a6e4e2785133cfcc3e4d43c17fecb023733f0f5443f")
    version("3.7.0", sha256="a19dcfe9d156ae45d209b15e0faed5c7b5f109b6117bfc1974b6a7b98a850320")
    version("3.6.1", sha256="3d4e589d81b2006ca603c1ab712c9715a76227293032d05b26fca603f90b3f5b")
    version("3.5.2", sha256="4ffd420f39f226e96aebc3554f9c66a912f6cad6261f39f194f16af8a1f6dab2")
    version("3.5.1.1", sha256="56b5d9e1ab2bf4f5736c4cfba9f4981fbc6976246721e7ded5602fbaee6d6869")
    version("3.5.1", sha256="826425182ee43990731217b917c5c3ea7190cfda141af4869e6d4ad9085a740f")
    version("3.5.0.1", sha256="86be71e61c76575c60839452a4f265449a6ea51570d7983cb929f06ad294b5f5")
    version("3.5.0", sha256="0cc6607e2daa675101e9b7398a436f09167dffb8ca0489b0307ff7260498c13c")
    version("3.4.1", sha256="8e0236242106e680b4f9f576cc44b8cd711e948b20a9fc07769b0a20ceab9cc4")
    version("3.4.0", sha256="f6600abeee3babfa18591961a0ff21e7db6a6d9ef82418a261ec4fee44ee6d44")
    version("3.3.0", sha256="9a36bc1265fa83b8e818714c0d4f08b8cec97a1910de0754a321b11e66eb76de")
    version("3.2.0", sha256="a839d3f1519ff9d68ab908de5a0f269650ef1fc501c10f6eefd4cae51d29b86f")
    version("3.1.0", sha256="fb2a314f4be897491bb2446697be693d489af645cb0e165a85e7e64e07eb134d")
    version("3.0.2", sha256="a0a265bcc9d4e98c87416e59c33afc37cede9fb277292523739417e449b18c1e")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant("shared", default=True, description="Enables the build of shared libraries")
    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release", "RelWithDebInfo"),
    )

    depends_on("abseil-cpp@20230125.3:", when="@3.22.5:")
    # https://github.com/protocolbuffers/protobuf/issues/11828#issuecomment-1433557509
    depends_on("abseil-cpp@20230125:", when="@3.22:")
    depends_on("zlib-api")

    conflicts("%gcc@:4.6", when="@3.6.0:")  # Requires c++11
    conflicts("%gcc@:4.6", when="@3.2.0:3.3.0")  # Breaks

    # first fixed in 3.4.0: https://github.com/google/protobuf/pull/3406
    patch("pkgconfig.patch", when="@3.0.2:3.3.2")

    patch("intel-v1.patch", when="@3.2:3.6 %intel")

    # See https://github.com/protocolbuffers/protobuf/pull/7197
    patch("intel-v2.patch", when="@3.7:3.11.4 %intel")

    # See https://github.com/protocolbuffers/protobuf/issues/9916
    patch(
        "https://github.com/protocolbuffers/protobuf/pull/9936.patch?full_index=1",
        when="@3.20 %gcc@12.1.0",
        sha256="fa1abf042eddc1b3b43875dc018c651c90cd1c0c5299975a818a1610bee54ab8",
    )

    # fix build on Centos 8, see also https://github.com/protocolbuffers/protobuf/issues/5144
    patch(
        "https://github.com/protocolbuffers/protobuf/commit/462964ed322503af52638d54c00a0a67d7133349.patch?full_index=1",
        when="@3.4:3.21",
        sha256="9b6dcfa30dd3ae0abb66ab0f252a4fc1e1cc82a9820d2bdb72da35c4f80c3603",
    )

    patch("msvc-abseil-target-namespace.patch", when="@3.22 %msvc")

    # Misisng #include "absl/container/internal/layout.h"
    # See https://github.com/protocolbuffers/protobuf/pull/14042
    patch(
        "https://github.com/protocolbuffers/protobuf/commit/e052928c94f5a9a6a6cbdb82e09ab4ee92b7815f.patch?full_index=1",
        when="@3.22:3.24.3 ^abseil-cpp@20240116:",
        sha256="20e3cc99a9513b256e219653abe1bfc7d6b6a5413e269676e3d442830f99a1af",
    )

    # Missing #include "absl/strings/str_cat.h"
    # See https://github.com/protocolbuffers/protobuf/pull/14054
    patch(
        "https://github.com/protocolbuffers/protobuf/commit/38a24729ec94e6576a1425951c898ad0b91ad2d2.patch?full_index=1",
        when="@3.22:3.24.3 ^abseil-cpp@20240116:",
        sha256="c061356db31cdce29c8cdd98a3a8219ef048ebc2318d0dec26c1f2c5e5dae29b",
    )

    def fetch_remote_versions(self, *args, **kwargs):
        """Ignore additional source artifacts uploaded with releases,
        only keep known versions
        fix for https://github.com/spack/spack/issues/5356"""
        return dict(
            map(
                lambda u: (u, self.url_for_version(u)),
                spack.url.find_versions_of_archive(self.all_urls, self.list_url, self.list_depth),
            )
        )

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("protobuf_BUILD_TESTS", False),
            self.define("CMAKE_POSITION_INDEPENDENT_CODE", True),
        ]

        if self.spec.satisfies("@3.22:"):
            cxxstd = self.spec["abseil-cpp"].variants["cxxstd"].value
            args.extend(
                [
                    self.define("protobuf_ABSL_PROVIDER", "package"),
                    self.define("CMAKE_CXX_STANDARD", cxxstd),
                ]
            )

        if self.spec.satisfies("platform=darwin"):
            args.append(self.define("CMAKE_MACOSX_RPATH", True))

        return args

    @property
    def root_cmakelists_dir(self):
        if self.spec.satisfies("@:3.20"):
            return join_path(self.stage.source_path, "cmake")
        else:
            return self.stage.source_path
