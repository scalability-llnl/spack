# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Qemu(AutotoolsPackage):
    """QEMU is a generic and open source machine emulator and virtualizer."""

    homepage = "https://www.qemu.org"
    url = "https://download.qemu.org/qemu-4.1.1.tar.xz"

    maintainers("anderbubble")

    # Docs say TCG is "under a BSD license" but all the headers for TCG have the MIT license.
    license("GPL-2.0-only AND LGPL-2.1-only AND MIT", checked_by="tgamblin")

    version("9.1.0", sha256="816b7022a8ba7c2ac30e2e0cf973e826f6bcc8505339603212c5ede8e94d7834")
    version("4.1.1", sha256="ed6fdbbdd272611446ff8036991e9b9f04a2ab2e3ffa9e79f3bab0eb9a95a1d2")
    version("4.1.0", sha256="656e60218689bdeec69903087fd7582d5d3e72238d02f4481d8dc6d79fd909c6")
    version("4.0.1", sha256="f2674dd6053ef1d48593aa1f0a50c5ac9039f7a059ecb6f9b8307f3fb2fcedad")
    version("4.0.0", sha256="13a93dfe75b86734326f8d5b475fde82ec692d5b5a338b4262aeeb6b0fa4e469")
    version("3.1.1.1", sha256="b148fc3c7382c5addd915db433383160ca7b840bc6ea90bb0d35c6b253526d56")
    version("3.1.1", sha256="d7c69fef3fb4bfbac99e3f2ac9fb8d6409db4faadf2e37337d544e3fdb4fde3a")
    version("3.1.0", sha256="6a0508df079a0a33c2487ca936a56c12122f105b8a96a44374704bef6c69abfc")
    version("3.0.1", sha256="cf5747aa3bf0e7ec6cb166f48be4680097c333ce320e8e58140980b0d99512f3")
    version("3.0.0", sha256="8d7af64fe8bd5ea5c3bdf17131a8b858491bcce1ee3839425a6d91fb821b5713")
    version("2.12.1", sha256="33583800e0006cd00b78226b85be5a27c8e3b156bed2e60e83ecbeb7b9b8364f")
    version("2.12.0", sha256="e69301f361ff65bf5dabd8a19196aeaa5613c1b5ae1678f0823bdf50e7d5c6fc")
    version("2.11.2", sha256="02d2b2cf5526b642b174596d9b3a8716184f9e79710bc68bf6d9fec175b3821b")
    version("2.11.1", sha256="8a5145d1f8bd2eadc6776f3e13c68cd28d01349e30639bdbcb26ac588d668686")
    version("2.11.0", sha256="c9d34a79024eae080ce3853aa9afe503824520eefb440190383003081ce7f437")
    version("2.10.2", sha256="fcfdaa1ecdaac8aead616fe811bfb8fe4a8f2cd59796aa446c5175b5af0e829f")
    version("2.10.1", sha256="1dd51a908fc68c7d935b0b31fb184c5669bc23b5a1b081816e824714f2a11caa")
    version("2.10.0", sha256="55d81ac987a4821d2744359c026d766459319ba9c013746570369068d93ff335")
    version("2.9.1", sha256="4350b3d1d75f1e6a562d975687e181f61ceaf3ac94e6b629f87e24cbe680d03d")
    version("2.9.0", sha256="f01cc33e3c5fd5fd2534ce14e369b6b111d7e54e4a4977f8c37eae668176b022")
    version("2.8.1.1", sha256="7b50634d729dcabe4a96d74062832274fa2f4c883e82904f5e6955f801edab54")
    version("2.8.1", sha256="4d4d2f62c0f7977fb1d49ba4894b2d5e43b8bf8a442be77d42701262c9166440")
    version("2.8.0", sha256="656c3d408e367de7eca85ea488228d5bb7c68f4a6dc0b1966b529524bd6b938c")
    version("2.7.1", sha256="7fd448219b43bb61f8b5eb37e465298d503abc84156c9dd6e73c9dc6902a2831")
    version("2.7.0", sha256="ea5186cffe3ea5e7e903a3f96905aa5596bde2cda445b1ce4fa00024da6c1371")
    version("2.6.2", sha256="bd4b00c47d47ac45518bce2e9bc1a7d24f2df102dcdeedecca699cdbdde2ff2b")
    version("2.6.1", sha256="b7e17b0c8a92c99317b984ed5aad85603c475e58f8fe70d75aef1936d22822f0")
    version("2.6.0", sha256="d0ddb3e80686003feb7e37dae9531237544ee94f91f36b3c49e87ae11e84393c")
    version("2.5.1.1", sha256="29b00bfa8933831122eb43521ff02b462ae4e5bcef77de6309015cbb19d3743f")
    version("2.5.1", sha256="bd630bb8dffb3d8579bc9c88534debc941215f346801d78fcae9a71becec84b0")
    version("2.5.0", sha256="0b2de3ec698135c20d73c4e67f854590e5eadebcc8bfa8484fe59643370ce002")
    version("2.4.1", sha256="b5049109656c98558584cfe0125d7994d8eba987f6f92dca289f44efcd0bb231")
    version("2.4.0.1", sha256="7ffebc51f7ff61324524eef7a7ec47596c4e53b3d45ba76141b32884dd7f8cbc")
    version("2.4.0", sha256="38be58b62b52115e902439c98c61f3bd4773c0113b62f5b153533fc0fae3f485")
    version("2.3.1", sha256="da78995a818146e4ded948cd7590a75b9e5b042f8be28a79bfae1f669819075c")
    version("2.3.0", sha256="8cea969890681a4069b1beaa82b89728991f1ca701a0184af50210305078bf5f")
    version("2.2.1", sha256="1d8f976255db2d3d280ab0d31a11ea5c39da5ddfdec157475b6c335d017ed978")
    version("2.2.0", sha256="ffd9a4bf2df9cd8607924690caae1c6ed79681412449e3679b1308dbc1d64b9a")
    version("2.1.3", sha256="26231047738ba53e3eef6caafa97dae6194307b9b34040436292446f12853c10")
    version("2.1.2", sha256="4d710187d189f42130c3b0a83d091ed6f97fa6ad152d0e87d48fbb5cc73f661a")
    version("2.1.1", sha256="ed40d0616f6c10d0f70d67c5672383aa2b426e22565e48a85aa135ab95b97e98")
    version("2.1.0", sha256="ece4d8e9b99ba1671ab3a6ed67ab1f65f85912a8b6318a1350b36088408887f5")
    version("2.0.2", sha256="1a7a4479796474ebfc2991ea3eeb62a3dd7375cc427089bb474d6c13dd732307")
    version("2.0.0", sha256="8b4a6243e0cec451438f1d5283b3097700298728c046e3fb80814c0b45cb649d")
    version("1.7.2", sha256="8897908a564a8be8adaaca5f963285b602de3bec57b187e8575a3808ead350fe")
    version("1.7.0", sha256="d9338f59ca570d55e4611f133a1c474620b629067afcd3fba0914e0a2c098dae")
    version("1.6.2", sha256="e7bf52efb9842386c3c4e47a48f39327ba3ece12e203c169f2faf4bd2a0c0961")
    version("1.6.1", sha256="9d7805e9486116704b546411641a77ed25d306c586036fc3933a7740e190d3b1")
    version("1.6.0", sha256="491678c5a94c85c287e3525f1496168fcba6d30752d17ccad91f648bb72f06cf")
    version("1.5.3", sha256="bab87866283a49cd7b5f8bf9c136e24715c741f4ec0605742736a958f178cec0")
    version("1.5.2", sha256="a0322e5f3004d4c383b075c9c583be39098df35dcf33caa9ba2f2847dd8b99c6")
    version("1.5.1", sha256="1286c204c7f50559e61e7ee22842925da30fbbf9ec28d3109d1b195442ebc17d")
    version("1.5.0", sha256="04177f655efde974c24b3c2fee22f3138768905b94aa1597fa70868a727396af")
    version("1.4.2", sha256="1ac21bd817495599e6db700086c7b1422746a3d30bf531e5e4dcf555ed7e44ad")
    version("1.4.1", sha256="62c8240f1c6d72c6c134d8fd466821391c33729cdb82569f3a55e0aa05d18f98")
    version("1.4.0", sha256="82d31db238216a53348293ebf06ef00673301a73e0b5d25a4be3c7f8b9ba6f6d")
    version("1.3.1", sha256="eb098fcd46676071ac1eec49d558a8cf15a73f344e880f6f033620e94ec46af3")
    version("1.3.0", sha256="425d220e6ddcf043486343bf4ae0953b53e5c715bd9ed4d1705becc409661b59")
    version("1.2.2", sha256="d81f1d52c08a6fd842c519c0f50ab9b1d0d0f469922402f4552b5515644f9e00")
    version("1.2.1", sha256="7ccee3c0d67cf506d85ab1bb80b8bc6734fff7f610c34745798e3945d68a53fc")
    version("1.2.0", sha256="ba1fc4cc582d3e6f267a72d864c4c8d2f7ee53b160ef338ae4e64e041e6b6c11")
    version("1.1.2", sha256="715aba5e05d48a3af69f704840e8a478a0474d0fb75d846e197dac8942c29ad4")
    version("1.1.1", sha256="e28722fd676fed34cfdc07581fd2547a766a1785c71f391ed1f2f4f4e923df64")
    version("1.1.0-1", sha256="3a58fbaef1715ac3fa40e534d499873b66039b6adb409a22df11d45a5332e21c")
    version("1.1.0", sha256="d9899cf9842f2fe4b0dc3c659dabc8ae32e192151f5be3709a1cd7be5a2c0a9a")
    version("1.0.1", sha256="a0548ac6221fce09a5a6877c8db19e8755e175f97b934e69a449170a604825dd")
    version("1.0", sha256="6b75305f49cdff890df52a3a341060e8909592d8a9a9b330bb6808153b0a2078")
    version("0.15.1", sha256="e25d068d753d1a7d498ae6fdf916da08c3a1aa9ddfb4c5078750009359bb3a75")
    version("0.15.0", sha256="6a319f56b9f68c9de3f0b4bf5a6a47e065f4bde50e64f715e12819b2e6f92e4d")
    version("0.14.1", sha256="274de48593d153d4cb4c487c902eafcdbd3224f1b846ff832aba03396d8453c7")
    version("0.14.0", sha256="fbe4e1d04bf57faeb53c6ae2a2a280504a3c8c9cd1f47db6180c1f8d7e48364d")
    version("0.13.0", sha256="69ff5503313fbfcb7b911f2129f16f61a61c7d1a7f13e73f8d6537eaac31e924")
    version("0.12.4", sha256="935b243bcf461bb0c6e6c938cd21498edbe204861c4db0869a42cca2f33ff95c")
    version("0.12.3", sha256="813cbbe26d521f1081774a4e041b3f068f41481071ba01a4154b4876eaafea90")
    version("0.12.2", sha256="26a67f6a9e288117833e498cc02ed61e1e9439e6275ddfe2478da62cdf20e9ba")
    version("0.12.1", sha256="2865bde4ab2c53e257755cb8f281ee6fba5a9bf54bc3c503edfa36dc03b484fd")
    version("0.12.0", sha256="e885a7bdd8923f828aba3a924ad992c81c0c67f80265279017dd71b5acafd84e")
    version("0.11.0", sha256="cc1d141a91e180c9a151369592bcd6b864c9bf581f2db837ab365aec1533bb3e")
    version("0.10.6", sha256="5727770bb8cea75e6bd76e0911008217a0fd07ed84ae82d967c7bdd98f9c7749")
    version("0.10.5", sha256="59ac82c32b6493bf0a6042ef39549368ad8f0d3ec2151ab040f4ce28c93d751e")
    version("0.10.4", sha256="db46889bc8908318e15f26f4bde8eb31824cb117d9234afb77a348ad4b6f5050")
    version("0.10.3", sha256="4a5393ff47493a80d28a53ce307bffa52a066fd82045a5598b8da074a2f7dfe7")
    version("0.10.2", sha256="2d62bcad5ef7609813381e77a6422fec3d4cbd6347f4297b687510ab4d32e813")
    version("0.10.1", sha256="632b8942d8c85b36997ce3ed893bc34c868b432fbaadd4ea86994ca881d6665b")
    version("0.10.0", sha256="cd554729fa9d0ec17164afbc1cea62d02bde3db8e16db3fd1b8e71d8e1b3dd41")
    version("0.9.1", sha256="a9655a471d0649f5540b890447b35849c162d9b986bf2bbddcb68461748e0f42")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("py-tomli", when="@9:", type="build")
    depends_on("meson@1.1.0:", when="@9:", type="build")

    depends_on("bison", when="@9:")
    depends_on("bzip2", when="@9:")
    depends_on("capstone", when="@9:")
    depends_on("dtc", when="@9:")
    depends_on("flex", when="@9:")
    depends_on("glib@2.40:")
    depends_on("gnutls", when="@9:")
    depends_on("libslirp", when="@9:")
    depends_on("libssh", when="@9:")
    depends_on("libusb", when="@9:")
    depends_on("lzo", when="@9:")
    depends_on("ncurses", when="@9:")
    depends_on("nettle", when="@9:")
    depends_on("pixman@0.21.8:")
    depends_on("snappy", when="@9:")
    depends_on("vde", when="@9:")
    depends_on("zlib", when="@9:")
    depends_on("zstd", when="@9:")

    # linux deps not needed on darwin
    depends_on("elfutils", when="@9: platform=linux")
    depends_on("libcap-ng", when="@9: platform=linux")

    build_directory = "build"

    @when("@9:")
    def configure_args(self):
        return [
            "--disable-bsd-user",
            "--disable-guest-agent",
            "--disable-sdl",
            "--disable-bsd-user",
            "--disable-guest-agent",
            "--enable-slirp",
            "--enable-capstone",
            "--enable-curses",
            "--enable-fdt=system",
            "--enable-libssh",
            "--enable-vde",
            "--enable-virtfs",
            "--enable-zstd",
            "--disable-docs",
        ]
