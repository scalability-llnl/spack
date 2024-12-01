# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gradle(Package):
    """Gradle is an open source build automation system that builds
    upon the concepts of Apache Ant and Apache Maven and introduces
    a Groovy-based domain-specific language (DSL) instead of the XML
    form used by Apache Maven for declaring the project configuration.
    Gradle uses a directed acyclic graph ("DAG") to determine the
    order in which tasks can be run."""

    homepage = "https://gradle.org"
    url = "https://services.gradle.org/distributions/gradle-3.4-all.zip"

    license("Apache-2.0", checked_by="wdconinc")

    version("8.10.2", sha256="2ab88d6de2c23e6adae7363ae6e29cbdd2a709e992929b48b6530fd0c7133bd6")
    version("8.10.1", sha256="fdfca5dbc2834f0ece5020465737538e5ba679deeff5ab6c09621d67f8bb1a15")
    version("8.10", sha256="682b4df7fe5accdca84a4d1ef6a3a6ab096b3efd5edf7de2bd8c758d95a93703")
    version("8.9", sha256="258e722ec21e955201e31447b0aed14201765a3bfbae296a46cf60b70e66db70")
    version("8.8", sha256="f8b4f4772d302c8ff580bc40d0f56e715de69b163546944f787c87abf209c961")
    version("8.7", sha256="194717442575a6f96e1c1befa2c30e9a4fc90f701d7aee33eb879b79e7ff05c0")
    version("8.6", sha256="85719317abd2112f021d4f41f09ec370534ba288432065f4b477b6a3b652910d")
    version("8.5", sha256="c16d517b50dd28b3f5838f0e844b7520b8f1eb610f2f29de7e4e04a1b7c9c79b")
    version("8.4", sha256="f2b9ed0faf8472cbe469255ae6c86eddb77076c75191741b4a462f33128dd419")
    version("8.3", sha256="bb09982fdf52718e4c7b25023d10df6d35a5fff969860bdf5a5bd27a3ab27a9e")
    version("8.2.1", sha256="7c3ad722e9b0ce8205b91560fd6ce8296ac3eadf065672242fd73c06b8eeb6ee")
    version("8.2", sha256="5022b0b25fe182b0e50867e77f484501dba44feeea88f5c1f13b6b4660463640")
    version("8.1.1", sha256="5625a0ae20fe000d9225d000b36909c7a0e0e8dda61c19b12da769add847c975")
    version("8.0.2", sha256="47a5bfed9ef814f90f8debcbbb315e8e7c654109acd224595ea39fca95c5d4da")
    version("7.3", sha256="00b273629df4ce46e68df232161d5a7c4e495b9a029ce6e0420f071e21316867")
    version("7.2", sha256="a8da5b02437a60819cad23e10fc7e9cf32bcb57029d9cb277e26eeff76ce014b")
    version("7.1.1", sha256="9bb8bc05f562f2d42bdf1ba8db62f6b6fa1c3bf6c392228802cc7cb0578fe7e0")
    version("7.1", sha256="a9e356a21595348b6f04b024ed0b08ac8aea6b2ac37e6c0ef58e51549cd7b9cb")
    version("7.0.2", sha256="13bf8d3cf8eeeb5770d19741a59bde9bd966dd78d17f1bbad787a05ef19d1c2d")
    version("7.0.1", sha256="ca42877db3519b667cd531c414be517b294b0467059d401e7133f0e55b9bf265")
    version("7.0", sha256="81003f83b0056d20eedf48cddd4f52a9813163d4ba185bcf8abd34b8eeea4cbd")
    version("6.9.1", sha256="b13f5d97f08000996bf12d9dd70af3f2c6b694c2c663ab1b545e9695562ad1ee")
    version("6.9", sha256="5d234488d2cac2ed556dc3c47096e189ad76a63cf304ebf124f756498922cf16")
    version("6.8.3", sha256="9af5c8e7e2cd1a3b0f694a4ac262b9f38c75262e74a9e8b5101af302a6beadd7")
    version("6.8.2", sha256="1433372d903ffba27496f8d5af24265310d2da0d78bf6b4e5138831d4fe066e9")
    version("6.8.1", sha256="3db89524a3981819ff28c3f979236c1274a726e146ced0c8a2020417f9bc0782")
    version("6.8", sha256="a7ca23b3ccf265680f2bfd35f1f00b1424f4466292c7337c85d46c9641b3f053")
    version("6.7.1", sha256="22449f5231796abd892c98b2a07c9ceebe4688d192cd2d6763f8e3bf8acbedeb")
    version("6.7", sha256="0080de8491f0918e4f529a6db6820fa0b9e818ee2386117f4394f95feb1d5583")
    version("6.6.1", sha256="11657af6356b7587bfb37287b5992e94a9686d5c8a0a1b60b87b9928a2decde5")
    version("6.6", sha256="83fa7c3e5ab84c3c5c4a04fb16947338209efa9aab1f6bf09a5d0e3d2ed87742")
    version("6.5.1", sha256="143a28f54f1ae93ef4f72d862dbc3c438050d81bb45b4601eb7076e998362920")
    version("6.5", sha256="c9910513d0eed63cd8f5c7fec4cb4a05731144770104a0871234a4edc3ba3cef")
    version("6.4.1", sha256="3fd824892df8ad5847be6e4fb7d3600068437de172939fd657cc280a1a629f63")
    version("6.4", sha256="d08f7e24d061910382c2fda9915e6ed42dd1480ae2e99211f92c70190cb697e0")
    version("6.3", sha256="0f316a67b971b7b571dac7215dcf2591a30994b3450e0629925ffcfe2c68cc5c")
    version("6.2.2", sha256="838fa0e3373a9c8d953eff972449edc6be5fa12b26509ac3387727de85138cc0")
    version("6.2.1", sha256="49fad5c94e76bc587c1a1138f045daee81476a82b288c7ab8c7cd6b14bf2b1c7")
    version("6.2", sha256="f016e66d88c2f9adb5b6e7dff43a363b8c2632f18b4ad6f365f49da34dd57db8")
    version("6.1.1", sha256="10065868c78f1207afb3a92176f99a37d753a513dff453abb6b5cceda4058cda")
    version("6.1", sha256="634f972af958e3c753aeb42d7a688fab6820b527a0aef9eed03d7f3f6f9c7c06")
    version("6.0.1", sha256="6f6cfdbb12a577c3845522a1c7fbfe1295ea05d87edabedd4e23fd2bf02b88b1")
    version("6.0", sha256="a1eb4439c0a85bc7e64a22658d862e43b7d0ddfbf69a7abf6256e0b7514295df")
    version("5.6.4", sha256="abc10bcedb58806e8654210f96031db541bcd2d6fc3161e81cb0572d6a15e821")
    version("5.6.3", sha256="342f8e75a8879fa9192163fa8d932b9f6383ea00c1918a478f0f51e11e004b60")
    version("5.6.2", sha256="027fdd265d277bae65a0d349b6b8da02135b0b8e14ba891e26281fa877fe37a2")
    version("5.6.1", sha256="f6ea7f48e2823ca7ff8481044b892b24112f5c2c3547d4f423fb9e684c39f710")
    version("5.6", sha256="33214524e686838c88a88e14e8b30e2323589cc9698186bc8e0594758b132b31")
    version("5.5.1", sha256="6c4276f97c9059ef4dfb06cc7325c43ed9b933ab04f032e9d9372e8589cb6faf")
    version("5.5", sha256="302b7df46730ce75c582542c056c9bf5cac2b94fbf2cc656d0e37e41e8a5d371")
    version("5.4.1", sha256="14cd15fc8cc8705bd69dcfa3c8fefb27eb7027f5de4b47a8b279218f76895a91")
    version("5.4", sha256="f177768e7a032727e4338c8fd047f8f263e5bd283f67a7766c1ba4182c8455a6")
    version("5.3.1", sha256="b018a7308cb43633662363d100c14a3c41c66fd4e32b59e1dfc644d6fd2109f6")
    version("5.3", sha256="f4d820c2a9685710eba5b92f10e0e4fb20e0d6c0dd1f46971e658160f25e7147")
    version("5.2.1", sha256="9dc729f6dbfbbc4df1692665d301e028976dacac296a126f16148941a9cf012e")
    version("5.2", sha256="55db797adf2705bb782655f012af7cc7724b14382881f60fb3f3eb4b645c02d6")
    version("5.1.1", sha256="53b71812f18cdb2777e9f1b2a0f2038683907c90bdc406bc64d8b400e1fb2c3b")
    version("5.1", sha256="7b8a8b9cce0406733d2d3fab3874386c530657c73c3f4e9a3837d081e26060d8")
    version("5.0", sha256="17847c8e12b2bcfce26a79f425f082c31d4ded822f99a66127eee2d96bf18216")
    version("4.10.3", sha256="336b6898b491f6334502d8074a6b8c2d73ed83b92123106bd4bf837f04111043")
    version("4.10.2", sha256="b7aedd369a26b177147bcb715f8b1fc4fe32b0a6ade0d7fd8ee5ed0c6f731f2c")
    version("4.10.1", sha256="36bf7ff499223d5139f005822130ccca784c91591b514677fd376eed966c907e")
    version("4.10", sha256="fc049dcbcb245d5892bebae143bd515a78f6a5a93cec99d489b312dc0ce4aad9")
    version("4.9", sha256="39e2d5803bbd5eaf6c8efe07067b0e5a00235e8c71318642b2ed262920b27721")
    version("4.8.1", sha256="ce1645ff129d11aad62dab70d63426fdce6cfd646fa309dc5dc5255dd03c7c11")
    version("3.4", sha256="37c2fdce55411e4c89b896c292cae1f8f437862c8433c8a74cfc3805d7670c0a")
    version("3.3", sha256="71a787faed83c4ef21e8464cc8452b941b5fcd575043aa29d39d15d879be89f7")
    version("3.2.1", sha256="0209696f1723f607c475109cf3ed8b51c8a91bb0cda05af0d4bd980bdefe75cd")
    version("3.2", sha256="e25ff599ff268182b597c371ed94eb3c225496af5d4e7eb9dcbb08d30f93a9ec")
    version("3.1", sha256="43be380834a13e28e9504c21f67fe1a8895ab54f314a6596601896dca7213482")
    version("3.0", sha256="9c8b7564ea6a911b5b9fcadd60f3a6cea4238413c8b1e1dd14400a50954aab99")
    version("2.14.1", sha256="88a910cdf2e03ebbb5fe90f7ecf534fc9ac22e12112dc9a2fee810c598a76091")
    version("2.14", sha256="65bbc0ef9c48be86fb06522fc927d59dcc7c04266f2bb8156be76971f7c3fc4a")
    version("2.13", sha256="fb126ed684150f9dc39a811cbcf4daada4292fd387ed998c151ff2cf2536d94d")
    version("2.12", sha256="d8b1948a575dc9ec13e03db94502ce91815d73da023f611296c04b852164cb5f")
    version("2.11", sha256="a1242e4db8f979998796b1844e608c2acf8f8f54df518bbb3d5954e52253ba71")
    version("2.10", sha256="496d60c331f8666f99b66d08ff67a880697a7e85a9d9b76ff08814cf97f61a4c")
    version("2.9", sha256="4647967f8de78d6d6d8093cdac50f368f8c2b8038f41a5afe1c3bce4c69219a9")
    version("2.8", sha256="65f3880dcb5f728b9d198b14d7f0a678d35ecd33668efc219815a9b4713848be")
    version("2.7", sha256="2ba0aaa11a3e96ec0af31d532d808e1f09cc6dcad0954e637902a1ab544b9e60")
    version("2.6", sha256="5489234fc9c9733fc4115055618763ccb4d916d667980e6ab4fa57fc81197d16")
    version("2.5", sha256="b71ab21fa5e91dcc6a4bd723b13403e8610a6e1b4b9d4b314ff477820de00bf9")
    version("2.4", sha256="371cb9fbebbe9880d147f59bab36d61eee122854ef8c9ee1ecf12b82368bcf10")
    version("2.3", sha256="515962aeec8c3e67b97f0c13c4575beeed1b5da16181d8b9054416339edc8c2d")
    version("2.2.1", sha256="1d7c28b3731906fd1b2955946c1d052303881585fc14baedd675e4cf2bc1ecab")
    version("2.2", sha256="65fc05f787c7344cc8834dc13a445c91ea3712a987f5958b8489422484d7371b")
    version("2.1", sha256="b351ab27da6e06a74ba290213638b6597f2175f5071e6f96a0a205806720cb81")
    version("2.0", sha256="11c32ed95c0ed44e091154391d69008ac5ec25ad897bc881547e6942a03aeb13")
    version("1.12", sha256="cf111fcb34804940404e79eaf307876acb8434005bc4cc782d260730a0a2a4f2")
    version("1.11", sha256="07e58cd960722c419eb0f6a807228e7179bb43bc266f390cde4632abdacdd659")
    version("1.10", sha256="cd1a0f532258369c414a56b3e73b7bd7f087cf515b7c71dcb9091598c4a8d815")
    version("1.9", sha256="eeb919fe734bc4a63aaf75c05c19bc55c8bccc925b0eca4269c67f7e8cf48efb")
    version("1.8", sha256="4f03076116841743808c2f2c1ae2041d03adebe09ab80356b87516c7ed055e40")
    version("1.5", sha256="fecf73744c5695e2a3078104072ae2a9fdec17e36dc058dc20adf8c7be8af13b")
    version("1.4", sha256="436771c854cc665c790a6c452a2878dfbdaaf9d14e505a58127b407bb05b013f")
    version("1.3", sha256="c8572e9579e2300c5e2e8ae8f1a2433d9fd7ad9a4b1e721a5ee588c72fbf7799")
    version("1.2", sha256="ea66177dd532da09cb28d050e880961df5bd7ba014eda709c76f2c022f069282")
    version("1.1", sha256="00519a961f7f902123368c5bfe4c01be607628410620c8c8a466fbb0de8c6715")
    version("1.0", sha256="510258aa9907a8b406a118eed1f57cfe7994c4fe0a37a6f08403fe3620526504")
    version("0.9.2", sha256="a9b33c1cb7c056a7bd26b588301ce80f0b6e3872d18b0f1cb80ab74af0e62404")
    version("0.9.1", sha256="6b9e2033e856ed99b968d71c2dc5174dc5637c10d5e4cc9502a51e86f45709eb")
    version("0.9", sha256="a06117e826ea8713f61e47b2fe2d7621867c56f4c44e4e8012552584e08b9c1b")
    version("0.8", sha256="42e0db29f2e0be4eeadfe77b6491d9e2b21b95abb92fc494dfcf8615f2126910")
    version("0.7", sha256="ca902f52f0789ab94762f7081b06461f8d3a03540ab73bf2d642f2d03e8558ef")

    depends_on("java")

    def install(self, spec, prefix):
        install_tree(".", prefix)
