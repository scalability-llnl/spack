# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nco(AutotoolsPackage):
    """The NCO toolkit manipulates and analyzes data stored in
    netCDF-accessible formats"""

    homepage = "https://nco.sourceforge.net/"
    url = "https://github.com/nco/nco/archive/5.0.1.tar.gz"

    maintainers("altheaden", "xylar")

    license("BSD-3-Clause")

    version("5.3.2", sha256="645179433e0f54e7e6fefa9fcc74c1866ad55dd69f0fccbc262c550fcc186385")
    version("5.3.1", sha256="c527e991e1befcc839a14151a2982a20340ab1523ce98b66ef3efa2878ee039b")
    version("5.3.0", sha256="661d12f4eb678ca301bf6000f1c1d0fb0e32a69def237dc14f3253e9fc1aaf6a")
    version("5.2.9", sha256="6245886e2a18a4821b0fb768cf9906de09aeb47c303462c8e85f0d1a4f34956d")
    version("5.2.8", sha256="802676c8c22081e6eeed79b73ebe4cd6cac2edad49a712e17880b184d96daeeb")
    version("5.2.7", sha256="fb463905b9c451cf9bd5a9c2259cdff054224cea3ef449145495cdeb966f06af")
    version("5.2.6", sha256="31245c56c031eee14e32d77b56fcc291785e407ed9534a62c2f1f8320eb317af")
    # skipping 5.2.5, see https://github.com/nco/nco/releases/tag/5.2.6
    version("5.2.4", sha256="44efa9151825487fa0562fa5c6d68837624059a8e2da9d15c83ceb4d498f7902")
    version("5.2.3", sha256="178ad32448067c72dc82b71ffc8b39add1252637cf6f9e23982ba1484920ca44")
    version("5.2.2", sha256="3908ce21dc7fd3be5f7fa4fe72bd96b69e6608bd246e6c1a504879ed6c7acfda")
    version("5.2.1", sha256="d3975f9e3ee659ed53690a887be8e950c90fc1faed71f2969896427907557ac3")
    # skipping 5.2.0 because of bugs
    version("5.1.9", sha256="9cd90345c1e3860a690b53fd6c08b721d631a646d169431927884c99841c34e9")
    version("5.1.8", sha256="f22c63a3cbe1947fbf06160a6ed7b6d1934aa242fbe3feeb8d1964eef266b7d5")
    version("5.1.7", sha256="2b068558a605e30a465870166747e1d37726849814a5cfe41a000764b30e2ba1")
    version("5.1.6", sha256="6b217156cb14f670c80d5de5c5b88905cdb281f6e239e83397f14eaf3d0b390b")
    version("5.1.5", sha256="6a35c2d45744b427a424896d32066e483c0a49a46dba83ba90f2cc5ed3dca869")
    version("5.1.4", sha256="4b1ec67b795b985990620be7b7422ecae6da77f5ec93e4407b799f0220dffc88")
    version("5.1.3", sha256="f6766627dab3f067c88f2cd713e3058c324ea4f900fabf9755bdd8918c32de7b")
    version("5.1.2", sha256="1b86303fc55b5a52b52923285a5e709de82cbc1630e68b64dce434b681e4100a")
    version("5.1.1", sha256="6e004cfaa8e3188f543d2a31f7fdd7b2d2a59b6c7fea44c41ad13232bbe1c8d6")
    version("5.1.0", sha256="6f0ba812e0684881a85ebf3385117761cffbba36ba842889cc96f111157f89c2")
    version("5.0.7", sha256="6ddb397e7de4a7876e7d84ea82d4ee716cfd60ad8ee50ef49716945c505cbc1d")
    version("5.0.6", sha256="d4c74e0268af94bdddcb0c77189830992f61c04147c23669b66470f1a8595d60")
    version("5.0.5", sha256="765af0e3194c364504251c19d3362038730752fc5e741078ecdd875de45dbc55")
    version("5.0.4", sha256="91c9d191db8c7132489d86727b195c04577f034adf168f9d341ec63b55ea4353")
    version("5.0.3", sha256="61b45cdfbb772718f00d40da1a4ce268201fd00a61ebb9515460b8dda8557bdb")
    version("5.0.2", sha256="7486e7e03da4caf2736e8eb3d2299a686fb58dbcc04391ce073e0a8c2baf80d6")
    version("5.0.1", sha256="37d11ffe582aa0ee89f77a7b9a176b41e41900e9ab709e780ec0caf52ad60c4b")
    version("4.9.3", sha256="eade5b79f3814b11ae3f52c34159567e76a73f05f0ab141eccaac68f0ca94aee")
    version("4.9.2", sha256="1a98c37c946c00232fa7319d00d1d80f77603adda7c9239d10d68a8a3545a4d5")
    version("4.9.1", sha256="9592efaf0dfd6ccdefd0b417d990cfccae7e89c20d90fb44ead6263009778834")
    version("4.9.0", sha256="21dd53f427793cbc52d1c007e9b7339c83f6944a937a1acfbbe733e49b65378b")
    version("4.8.1", sha256="ddae3fed46c266798ed1176d6a70b36376d2d320fa933c716a623172d1e13c68")
    version("4.8.0", sha256="91f95ebfc9baa888adaec3016ca18a6297e2881b1429d74543a27fdfbe15fcab")
    version("4.7.9", sha256="048f6298bceb40913c3ae433f875dea1e9129b1c86019128e7271d08f274a879")
    version("4.6.7", sha256="2fe2dabf14a60bface694307cbe719df57103682b715348e9d77bfe8d31487f3")
    version("4.6.6", sha256="079d83f800b73d9b12b8de1634a88c2cbe40a639aaf7bc056cd2e836c6047697")
    version("4.6.5", sha256="d5b18c9ada25d062a539e2995be445db39e8021c56cd4b20c88485cb2452c7ae")
    version("4.6.4", sha256="1c2ab906fc81f91bf8aff3e6da27ae7a4c89821c5836d787188fff5262418062")
    version("4.6.3", sha256="414ccb349ed25cb37b669fb87f9e2e4ca8d58c2f45538feda199bf895b982bf8")
    version("4.6.2", sha256="cec82e35d47a6bbf8ab9301d5ff4cf08051f489b49e8529ebf780380f2c21ed3")
    version("4.6.1", sha256="7433fe5901f48eb5170f24c6d53b484161e1c63884d9350600070573baf8b8b0")
    version("4.5.5", sha256="bc6f5b976fdfbdec51f2ebefa158fa54672442c2fd5f042ba884f9f32c2ad666")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # https://github.com/nco/nco/issues/43
    patch("NUL-0-NULL.patch", when="@:4.6.7")

    variant("doc", default=False, description="Build/install NCO TexInfo-based documentation")
    variant("openmp", default=True, description="Include OpenMP support")

    # See "Compilation Requirements" at:
    # http://nco.sourceforge.net/#bld
    depends_on("netcdf-c")
    depends_on("antlr@2.7.7+cxx")  # required for ncap2
    depends_on("gsl")  # desirable for ncap2
    depends_on("udunits")  # allows dimensional unit transformations

    depends_on("flex", type="build")
    depends_on("bison", type="build")
    depends_on("texinfo@4.12:", type="build", when="+doc")

    conflicts("%gcc@9:", when="@:4.7.8")

    def configure_args(self):
        config_args = self.enable_or_disable("doc")
        config_args += self.enable_or_disable("openmp")
        return config_args

    def setup_build_environment(self, env):
        spec = self.spec
        env.set("NETCDF_INC", spec["netcdf-c"].prefix.include)
        env.set("NETCDF_LIB", spec["netcdf-c"].prefix.lib)
        env.set("ANTLR_ROOT", spec["antlr"].prefix)
        env.set("UDUNITS2_PATH", spec["udunits"].prefix)
