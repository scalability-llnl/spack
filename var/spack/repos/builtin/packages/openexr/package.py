# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.cmake import CMakeBuilder
from spack.package import *


class Openexr(CMakePackage, AutotoolsPackage):
    """OpenEXR Graphics Tools (high dynamic-range image file format)"""

    homepage = "https://www.openexr.com/"
    url = "https://github.com/AcademySoftwareFoundation/openexr/archive/refs/tags/v3.1.5.tar.gz"

    license("BSD-3-Clause")

    # New versions should come from github now
    version("3.3.1", sha256="58aad2b32c047070a52f1205b309bdae007442e0f983120e4ff57551eb6f10f1")
    version("3.2.3", sha256="f3f6c4165694d5c09e478a791eae69847cadb1333a2948ca222aa09f145eba63")
    version("3.2.0", sha256="b1b200606640547fceff0d3ebe01ac05c4a7ae2a131be7e9b3e5b9f491ef35b3")
    version("3.1.11", sha256="06b4a20d0791b5ec0f804c855d320a0615ce8445124f293616a086e093f1f1e1")
    version("3.1.7", sha256="78dbca39115a1c526e6728588753955ee75fa7f5bb1a6e238bed5b6d66f91fd7")
    version("3.1.5", sha256="93925805c1fc4f8162b35f0ae109c4a75344e6decae5a240afdfce25f8a433ec")
    version("2.5.9", sha256="05bb9c2da3ff3508eee51c30f59c7f2c59bf068f3b636d12d5991e8bbaf13e01")
    version("2.4.2", sha256="8e5bfd89f4ae1221f84216a163003edddf0d37b8aac4ee42b46edb55544599b9")
    version(
        "2.3.0",
        sha256="fd6cb3a87f8c1a233be17b94c74799e6241d50fc5efd4df75c7a4b9cf4e25ea6",
        url="https://github.com/AcademySoftwareFoundation/openexr/releases/download/v2.3.0/openexr-2.3.0.tar.gz",
    )

    version(
        "2.2.0",
        sha256="36a012f6c43213f840ce29a8b182700f6cf6b214bea0d5735594136b44914231",
        url="http://download.savannah.nongnu.org/releases/openexr/openexr-2.2.0.tar.gz",
    )
    version(
        "2.1.0",
        sha256="54486b454073c1dcb5ae9892cf0f730ffefe62f38176325281505093fd218a14",
        url="http://download.savannah.nongnu.org/releases/openexr/openexr-2.1.0.tar.gz",
    )
    version(
        "2.0.1",
        sha256="b9924d2f9d57376ff99234209231ad97a47f5cfebd18a5d0570db6d1a220685a",
        url="http://download.savannah.nongnu.org/releases/openexr/openexr-2.0.1.tar.gz",
    )
    version(
        "1.7.0",
        sha256="b68a2164d01bd028d15bd96af2704634a344e291dc7cc2019a662045d8c52ca4",
        url="http://download.savannah.nongnu.org/releases/openexr/openexr-1.7.0.tar.gz",
    )
    version(
        "1.6.1",
        sha256="c616906ab958de9c37bb86ca7547cfedbdfbad5e1ca2a4ab98983c9afa6a5950",
        url="http://download.savannah.nongnu.org/releases/openexr/openexr-1.6.1.tar.gz",
    )
    version(
        "1.5.0",
        sha256="5a745eee4b8ab94cd16f85528c2debfebe6aa1ba23f5b8fc7933d4aa5c3c3416",
        url="http://download.savannah.nongnu.org/releases/openexr/openexr-1.5.0.tar.gz",
    )
    version(
        "1.4.0a",
        sha256="5d8a7327bd28eeb5d3064640d8eb32c3cd8c5a15999c70b0afa9f8af851936d1",
        url="http://download.savannah.nongnu.org/releases/openexr/openexr-1.4.0a.tar.gz",
    )
    version(
        "1.3.2",
        sha256="fa08ad904bf89e2968078d25d1d9817f5bc17f372d1bafabf82e8f08ca2adc20",
        url="http://download.savannah.nongnu.org/releases/openexr/openexr-1.3.2.tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("imath", when="@3:")
    depends_on("ilmbase", when="@:2")
    depends_on("zlib-api")
    depends_on("libdeflate", when="@3.2:")

    conflicts("@:2.5.8 %gcc@13:")

    # Build system
    build_system(
        conditional("cmake", when="@2.4:"), conditional("autotools", when="@:2.3"), default="cmake"
    )

    with when("build_system=cmake"):
        depends_on("cmake@3.12:", type="build")
        depends_on("cmake@3.14:", type="build", when="@3.3:")

    @property
    def libs(self):
        # Override because libs have different case than Spack package name
        name = "libOpenEXR*"
        # We expect libraries to be in either lib64 or lib directory
        for root in (self.prefix.lib64, self.prefix.lib):
            liblist = find_libraries(name, root=root, shared=True, recursive=False)
            if liblist:
                break
        return liblist


class CMakeBuilder(CMakeBuilder):
    def cmake_args(self):
        args = [self.define("BUILD_TESTING", self.pkg.run_tests)]
        return args
