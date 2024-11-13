# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Onednn(CMakePackage):
    """oneAPI Deep Neural Network Library (oneDNN).

    Formerly known as Intel MKL-DNN and DNNL."""

    homepage = "https://01.org/onednn"
    url = "https://github.com/oneapi-src/oneDNN/archive/v1.7.tar.gz"
    git = "https://github.com/oneapi-src/oneDNN.git"

    maintainers("adamjstewart")

    license("Apache-2.0")

    version("master", branch="master")
    version("3.0", sha256="b93ac6d12651c060e65086396d85191dabecfbc01f30eb1f139c6dd56bf6e34c")
    version("2.7.3", sha256="a50993aa6265b799b040fe745e0010502f9f7103cc53a9525d59646aef006633")
    version("2.5.2", sha256="11d50235afa03571dc70bb6d96a98bfb5d9b53e8c00cc2bfbde78588bd01f6a3")
    version("2.1-rc", sha256="13d293e7368a8fdd8dd3c11c73352cf5f564398658dd027ce0acde947440b4cb")
    version("2.0", sha256="922b42c3ea7a7122a77c61568dc4512aa8130c264c0489283c989919d1f59a6d")
    version("1.8.1", sha256="1883ccfb037bd31f916203a38e877899fc27ae10bc9ebad686f78d189ba506a7")
    version("1.8", sha256="0a1bfbbc6fd86c6ea4cf0f7c36fe3e69b0bbefa74158c65a5db28d589cb5fbe9")
    version("1.7", sha256="2dbd53578b36bd84bbc3e411d1a4cacc0eed832892818c5fa16b72cbf1dab015")
    version("1.6.5", sha256="6258d961fe1757b70d10cf34f0925079401ffae264f056b15024270b11d5c1eb")
    version("1.6.4", sha256="5369f7b2f0b52b40890da50c0632c3a5d1082d98325d0f2bff125d19d0dcaa1d")
    version("1.6.3", sha256="471c877671f672e4119e5f49143890c5ce2efff80a52a5eaf7ef3730eb3e1738")
    version("1.6.2", sha256="83533fcf81cd4c4565bf640b895d1ea0a4563a5dac88af8e5c05813f1af13e25")
    version("1.6.1", sha256="6686d01d9493905c9c8bcfabcf5b2cc9ced7de7a41c52bba99e569fd5b63464d")
    version("1.6", sha256="f54893e487ccd99586725afdd19f526bb84e3251222586850782e3c7eedb7c4f")
    version("1.5.1", sha256="aef4d2a726f76f5b98902491a1a4ac69954039aa8e5a1d67ef6ce58ed00e23a6")
    version("1.5", sha256="2aacc00129418185e0bc1269d3ef82f93f08de2c336932989c0c360279129edb")
    version("1.4", sha256="54737bcb4dc1961d32ee75da3ecc529fa48198f8b2ca863a079e19a9c4adb70f")
    version("1.3", sha256="b87c23b40a93ef5e479c81028db71c4847225b1a170f82af5e79f1cda826d3bf")
    version("1.2.2", sha256="251dd17643cff285f38b020fc4ac9245d8d596f3e2140b98982ffc32eae3943c")
    version("1.2.1", sha256="e7798b82a4c57a75c8cf48607007ab7d46c428d3837644da8004ea2fb37c9bd0")
    version("1.2", sha256="101aa3c3bd943de6597ff3230d2d61ecaff70cbe9a18db3ed7605a26d4140874")
    version("1.1.3", sha256="91e47e9c97bc7765fa4dd65dcca2c9ba8a71d4cfe72ee71ae6f6623a8e476dec")
    version("1.1.2", sha256="361545c9d03a451ee731e778df6dc42c26528130d16be4472c4a0ce164e8448f")
    version("1.1.1", sha256="22fd037f8a6316ae23cddec118b571459064a1fdbab054fe6401713db8803d1c")
    version("1.1", sha256="77533413aa6828aa724a1ef8ac0587c999e41fe36fae4f63cde5c4652ec11fd3")
    version("1.0.4", sha256="70b079c73120821d274f91a56f3a8b15dc6c514f4ac86a89f0612e5e2ac7ca8d")
    version("1.0.3", sha256="a3da591ffd7ccc269bbaef4894b409b09e80ea1bbd678f7fa0f3cf96f48e6b3e")
    version("1.0.2", sha256="9281715436adb7b9eef63fad419a581f397218824bc1271e557c134725c03916")
    version("1.0.1", sha256="8fee2324267811204c1f877a1dea70b23ab3d5f4c3ea0198d81f0921aa70d76e")
    version("1.0", sha256="7bfe11cac1d1f5dc1b60c1258e79d8cc84944d459e3758d50c1f7feba05bc6d7")
    version("0.21.5", sha256="ebb146cadda1c14767251ded54219c8215daee84aa1ac773cf43b5c2ae53160b")
    version("0.21.4", sha256="00ace1ce08cab3408bc83e6b9d55ccba661761e044c03175d58caccedddf93b3")
    version("0.21.3", sha256="a0211aeb5e7dad50b97fa5dffc1a2fe2fe732572d4164e1ee8750a2ede43fbec")
    version("0.21.2", sha256="5897bfd0e321a761de0c57ba1dfe0ebc753cc0d8a18bda2056af48022706a297")
    version("0.21.1", sha256="4cabdb02863a874b2fe58b46489eda5cfefcbe6c63cb615f4d86bf00a6ccfffa")
    version("0.21", sha256="1d97635c8ef40dae3bc46e79769326216d0495a0262ab7cf0ea294ca7924f8e4")
    version("0.20.6", sha256="f1de676fddeb94132c5ae480fb03a64f03deda10b09b3141373f2b2fe5cd031d")
    version("0.20.5", sha256="47af2fa2987836794ad2a48cb289ac053f8c4babc274a8d943944576d00a73d0")
    version("0.20.4", sha256="87947726af741e46314756329ee5a16f18ace17f342ec4489679c09e4ab18bbe")
    version("0.20.3", sha256="0a0b60c8a4c56f50455241ea1cf9be84b3b7d255d76f9fae0143c1bd089fb1f2")
    version("0.20.2", sha256="a70f7877481427df04f26d0dcd9c80bc9844b8e4dded4bfd763b6a4697a57f32")
    version("0.20.1", sha256="a0fe8a9f5358a8e2fb56d0440516c398ed838b2eff2b5bab27606e376c10ca31")
    version("0.20", sha256="99828ff0157b31c0d45b9fd63cfe3fe02c4dc13633b8a1207fffddac56770baa")
    version("0.19", sha256="a7e64e07a5db1c42d72a23bea4acd04fd0c162e27af0b8b8f38ca48b6b5d9999")
    version("0.18.1", sha256="a704e8a2011494a489ec01f42295fea577ea4108ac6159db47ee1ebcca369c26")
    version("0.11", sha256="2d8c1e39107f3fcfa93a5cc8ac8e94b1bbf0a0715b0c99e0d52ed18646346d58")
    version("0.10", sha256="e783d6d085e4dd930a990cf02a76401071f606c6f40e47eae4dc638b54146430")
    version("0.9", sha256="721ab6a14e05f9916645ebb410c3e97fae660d09a1c7df4da7958676504e572b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    default_cpu_runtime = "omp"
    if sys.platform == "darwin":
        default_cpu_runtime = "tbb"

    variant(
        "cpu_runtime",
        default=default_cpu_runtime,
        description="CPU threading runtime to use",
        values=(
            conditional("none", when="@2.3:"),
            "omp",
            "tbb",
            "seq",
            conditional("threadpool", when="@1.4:"),
            conditional("sycl", when="@2:"),
        ),
        multi=False,
    )
    variant(
        "gpu_runtime",
        default="none",
        description="Runtime to use for GPU engines",
        values=("ocl", "none", conditional("sycl", when="@2:")),
        multi=False,
    )
    variant(
        "acl", default=False, description="Use Arm Compute Library", when="@1.7: target=aarch64:"
    )

    # https://github.com/oneapi-src/oneDNN#requirements-for-building-from-source
    depends_on("cmake@2.8.12:", when="@2.3:", type="build")
    depends_on("cmake@2.8.11:", type="build")
    depends_on("tbb@2017:", when="cpu_runtime=tbb")
    depends_on("llvm-openmp", when="%apple-clang cpu_runtime=omp")
    depends_on("opencl@1.2:", when="gpu_runtime=ocl")
    depends_on("armcomputelibrary", when="+acl")
    depends_on("tbb", when="cpu_runtime=sycl")
    depends_on("opencl@1.2:", when="gpu_runtime=sycl")
    depends_on("oneapi-level-zero", when="gpu_runtime=sycl")

    def cmake_args(self):
        args = [
            "-DDNNL_CPU_RUNTIME={0}".format(self.spec.variants["cpu_runtime"].value.upper()),
            "-DDNNL_GPU_RUNTIME={0}".format(self.spec.variants["gpu_runtime"].value.upper()),
        ]

        if self.run_tests:
            args.append("-DDNNL_BUILD_TESTS=ON")
        else:
            args.append("-DDNNL_BUILD_TESTS=OFF")

        # https://github.com/oneapi-src/oneDNN/issues/591
        if self.spec.satisfies("%apple-clang cpu_runtime=omp"):
            args.extend(
                [
                    "-DOpenMP_CXX_FLAGS={0}".format(self.compiler.openmp_flag),
                    "-DOpenMP_C_FLAGS={0}".format(self.compiler.openmp_flag),
                    "-DOpenMP_CXX_LIB_NAMES=libomp",
                    "-DOpenMP_C_LIB_NAMES=libomp",
                    "-DOpenMP_libomp_LIBRARY={0}".format(
                        self.spec["llvm-openmp"].libs.libraries[0]
                    ),
                    "-DCMAKE_SHARED_LINKER_FLAGS={0}".format(
                        self.spec["llvm-openmp"].libs.ld_flags
                    ),
                ]
            )
        elif self.spec.satisfies("cpu_runtime=tbb"):
            args.append("-DTBBROOT=" + self.spec["tbb"].prefix)

        if self.spec.satisfies("gpu_runtime=ocl"):
            args.append("-DOPENCLROOT=" + self.spec["opencl"].prefix)

        args.append(self.define_from_variant("DNNL_AARCH64_USE_ACL", "acl"))

        return args

    def setup_build_environment(self, env):
        if self.spec.satisfies("+acl"):
            env.set("ACL_ROOT_DIR", self.spec["armcomputelibrary"].prefix)
