# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nano(AutotoolsPackage):
    """Tiny little text editor"""

    homepage = "http://www.nano-editor.org"
    url      = "https://www.nano-editor.org/dist/v4/nano-4.9.tar.xz"
    list_url = "https://www.nano-editor.org/dist/"
    list_depth = 1

    # 4.x
    version('4.9', sha256='0e399729d105cb1a587b4140db5cf1b23215a0886a42b215efa98137164233a6')
    version('4.8', sha256='c348f61c68ab1d573b308398212a09cd68c60fbee20f01a5bd4b50071a258e63')
    version('4.7', sha256='58c0e197de5339ca3cad3ef42b65626d612ddb0b270e730f02e6ab3785c736f5')
    version('4.6', sha256='9bac3a4153774fd921dd3eb291986d43985466b081165b5ac5262b37b79628e9')
    version('4.5', sha256='ded5c38f5ecd9de2b624e0db8013a375c169d3fbbd49575967b868847df8f533')
    version('4.4', sha256='2af222e0354848ffaa3af31b5cd0a77917e9cb7742cd073d762f3c32f0f582c7')
    version('4.3', sha256='00d3ad1a287a85b4bf83e5f06cedd0a9f880413682bebd52b4b1e2af8cfc0d81')
    version('4.2', sha256='1143defce62e391b241252ffdb6e5c1ded56cfe26d46ee81b796abe0ccc45df9')
    version('4.1', sha256='86bde596a038d6fde619b49d785c0ebf0b3eaa7001a39dbe9316bd5392d221d0')
    version('4.0', sha256='1e2fcfea35784624a7d86785768b772d58bb3995d1aec9176a27a113b1e9bac3')
    # 3.x
    version('3.2', sha256='d12773af3589994b2e4982c5792b07c6240da5b86c5aef2103ab13b401fe6349')
    version('3.1', sha256='14c02ca40a5bc61c580ce2f9cb7f9fc72d5ccc9da17ad044f78f6fb3fdb7719e')
    version('3.0', sha256='e0a5bca354514e64762c987c200a8758b05e7bcced3b00b3e48ea0a2d383c8a0')
    # 2.9.x
    version('2.9.8', sha256='c2deac31ba4d3fd27a42fafcc47ccf499296cc69a422bbecab63f2933ea85488')
    version('2.9.7', sha256='b64ab017305b1777e97b5b9b07b31db8aeebfc3e8719f61e8da1cf3866d344bd')
    version('2.9.6', sha256='a373507ebb4e9307a8202fbc19b5d29718025c8ec773669349211c362545d4c6')
    version('2.9.5', sha256='7b8d181cb57f42fa86a380bb9ad46abab859b60383607f731b65a9077f4b4e19')
    version('2.9.4', sha256='2cf9726e735f5c962af63d27c2faaead5936e45adec983659fb9e4af88ffa35a')
    version('2.9.3', sha256='7783bcfd4b2d5dc0bf64d4bd07b1a19e7ba3c91da881a4249772a36b972d4012')
    version('2.9.2', sha256='4eccb7451b5729ce8abae8f9a5679f32e41ae58df73ea86b850ec45b10a83d55')
    version('2.9.1', sha256='6316d52d0d26af3e79a13dcb4db1c7a4aeac61b37fd9381e801a4189a2ecba7c')
    version('2.9.0', sha256='d2d30c39caef53aba1ec1b4baff4186d4496f35d2411b0848242a5f2e27e129e')
    # 2.8.x
    version('2.8.7', sha256='fbe31746958698d73c6726ee48ad8b0612697157961a2e9aaa83b4aa53d1165a')
    version('2.8.6', sha256='9a46962a3ae59db922467a095217ed23280b42d80640f932f3a59ba2a6a85776')
    version('2.8.5', sha256='cb43bf11990b2839446229b0c21ed7abef67c2df861f250cc874553ca27d89c2')
    version('2.8.4', sha256='c7cf264f0f3e4af43ecdbc4ec72c3b1e831c69a1a5f6512d5b0c109e6bac7b11')
    version('2.8.3', sha256='62b8e55b934091edbb41e948eac3d6769cc13d18b837c38faf7226c0820b0f55')
    version('2.8.2', sha256='023e8a7b38b2420d5476d7b2b4d8524d7de55c0853b4dc0b02e4a4adf7ecb9e0')
    version('2.8.1', sha256='e935a8bb373345c833dff3a304c6d392775d206b94c802d9285ae80ac6b66d0b')
    version('2.8.0', sha256='15c1bcf4d8888d3b56f68a0b75871cc349b81a9094f8a42d73010ffc26c85dc2')
    # 2.7.x
    version('2.7.5', sha256='a64d24e6bc4fc448376d038f9a755af77f8e748c9051b6f45bf85e783a7e67e4')
    version('2.7.4', sha256='752170643039e2c95a433de357f0c70a8c4c4c561a90a7e7259a63e225b659b9')
    version('2.7.3', sha256='d926ef5060d23bafec75dab9328bb9b9df9a08e58c56b9061d686f5698770bfc')
    version('2.7.2', sha256='77016f73c686857ce8a3ec217832febb6e636122762d47ce3c6cbef6f7e390c2')
    version('2.7.1', sha256='df5cbe69831d7394c0a32fb27373ab313335ea4dc586d6f4be4081eb1de857cd')
    version('2.7.0', sha256='f86af39514ae74e20bef3c29cd01d1090a9aca772a70e9c9f9e70c3d14b39521')
    # 2.6.x
    version('2.6.3', sha256='69ecbfbaa845800f43c27d6190ca87d277f3278f81e9c55ee569181b572b7519')
    version('2.6.2', sha256='22f79cc635458e0c0d110d211576f1edc03b112a62d73b914826a46547a6ac27')
    version('2.6.1', sha256='45721fa6d6128068895ad71a6967ff7398d11b064b3f888e5073c97a2b6e9a81')

    depends_on('ncurses')

    def url_for_version(self, version):
        url = "https://www.nano-editor.org/dist/v{0}/nano-{1}.tar.xz"
        subdir = version.up_to(2)
        major = version.up_to(1)
        if int(str(major)) > 2:
            subdir = major
        return url.format(subdir, version)
