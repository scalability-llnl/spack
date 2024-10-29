# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vecmem(CMakePackage, CudaPackage):
    """VecMem is a vectorised data model base and helper classes."""

    homepage = "https://github.com/acts-project/vecmem"
    url = "https://github.com/acts-project/vecmem/archive/refs/tags/v0.5.0.tar.gz"
    list_url = "https://github.com/acts-project/vecmem/tags"

    maintainers("wdconinc", "stephenswat")

    license("MPL-2.0-no-copyleft-exception")

    version("1.10.0", sha256="1fbdc599a65ad7b2cd1176844c7578da38911bc747fbe51a71e00d20e6105330")
    version("1.9.0", sha256="c1ddc43ff0d742306cbee71afd80efd348b6b0b1ba9e4210ca7f8b607f03bd70")
    version("1.8.0", sha256="d04f1bfcd08837f85c794a69da9f248e163985214a302c22381037feb5b3a7a9")
    version("1.7.0", sha256="ff4bf8ea86a5edcb4a1e3d8dd0c42c73c60e998c6fb6512a40182c1f4620a73d")
    version("1.6.0", sha256="797b016ac0b79bb39abad059ffa9f4817e519218429c9ab4c115f989616bd5d4")
    version("1.5.0", sha256="5d7a2d2dd8eb961af12a1ed9e4e427b89881e843064ffa96ad0cf0934ba9b7ae")
    version("1.4.0", sha256="545dfb4de4f9f3d773eef6a0e3297ebf981bb81950930d0991ad739e31ab16af")
    version("1.3.1", sha256="09b108b0b48d564bbc1b9893ad9c3f7fa0b7914179f55be4c81f88a93e25f2e2")
    version("1.3.0", sha256="53367db3084de56891ff885754c8fc2427d9ae69a351dd4d984558edf4162bad")
    version("1.2.0", sha256="2cca8c1143803f209b58e49e9f2d58ebeeec4c815e7d99b0da9f61a319274aa9")
    version("1.1.0", sha256="4d1f08a28268708819b68ed547eac912ec46e6707b059f0cc4aa7103a525164e")
    version("1.0.0", sha256="59f478e036aed384eed1ecee1a99c5c52983534d3007d9f9203b7cb12c6ffa19")
    version("0.27.0", sha256="f50a32214500767402930d4650243583769684c28fa29fe17f17f393a37ce0f2")
    version("0.26.0", sha256="0e67acc197c4c1052288957c6419478c243aca718b64d383decd758d3c8f49ee")
    version("0.25.0", sha256="90a87f00d45216cf4548fbcd6bb255dc15190873dc52936293a8c13f82e907f3")
    version("0.24.0", sha256="b395c013fba4e01f02939fefac14b357dbfd8e572b5c8f4ee5a1414adbd2ea93")
    version("0.22.0", sha256="b8811723bee60b0ea289d4c8b73363883e7c856859baf4cb6276b38816b0b258")
    version("0.21.0", sha256="97df3beb9a59b89b65c51ceb7e7c9b09172b3875b25f2d8fc070e4f9b061b631")
    version("0.20.0", sha256="1361aa180255d38a15b9d674cbb9411f8565c660f918a536479a21f3856b1fd8")
    version("0.19.0", sha256="9c56d17dbb122fa8b81e392f6c00b132ca07b8f0107e25a6fff798295b58a193")
    version("0.18.0", sha256="5cba44e8a8baadf224ee377206dfb91ebc66fb5c299baf00e1638ba47a28f2a2")
    version("0.17.0", sha256="5b85b5891b16efe1e53081fec002607c154e0faeb6974616102f5c6354cc3617")
    version("0.16.0", sha256="5e76c519fba0ae7f1cdac40bd9e85dcc843e5d8a28550eafe21eee3f493d24e3")
    version("0.15.0", sha256="acb8170e0c5454fd06bea2fb1e3ae97a5dbf55d1d6f470f2550ab0e2dd98c9fb")
    version("0.14.0", sha256="e6f396818e72a18ca6c277b3feec0af7794b020ba880c35a3372162e2c3a2b9a")
    version("0.13.0", sha256="084f279d88ff15951c3653a21c45f94c671902c86dfad88bcf257f604dfdbe9b")
    version("0.12.0", sha256="aab017e5df5f4251c53313aecf63f550c43890ec4845f138e3d46aa4113b8609")
    version("0.11.0", sha256="4bed7f2cdcad376ee3e2f744aba95497c837b6a9807a069245f66e02c78b745a")
    version("0.10.0", sha256="b872835dde943ec5ef88799db7846b3bdac5f36d1254f74116ec4e4615e35bb1")
    version("0.9.0", sha256="4c742f4b85ab470e2401f00bde67e36319ae83ab2a89261eb24836e27bd3f542")
    version("0.8.0", sha256="a13f7178c940d6bf3386e7e8f5eb158e6435882533bffe888d3c9775eeb2f20e")
    version("0.7.0", sha256="c00266bc80df8f568103f2874ce349fe8f74fb7e361901d562cce41ab7f9b85c")
    version("0.6.0", sha256="e6c8262844a5ff7f03df7f849a1e7cf1a68214730ac54c35c14333522ff31723")
    version("0.5.0", sha256="b9739e8fcdf27fa9ef509743cd8f8f62f871b53b0a63b93f24ea9865c2b00a3a")
    version("0.4.0", sha256="51dfadc2b97f34530c642abdf86dcb6392e753dd68ef011bac89382dcf8aaad4")
    version("0.3.0", sha256="4e7851ab46fee925800405c5ae18e99b62644d624d3544277a522a06fb812dbf")
    version("0.2.0", sha256="33aea135989684e325cb097e455ff0f9d1a9e85ff32f671e3b3ed6cc036176ac")
    version("0.1.0", sha256="19e24e3262aa113cd4242e7b94e2de34a4b362e78553730a358f64351c6a0a01")

    depends_on("cxx", type="build")  # generated

    variant("hip", default=False, description="Build the vecmem::hip library")
    variant("sycl", default=False, description="Build the vecmem::sycl library")

    depends_on("cmake@3.17:", type="build")
    depends_on("hip", when="+hip")
    depends_on("sycl", when="+sycl")

    # FIXME: due to #29447, googletest is not available to cmake when building with --test,
    # and we can choose between always depending on googletest, or using FetchContent
    # depends_on("googletest", type="test")

    def setup_build_environment(self, env):
        if self.spec.satisfies("+sycl"):
            env.set("SYCLCXX", self.compiler.cxx)
            if self.spec.satisfies("%oneapi"):
                env.set("SYCLFLAGS", "-fsycl")

    def cmake_args(self):
        args = [
            self.define("FETCHCONTENT_FULLY_DISCONNECTED", False),  # see FIXME above
            self.define_from_variant("VECMEM_BUILD_CUDA_LIBRARY", "cuda"),
            self.define_from_variant("VECMEM_BUILD_HIP_LIBRARY", "hip"),
            self.define_from_variant("VECMEM_BUILD_SYCL_LIBRARY", "sycl"),
            self.define("BUILD_TESTING", self.run_tests),
            self.define("VECMEM_BUILD_TESTING", self.run_tests),
            self.define("VECMEM_USE_SYSTEM_LIBS", True),
            self.define("VECMEM_USE_SYSTEM_GOOGLETEST", False),  # see FIXME above
        ]

        if "+cuda" in self.spec:
            cuda_arch_list = self.spec.variants["cuda_arch"].value
            cuda_arch = cuda_arch_list[0]
            if cuda_arch != "none":
                args.append("-DCUDA_FLAGS=-arch=sm_{0}".format(cuda_arch))

        return args
