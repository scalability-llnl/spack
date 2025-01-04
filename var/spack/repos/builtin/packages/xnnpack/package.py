# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xnnpack(CMakePackage):
    """High-efficiency floating-point neural network inference operators for
    mobile, server, and Web"""

    homepage = "https://github.com/google/XNNPACK"
    git = "https://github.com/google/XNNPACK.git"

    license("BSD-3-Clause")

    version("master", branch="master", deprecated=True)
    version("2024-02-29", commit="fcbf55af6cf28a4627bcd1f703ab7ad843f0f3a2")  # py-torch@2.3:
    version("2022-12-22", commit="51a987591a6fc9f0fc0707077f53d763ac132cbf")  # py-torch@2.0:2.2
    version("2022-02-16", commit="ae108ef49aa5623b896fc93d4298c49d1750d9ba")  # py-torch@1.12:1.13
    version("2021-06-21", commit="79cd5f9e18ad0925ac9a050b00ea5a36230072db")  # py-torch@1.10:1.11
    version("2021-02-22", commit="55d53a4e7079d38e90acd75dd9e4f9e781d2da35")  # py-torch@1.8:1.9
    version("2020-03-23", commit="1b354636b5942826547055252f3b359b54acff95")  # py-torch@1.6:1.7
    version("2020-02-24", commit="7493bfb9d412e59529bcbced6a902d44cfa8ea1c")  # py-torch@1.5

    generator("ninja")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    with default_args(type="build"):
        depends_on("cmake@3.15:", when="@2022-04-26:")
        depends_on("cmake@3.12:", when="@2022-02-15:")
        depends_on("cmake@3.5:")
        depends_on("python")

    # Resources must be exact commit
    # https://github.com/google/XNNPACK/issues/4023

    # cmake/DownloadCLog.cmake
    resource(
        name="clog",
        url="https://github.com/pytorch/cpuinfo/archive/4b5a76c4de21265ddba98fc8f259e136ad11411b.zip",
        sha256="6000cf2a0befe428d97ea921372397d049889cbd8a4cd5b93390c71415dd3b68",
        destination="deps",
        placement="clog",
        when="@2022-12-22:2023-01-17",
    )
    resource(
        name="clog",
        url="https://github.com/pytorch/cpuinfo/archive/d5e37adf1406cf899d7d9ec1d317c47506ccb970.tar.gz",
        sha256="3f2dc1970f397a0e59db72f9fca6ff144b216895c1d606f6c94a507c1e53a025",
        destination="deps",
        placement="clog",
        when="@:2022-02-16",
    )

    # cmake/DownloadCpuinfo.cmake
    resource(
        name="cpuinfo",
        url="https://github.com/pytorch/cpuinfo/archive/d6860c477c99f1fce9e28eb206891af3c0e1a1d7.zip",
        sha256="a615cac78fad03952cc3e1fd231ce789a8df6e81a5957b64350cb8200364b385",
        destination="deps",
        placement="cpuinfo",
        when="@2024-02-29:",
    )
    resource(
        name="cpuinfo",
        url="https://github.com/Maratyszcza/cpuinfo/archive/0a38bc5cf17837bf3b536b57b9d35a259b6b2283.zip",
        sha256="fc79c33f10b7dcb710c5eb0fcd7fe4467bf98cdc6ff1925883b175fbb800c53e",
        destination="deps",
        placement="cpuinfo",
        when="@2022-12-22",
    )
    resource(
        name="cpuinfo",
        url="https://github.com/pytorch/cpuinfo/archive/5916273f79a21551890fd3d56fc5375a78d1598d.zip",
        sha256="2a160c527d3c58085ce260f34f9e2b161adc009b34186a2baf24e74376e89e6d",
        destination="deps",
        placement="cpuinfo",
        when="@2021-02-22:2022-02-16",
    )
    resource(
        name="cpuinfo",
        url="https://github.com/pytorch/cpuinfo/archive/d6c0f915ee737f961915c9d17f1679b6777af207.tar.gz",
        sha256="146fc61c3cf63d7d88db963876929a4d373f621fb65568b895efa0857f467770",
        destination="deps",
        placement="cpuinfo",
        when="@2020-03-23",
    )
    resource(
        name="cpuinfo",
        url="https://github.com/pytorch/cpuinfo/archive/d5e37adf1406cf899d7d9ec1d317c47506ccb970.tar.gz",
        sha256="3f2dc1970f397a0e59db72f9fca6ff144b216895c1d606f6c94a507c1e53a025",
        destination="deps",
        placement="cpuinfo",
        when="@2020-02-24",
    )

    # cmake/DownloadFP16.cmake
    resource(
        name="fp16",
        url="https://github.com/Maratyszcza/FP16/archive/0a92994d729ff76a58f692d3028ca1b64b145d91.zip",
        sha256="e66e65515fa09927b348d3d584c68be4215cfe664100d01c9dbc7655a5716d70",
        destination="deps",
        placement="fp16",
        when="@2024-02-29:",
    )
    resource(
        name="fp16",
        url="https://github.com/Maratyszcza/FP16/archive/0a92994d729ff76a58f692d3028ca1b64b145d91.zip",
        sha256="e66e65515fa09927b348d3d584c68be4215cfe664100d01c9dbc7655a5716d70",
        destination="deps",
        placement="fp16",
        when="@2021-06-21:2022-12-22",
    )
    resource(
        name="fp16",
        url="https://github.com/Maratyszcza/FP16/archive/3c54eacb74f6f5e39077300c5564156c424d77ba.zip",
        sha256="0d56bb92f649ec294dbccb13e04865e3c82933b6f6735d1d7145de45da700156",
        destination="deps",
        placement="fp16",
        when="@2021-02-22",
    )
    resource(
        name="fp16",
        url="https://github.com/Maratyszcza/FP16/archive/ba1d31f5eed2eb4a69e4dea3870a68c7c95f998f.tar.gz",
        sha256="9764297a339ad73b0717331a2c3e9c42a52105cd04cab62cb160e2b4598d2ea6",
        destination="deps",
        placement="fp16",
        when="@:2020-03-23",
    )

    # cmake/DownloadFXdiv.cmake
    resource(
        name="fxdiv",
        url="https://github.com/Maratyszcza/FXdiv/archive/b408327ac2a15ec3e43352421954f5b1967701d1.zip",
        sha256="ab7dfb08829bee33dca38405d647868fb214ac685e379ec7ef2bebcd234cd44d",
        destination="deps",
        placement="fxdiv",
        when="@2021-02-22:",
    )
    resource(
        name="fxdiv",
        url="https://github.com/Maratyszcza/FXdiv/archive/f8c5354679ec2597792bc70a9e06eff50c508b9a.tar.gz",
        sha256="7d3215bea832fe77091ec5666200b91156df6724da1e348205078346325fc45e",
        destination="deps",
        placement="fxdiv",
        when="@:2020-03-23",
    )

    # cmake/DownloadPSimd.cmake
    # Not listed in newer versions but FP16 needs it
    resource(
        name="psimd",
        url="https://github.com/Maratyszcza/psimd/archive/10b4ffc6ea9e2e11668f86969586f88bc82aaefa.tar.gz",
        sha256="1fefd66702cb2eb3462b962f33d4fb23d59a55d5889ee6372469d286c4512df4",
        destination="deps",
        placement="psimd",
    )

    # cmake/DownloadPThreadPool.cmake
    resource(
        name="pthreadpool",
        url="https://github.com/Maratyszcza/pthreadpool/archive/4fe0e1e183925bf8cfa6aae24237e724a96479b8.zip",
        sha256="a4cf06de57bfdf8d7b537c61f1c3071bce74e57524fe053e0bbd2332feca7f95",
        destination="deps",
        placement="pthreadpool",
        when="@2024-02-29:",
    )
    resource(
        name="pthreadpool",
        url="https://github.com/Maratyszcza/pthreadpool/archive/43edadc654d6283b4b6e45ba09a853181ae8e850.zip",
        sha256="e6370550a1abf1503daf3c2c196e0a1c2b253440c39e1a57740ff49af2d8bedf",
        destination="deps",
        placement="pthreadpool",
        when="@2022-12-22",
    )
    resource(
        name="pthreadpool",
        url="https://github.com/Maratyszcza/pthreadpool/archive/545ebe9f225aec6dca49109516fac02e973a3de2.zip",
        sha256="8461f6540ae9f777ce20d1c0d1d249e5e61c438744fb390c0c6f91940aa69ea3",
        destination="deps",
        placement="pthreadpool",
        when="@2021-02-22:2022-02-16",
    )
    resource(
        name="pthreadpool",
        url="https://github.com/Maratyszcza/pthreadpool/archive/ebd50d0cfa3664d454ffdf246fcd228c3b370a11.zip",
        sha256="ca4fc774cf2339cb739bba827de8ed4ccbd450c4608e05329e974153448aaf56",
        destination="deps",
        placement="pthreadpool",
        when="@2020-03-23",
    )
    resource(
        name="pthreadpool",
        url="https://github.com/Maratyszcza/pthreadpool/archive/7ad026703b3109907ad124025918da15cfd3f100.tar.gz",
        sha256="96eb4256fc438b7b8cab40541d383efaf546fae7bad380c24ea601c326c5f685",
        destination="deps",
        placement="pthreadpool",
        when="@2020-02-24",
    )

    # May be possible to disable NEON dot product instructions
    # https://github.com/google/XNNPACK/issues/1551
    conflicts("%gcc@:8")

    # https://github.com/google/XNNPACK/pull/2797
    patch("2797.patch", when="@:2022-03-27")

    def cmake_args(self):
        # TODO: XNNPACK has a XNNPACK_USE_SYSTEM_LIBS option, but it seems to be broken
        # See https://github.com/google/XNNPACK/issues/1543
        args = [
            self.define(
                "CPUINFO_SOURCE_DIR", join_path(self.stage.source_path, "deps", "cpuinfo")
            ),
            self.define("FP16_SOURCE_DIR", join_path(self.stage.source_path, "deps", "fp16")),
            self.define("FXDIV_SOURCE_DIR", join_path(self.stage.source_path, "deps", "fxdiv")),
            self.define(
                "PTHREADPOOL_SOURCE_DIR", join_path(self.stage.source_path, "deps", "pthreadpool")
            ),
            self.define("PSIMD_SOURCE_DIR", join_path(self.stage.source_path, "deps", "psimd")),
            # https://github.com/pytorch/pytorch/blob/main/cmake/Dependencies.cmake
            self.define("XNNPACK_LIBRARY_TYPE", "static"),
            self.define("XNNPACK_BUILD_BENCHMARKS", False),
            self.define("XNNPACK_BUILD_TESTS", False),
            self.define("CMAKE_POSITION_INDEPENDENT_CODE", True),
        ]

        if self.spec.satisfies("@:2023-01-17"):
            args.append(
                self.define("CLOG_SOURCE_DIR", join_path(self.stage.source_path, "deps", "clog"))
            )

        return args
