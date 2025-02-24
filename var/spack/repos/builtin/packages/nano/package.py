# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nano(AutotoolsPackage):
    """Tiny little text editor"""

    homepage = "https://www.nano-editor.org"
    url = "https://www.nano-editor.org/dist/v6/nano-6.3.tar.xz"
    list_url = "https://www.nano-editor.org/dist/"
    list_depth = 1

    license("GPL-3.0-or-later", checked_by="wdconinc")

    # 8.x
    version("8.2", sha256="d5ad07dd862facae03051c54c6535e54c7ed7407318783fcad1ad2d7076fffeb")
    version("8.1", sha256="93b3e3e9155ae389fe9ccf9cb7ab380eac29602835ba3077b22f64d0f0cbe8cb")
    version("8.0", sha256="c17f43fc0e37336b33ee50a209c701d5beb808adc2d9f089ca831b40539c9ac4")
    # 7.x
    version("7.2", sha256="86f3442768bd2873cec693f83cdf80b4b444ad3cc14760b74361474fc87a4526")
    # 6.x
    version("6.4", sha256="4199ae8ca78a7796de56de1a41b821dc47912c0307e9816b56cc317df34661c0")
    version("6.3", sha256="eb532da4985672730b500f685dbaab885a466d08fbbf7415832b95805e6f8687")
    version("6.2", sha256="2bca1804bead6aaf4ad791f756e4749bb55ed860eec105a97fba864bc6a77cb3")
    version("6.1", sha256="3d57ec893fbfded12665b7f0d563d74431fc43abeaccacedea23b66af704db40")
    version("6.0", sha256="93ac8cb68b4ad10e0aaeb80a2dd15c5bb89eb665a4844f7ad01c67efcb169ea2")
    # 5.x
    version("5.9", sha256="757db8cda4bb2873599e47783af463e3b547a627b0cabb30ea7bf71fb4c24937")
    version("5.8", sha256="e43b63db2f78336e2aa123e8d015dbabc1720a15361714bfd4b1bb4e5e87768c")
    version("5.7", sha256="d4b181cc2ec11def3711b4649e34f2be7a668e70ab506860514031d069cccafa")
    version("5.6", sha256="fce183e4a7034d07d219c79aa2f579005d1fd49f156db6e50f53543a87637a32")
    version("5.5", sha256="390b81bf9b41ff736db997aede4d1f60b4453fbd75a519a4ddb645f6fd687e4a")
    version("5.4", sha256="fe993408b22286355809ce48ebecc4444d19af8203ed4959d269969112ed86e9")
    version("5.3", sha256="c5c1cbcf622d9a96b6030d66409ed12b204e8bc01ef5e6554ebbe6fb1d734352")
    version("5.2", sha256="32c2da43e1ae9a5e43437d8c6e1ec0388af870c7762c479e5bffb5f292bda7e1")
    version("5.1", sha256="9efc46f341404d60095d16fc4f0419fc84b6e4eaeaf6ebce605d0465d92a6ee6")
    version("5.0", sha256="7c0d94be69cd066f20df2868a2da02f7b1d416ce8d47c0850a8bd270897caa36")
    # 4.x
    version("4.9", sha256="0e399729d105cb1a587b4140db5cf1b23215a0886a42b215efa98137164233a6")
    version("4.8", sha256="c348f61c68ab1d573b308398212a09cd68c60fbee20f01a5bd4b50071a258e63")
    version("4.7", sha256="58c0e197de5339ca3cad3ef42b65626d612ddb0b270e730f02e6ab3785c736f5")
    version("4.6", sha256="9bac3a4153774fd921dd3eb291986d43985466b081165b5ac5262b37b79628e9")
    version("4.5", sha256="ded5c38f5ecd9de2b624e0db8013a375c169d3fbbd49575967b868847df8f533")
    version("4.4", sha256="2af222e0354848ffaa3af31b5cd0a77917e9cb7742cd073d762f3c32f0f582c7")
    version("4.3", sha256="00d3ad1a287a85b4bf83e5f06cedd0a9f880413682bebd52b4b1e2af8cfc0d81")
    version("4.2", sha256="1143defce62e391b241252ffdb6e5c1ded56cfe26d46ee81b796abe0ccc45df9")
    version("4.1", sha256="86bde596a038d6fde619b49d785c0ebf0b3eaa7001a39dbe9316bd5392d221d0")
    version("4.0", sha256="1e2fcfea35784624a7d86785768b772d58bb3995d1aec9176a27a113b1e9bac3")
    # 3.x
    version("3.2", sha256="d12773af3589994b2e4982c5792b07c6240da5b86c5aef2103ab13b401fe6349")
    version("3.1", sha256="14c02ca40a5bc61c580ce2f9cb7f9fc72d5ccc9da17ad044f78f6fb3fdb7719e")
    version("3.0", sha256="e0a5bca354514e64762c987c200a8758b05e7bcced3b00b3e48ea0a2d383c8a0")
    # 2.9.x
    version("2.9.8", sha256="c2deac31ba4d3fd27a42fafcc47ccf499296cc69a422bbecab63f2933ea85488")
    version("2.9.7", sha256="b64ab017305b1777e97b5b9b07b31db8aeebfc3e8719f61e8da1cf3866d344bd")
    version("2.9.6", sha256="a373507ebb4e9307a8202fbc19b5d29718025c8ec773669349211c362545d4c6")
    version("2.9.5", sha256="7b8d181cb57f42fa86a380bb9ad46abab859b60383607f731b65a9077f4b4e19")
    version("2.9.4", sha256="2cf9726e735f5c962af63d27c2faaead5936e45adec983659fb9e4af88ffa35a")
    version("2.9.3", sha256="7783bcfd4b2d5dc0bf64d4bd07b1a19e7ba3c91da881a4249772a36b972d4012")
    version("2.9.2", sha256="4eccb7451b5729ce8abae8f9a5679f32e41ae58df73ea86b850ec45b10a83d55")
    version("2.9.1", sha256="6316d52d0d26af3e79a13dcb4db1c7a4aeac61b37fd9381e801a4189a2ecba7c")
    version("2.9.0", sha256="d2d30c39caef53aba1ec1b4baff4186d4496f35d2411b0848242a5f2e27e129e")
    # 2.8.x
    version("2.8.7", sha256="fbe31746958698d73c6726ee48ad8b0612697157961a2e9aaa83b4aa53d1165a")
    version("2.8.6", sha256="9a46962a3ae59db922467a095217ed23280b42d80640f932f3a59ba2a6a85776")
    version("2.8.5", sha256="cb43bf11990b2839446229b0c21ed7abef67c2df861f250cc874553ca27d89c2")
    version("2.8.4", sha256="c7cf264f0f3e4af43ecdbc4ec72c3b1e831c69a1a5f6512d5b0c109e6bac7b11")
    version("2.8.3", sha256="62b8e55b934091edbb41e948eac3d6769cc13d18b837c38faf7226c0820b0f55")
    version("2.8.2", sha256="023e8a7b38b2420d5476d7b2b4d8524d7de55c0853b4dc0b02e4a4adf7ecb9e0")
    version("2.8.1", sha256="e935a8bb373345c833dff3a304c6d392775d206b94c802d9285ae80ac6b66d0b")
    version("2.8.0", sha256="15c1bcf4d8888d3b56f68a0b75871cc349b81a9094f8a42d73010ffc26c85dc2")
    # 2.7.x
    version("2.7.5", sha256="a64d24e6bc4fc448376d038f9a755af77f8e748c9051b6f45bf85e783a7e67e4")
    version("2.7.4", sha256="752170643039e2c95a433de357f0c70a8c4c4c561a90a7e7259a63e225b659b9")
    version("2.7.3", sha256="d926ef5060d23bafec75dab9328bb9b9df9a08e58c56b9061d686f5698770bfc")
    version("2.7.2", sha256="77016f73c686857ce8a3ec217832febb6e636122762d47ce3c6cbef6f7e390c2")
    version("2.7.1", sha256="df5cbe69831d7394c0a32fb27373ab313335ea4dc586d6f4be4081eb1de857cd")
    version("2.7.0", sha256="f86af39514ae74e20bef3c29cd01d1090a9aca772a70e9c9f9e70c3d14b39521")
    # 2.6.x
    version("2.6.3", sha256="69ecbfbaa845800f43c27d6190ca87d277f3278f81e9c55ee569181b572b7519")
    version("2.6.2", sha256="22f79cc635458e0c0d110d211576f1edc03b112a62d73b914826a46547a6ac27")
    version("2.6.1", sha256="45721fa6d6128068895ad71a6967ff7398d11b064b3f888e5073c97a2b6e9a81")

    depends_on("c", type="build")

    depends_on("pkgconfig", type="build")
    depends_on("gettext@0.18.3:")
    depends_on("gettext@0.20:", when="@8.1:")
    depends_on("ncurses")

    def url_for_version(self, version):
        url = "https://www.nano-editor.org/dist/v{0}/nano-{1}.tar.xz"
        subdir = version.up_to(2)
        major = version.up_to(1)
        if int(str(major)) > 2:
            subdir = major
        return url.format(subdir, version)
