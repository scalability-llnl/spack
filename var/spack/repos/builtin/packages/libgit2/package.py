# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libgit2(CMakePackage):
    """libgit2 is a portable, pure C implementation of the Git core
    methods provided as a re-entrant linkable library with a solid
    API, allowing you to write native speed custom Git applications in
    any language which supports C bindings.
    """

    homepage = "https://libgit2.github.com/"
    url = "https://github.com/libgit2/libgit2/archive/v0.26.0.tar.gz"

    version("1.8.0", sha256="9e1d6a880d59026b675456fbb1593c724c68d73c34c0d214d6eb848e9bbd8ae4")
    version("1.7.2", sha256="de384e29d7efc9330c6cdb126ebf88342b5025d920dcb7c645defad85195ea7f")
    version("1.7.0", sha256="d9d0f84a86bf98b73e68997f5c1543cc5067d0ca9c7a5acaba3e8d117ecefef3")
    version("1.6.4", sha256="d25866a4ee275a64f65be2d9a663680a5cf1ed87b7ee4c534997562c828e500d")
    version("1.6.3", sha256="a8e2a09835eabb24ace2fd597a78af182e1e199a894e99a90e4c87c849fcd9c4")
    version("1.6.2", sha256="d557fbf35557bb5df53cbf38ae0081edb4a36494ec0d19741fa673e509245f8f")
    version("1.6.1", sha256="25f7d3e2e7f398477a6e18271c5a68510853d0fe826a6287811cebccf92e773f")
    version("1.5.2", sha256="57638ac0e319078f56a7e17570be754515e5b1276d3750904b4214c92e8fa196")
    version("1.5.1", sha256="7074f1e2697992b82402501182db254fe62d64877b12f6e4c64656516f4cde88")
    version("1.5.0", sha256="8de872a0f201b33d9522b817c92e14edb4efad18dae95cf156cf240b2efff93e")
    version("1.4.4", sha256="e9923e9916a32f54c661d55d79c28fa304cb23617639e68bff9f94d3e18f2d4b")
    version("1.4.3", sha256="f48b961e463a9e4e7e7e58b21a0fb5a9b2a1d24d9ba4d15870a0c9b8ad965163")
    version("1.4.2", sha256="901c2b4492976b86477569502a41c31b274b69adc177149c02099ea88404ef19")
    version("1.4.1", sha256="fccd371a271133e29d002dd207490d22a0c9b06992b874b8edb8366532a94f54")
    version("1.4.0", sha256="9051e75964350054d5e3f9339bc4d1fb56ac14949710e3860f98f07a0433fa25")
    version("1.3.1", sha256="a2a0a90d577f1771ba9f7e98042865c3f6386c896eeefa846c3fc0c37ce7c6e0")
    version("1.3.0", sha256="192eeff84596ff09efb6b01835a066f2df7cd7985e0991c79595688e6b36444e")
    version("1.2.0", sha256="701a5086a968a46f25e631941b99fc23e4755ca2c56f59371ce1d94b9a0cc643")
    version("1.1.1", sha256="13a525373f64c711a00a058514d890d1512080265f98e0935ab279393f21a620")
    version("1.1.0", sha256="41a6d5d740fd608674c7db8685685f45535323e73e784062cf000a633d420d1e")
    version("1.0.1", sha256="1775427a6098f441ddbaa5bd4e9b8a043c7401e450ed761e69a415530fea81d2")
    version("1.0.0", sha256="6a1fa16a7f6335ce8b2630fbdbb5e57c4027929ebc56fcd1ac55edb141b409b4")
    version("0.99.0", sha256="174024310c1563097a6613a0d3f7539d11a9a86517cd67ce533849065de08a11")
    version("0.28.5", sha256="2b7b68aee6f123bc84cc502a9c12738435b8054e7d628962e091cd2a25be4f42")
    version("0.28.4", sha256="30f3877469d09f2e4a21be933b4e2800560d16646028dd800744dc5f7fb0c749")
    version("0.28.3", sha256="ee5344730fe11ce7c86646e19c2d257757be293f5a567548d398fb3af8b8e53b")
    version("0.28.2", sha256="42b5f1e9b9159d66d86fff0394215c5733b6ef8f9b9d054cdd8c73ad47177fc3")
    version("0.28.1", sha256="0ca11048795b0d6338f2e57717370208c2c97ad66c6d5eac0c97a8827d13936b")
    version("0.28.0", sha256="9d60d64dc77085e8e530e5c66314057eafe0c06e4a7a61149a70ff3e0688f284")
    version("0.27.10", sha256="f6fd26378ff71bd7a4b17b576c82c774a2e9c2d6b74b24718a8fb29551e1c4a5")
    version("0.27.9", sha256="adf17310b590e6e7618f070c742b5ee028aeeed2c60099bc4190c386b5060de1")
    version("0.27.8", sha256="8313873d49dc01e8b880ec334d7430ae67496a89aaa8c6e7bbd3affb47a00c76")
    version("0.27.7", sha256="1a5435a483759b1cd96feb12b11abb5231b0688016db506ce5947178f6ba2531")
    version("0.27.6", sha256="d98db2ed11ec82fee94dce4819b466524613852c2c9c3426d351c57729ec49da")
    version("0.27.5", sha256="15f2775f4f325951d9139ed906502b6c71fee6787cada9b045f5994072ccbd33")
    version("0.27.4", sha256="0b7ca31cb959ff1b22afa0da8621782afe61f99242bf716c403802ffbdb21d51")
    version("0.27.3", sha256="50a57bd91f57aa310fb7d5e2a340b3779dc17e67b4e7e66111feac5c2432f1a5")
    version("0.27.2", sha256="ffacdbd5588aeb03e98e3866a7e2ceace468723a439bdc9bb01362fe140fa9e5")
    version("0.27.1", sha256="837b11927bc5f64e7f9ab0376f57cfe3ca5aa52ffd2007ac41184b21124fb086")
    version("0.27.0", sha256="545b0458292c786aba334f1bf1c8f73600ae73dd7205a7bb791a187ee48ab8d2")
    version("0.26.8", sha256="0f20d7e239be030db33d7350bab38ada2830b3bffab5539730074e71b0267796")
    version("0.26.7", sha256="65584ac1f4de2c3ab8491351c8629eb68bad2d65e67f6411bf0333b8976dc4ef")
    version("0.26.6", sha256="7669dd47ebdab86ced8888816c552596ec923b6e126704a3445b2081cb0e5662")
    version("0.26.5", sha256="52e28a5166564bc4365a2e4112f5e5c6e334708dbf13596241b2fd34efc1b0a9")
    version("0.26.4", sha256="292fa2600bbb4e52641793cfcc1c19ffc0bf97b5fd8378d422a6bfe7afffcb97")
    version("0.26.3", sha256="0da4e211dfb63c22e5f43f2a4a5373e86a140afa88a25ca6ba3cc2cae58263d2")
    version("0.26.2", sha256="747b47d5b02a2387ff81301c694763785181b895690b6eb91ed1ae4b7904307b")
    version("0.26.1", sha256="68cd0f8ee9e0ca84dcf0f0267d0a8297471d3365622d22d3da67c57165bb0722")
    version("0.26.0", sha256="6a62393e0ceb37d02fe0d5707713f504e7acac9006ef33da1e88960bd78b6eac")

    depends_on("c", type="build")  # generated

    # Backends
    variant(
        "https",
        default="system",
        description="HTTPS support",
        values=("system", "openssl", "none"),
        multi=False,
    )
    variant("ssh", default=True, description="Enable SSH support")
    variant(
        "curl", default=False, description="Enable libcurl support (only supported through v0.27)"
    )

    variant("mmap", default=True, description="Enable mmap support", when="@1.1.1:")

    # Build Dependencies
    depends_on("cmake@2.8:", type="build", when="@:0.28")
    depends_on("cmake@3.5:", type="build", when="@0.99:")
    depends_on("pkgconfig", type="build")
    depends_on("python", type="test")

    # Runtime Dependencies
    depends_on("libssh2", when="+ssh")
    depends_on("openssl", when="https=system platform=linux")
    depends_on("openssl", when="https=openssl")
    depends_on("curl", when="+curl")
    depends_on("pcre", when="@0.99:")

    conflicts("+curl", when="@0.28:")

    def flag_handler(self, name, flags):
        if name == "cflags" and not self.spec.variants.get("mmap", False):
            flags.append("-DNO_MMAP")
        return (flags, None, None)

    def cmake_args(self):
        args = []
        if self.spec.satisfies("https=system"):
            if self.spec.satisfies("platform=linux"):
                args.append("-DUSE_HTTPS=OpenSSL")
            elif self.spec.satisfies("platform=darwin"):
                args.append("-DUSE_HTTPS=SecureTransport")
            else:
                # Let CMake try to find an HTTPS implementation. Mileage on
                # your platform may vary
                args.append("-DUSE_HTTPS=ON")
        elif self.spec.satisfies("https=openssl"):
            args.append("-DUSE_HTTPS=OpenSSL")
        else:
            args.append("-DUSE_HTTPS=OFF")

        args.append(f"-DUSE_SSH={'ON' if '+ssh' in self.spec else 'OFF'}")

        # The curl backed is not supported after 0.27.x
        if self.spec.satisfies("@:0.27 +curl"):
            args.append(f"-DCURL={'ON' if '+curl' in self.spec else 'OFF'}")

        # Control tests
        args.append(self.define("BUILD_CLAR", self.run_tests))
        args.append(self.define("BUILD_TESTS", self.run_tests))

        return args
