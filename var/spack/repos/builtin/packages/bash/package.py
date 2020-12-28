# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Bash(AutotoolsPackage, GNUMirrorPackage):
    """The GNU Project's Bourne Again SHell."""

    homepage = "https://www.gnu.org/software/bash/"
    gnu_mirror_path = "bash/bash-5.0.tar.gz"

    maintainers = ['adamjstewart']

    version('5.0', sha256='b4a80f2ac66170b2913efbfb9f2594f1f76c7b1afd11f799e22035d63077fb4d')
    version('4.4', sha256='d86b3392c1202e8ff5a423b302e6284db7f8f435ea9f39b5b1b20fd3ac36dfcb')
    version('4.3', sha256='afc687a28e0e24dc21b988fa159ff9dbcf6b7caa92ade8645cc6d5605cd024d4')

    depends_on('ncurses')
    depends_on('readline@5.0:')
    depends_on('iconv')

    patches = [
        ('5.0', '001', 'f2fe9e1f0faddf14ab9bfa88d450a75e5d028fedafad23b88716bd657c737289'),
        ('5.0', '002', '87e87d3542e598799adb3e7e01c8165bc743e136a400ed0de015845f7ff68707'),
        ('5.0', '003', '4eebcdc37b13793a232c5f2f498a5fcbf7da0ecb3da2059391c096db620ec85b'),
        ('5.0', '004', '14447ad832add8ecfafdce5384badd933697b559c4688d6b9e3d36ff36c62f08'),
        ('5.0', '005', '5bf54dd9bd2c211d2bfb34a49e2c741f2ed5e338767e9ce9f4d41254bf9f8276'),
        ('5.0', '006', 'd68529a6ff201b6ff5915318ab12fc16b8a0ebb77fda3308303fcc1e13398420'),
        ('5.0', '007', '17b41e7ee3673d8887dd25992417a398677533ab8827938aa41fad70df19af9b'),
        ('5.0', '008', 'eec64588622a82a5029b2776e218a75a3640bef4953f09d6ee1f4199670ad7e3'),
        ('5.0', '009', 'ed3ca21767303fc3de93934aa524c2e920787c506b601cc40a4897d4b094d903'),
        ('5.0', '010', 'd6fbc325f0b5dc54ddbe8ee43020bced8bd589ddffea59d128db14b2e52a8a11'),
        ('5.0', '011', '2c4de332b91eaf797abbbd6c79709690b5cbd48b12e8dfe748096dbd7bf474ea'),
        ('5.0', '012', '2943ee19688018296f2a04dbfe30b7138b889700efa8ff1c0524af271e0ee233'),
        ('5.0', '013', 'f5d7178d8da30799e01b83a0802018d913d6aa972dd2ddad3b927f3f3eb7099a'),
        ('5.0', '014', '5d6eee6514ee6e22a87bba8d22be0a8621a0ae119246f1c5a9a35db1f72af589'),
        ('5.0', '015', 'a517df2dda93b26d5cbf00effefea93e3a4ccd6652f152f4109170544ebfa05e'),
        ('5.0', '016', 'ffd1d7a54a99fa7f5b1825e4f7e95d8c8876bc2ca151f150e751d429c650b06d'),
        ('5.0', '017', '4cf3b9fafb8a66d411dd5fc9120032533a4012df1dc6ee024c7833373e2ddc31'),
        ('5.0', '018', '7c314e375a105a6642e8ed44f3808b9def89d15f7492fe2029a21ba9c0de81d3'),

        ('4.4', '001', '3e28d91531752df9a8cb167ad07cc542abaf944de9353fe8c6a535c9f1f17f0f'),
        ('4.4', '002', '7020a0183e17a7233e665b979c78c184ea369cfaf3e8b4b11f5547ecb7c13c53'),
        ('4.4', '003', '51df5a9192fdefe0ddca4bdf290932f74be03ffd0503a3d112e4199905e718b2'),
        ('4.4', '004', 'ad080a30a4ac6c1273373617f29628cc320a35c8cd06913894794293dc52c8b3'),
        ('4.4', '005', '221e4b725b770ad0bb6924df3f8d04f89eeca4558f6e4c777dfa93e967090529'),
        ('4.4', '006', '6a8e2e2a6180d0f1ce39dcd651622fb6d2fd05db7c459f64ae42d667f1e344b8'),
        ('4.4', '007', 'de1ccc07b7bfc9e25243ad854f3bbb5d3ebf9155b0477df16aaf00a7b0d5edaf'),
        ('4.4', '008', '86144700465933636d7b945e89b77df95d3620034725be161ca0ca5a42e239ba'),
        ('4.4', '009', '0b6bdd1a18a0d20e330cc3bc71e048864e4a13652e29dc0ebf3918bea729343c'),
        ('4.4', '010', '8465c6f2c56afe559402265b39d9e94368954930f9aa7f3dfa6d36dd66868e06'),
        ('4.4', '011', 'dd56426ef7d7295e1107c0b3d06c192eb9298f4023c202ca2ba6266c613d170d'),
        ('4.4', '012', 'fac271d2bf6372c9903e3b353cb9eda044d7fe36b5aab52f21f3f21cd6a2063e'),
        ('4.4', '013', '1b25efacbc1c4683b886d065b7a089a3601964555bcbf11f3a58989d38e853b6'),
        ('4.4', '014', 'a7f75cedb43c5845ab1c60afade22dcb5e5dc12dd98c0f5a3abcfb9f309bb17c'),
        ('4.4', '015', 'd37602ecbeb62d5a22c8167ea1e621fcdbaaa79925890a973a45c810dd01c326'),
        ('4.4', '016', '501f91cc89fadced16c73aa8858796651473602c722bb29f86a8ba588d0ff1b1'),
        ('4.4', '017', '773f90b98768d4662a22470ea8eec5fdd8e3439f370f94638872aaf884bcd270'),
        ('4.4', '018', '5bc494b42f719a8b0d844b7bd9ad50ebaae560e97f67c833c9e7e9d53981a8cc'),
        ('4.4', '019', '27170d6edfe8819835407fdc08b401d2e161b1400fe9d0c5317a51104c89c11e'),
        ('4.4', '020', '1840e2cbf26ba822913662f74037594ed562361485390c52813b38156c99522c'),
        ('4.4', '021', 'bd8f59054a763ec1c64179ad5cb607f558708a317c2bdb22b814e3da456374c1'),
        ('4.4', '022', '45331f0936e36ab91bfe44b936e33ed8a1b1848fa896e8a1d0f2ef74f297cb79'),
        ('4.4', '023', '4fec236f3fbd3d0c47b893fdfa9122142a474f6ef66c20ffb6c0f4864dd591b6'),

        ('4.3', '001', 'ecb3dff2648667513e31554b3ad054ccd89fce38e33367c9459ac3a285153742'),
        ('4.3', '002', 'eee7cd7062ab29a9e4f02924d9c367264dcb8b162703f74ff6eb8f175a91502b'),
        ('4.3', '003', '000e6eac50cd9053ce0630db01239dcdead04a2c2c351c47e2b51dac1ac1087d'),
        ('4.3', '004', '5ea0a42c6506720d26e6d3c5c358e9a0d49f6f189d69a8ed34d5935964821338'),
        ('4.3', '005', '1ac83044032b9f5f11aeca8a344ae3c524ec2156185d3adbb8ad3e7a165aa3fa'),
        ('4.3', '006', 'a0648ee72d15e4a90c8b77a5c6b19f8d89e28c1bc881657d22fe26825f040213'),
        ('4.3', '007', '1113e321c59cf6a8648a36245bbe4217cf8acf948d71e67886dad7d486f8f3a3'),
        ('4.3', '008', '9941a98a4987192cc5ce3d45afe879983cad2f0bec96d441a4edd9033767f95e'),
        ('4.3', '009', 'c0226d6728946b2f53cdebf090bcd1c01627f01fee03295768605caa80bb40a5'),
        ('4.3', '010', 'ce05799c0137314c70c7b6ea0477c90e1ac1d52e113344be8e32fa5a55c9f0b7'),
        ('4.3', '011', '7c63402cdbc004a210f6c1c527b63b13d8bb9ec9c5a43d5c464a9010ff6f7f3b'),
        ('4.3', '012', '3e1379030b35fbcf314e9e7954538cf4b43be1507142b29efae39eef997b8c12'),
        ('4.3', '013', 'bfa8ca5336ab1f5ef988434a4bdedf71604aa8a3659636afa2ce7c7446c42c79'),
        ('4.3', '014', '5a4d6fa2365b6eb725a9d4966248b5edf7630a4aeb3fa8d526b877972658ac13'),
        ('4.3', '015', '13293e8a24e003a44d7fe928c6b1e07b444511bed2d9406407e006df28355e8d'),
        ('4.3', '016', '92d60bcf49f61bd7f1ccb9602bead6f2c9946d79dea0e5ec0589bb3bfa5e0773'),
        ('4.3', '017', '1267c25c6b5ba57042a7bb6c569a6de02ffd0d29530489a16666c3b8a23e7780'),
        ('4.3', '018', '7aa8b40a9e973931719d8cc72284a8fb3292b71b522db57a5a79052f021a3d58'),
        ('4.3', '019', 'a7a91475228015d676cafa86d2d7aa9c5d2139aa51485b6bbdebfdfbcf0d2d23'),
        ('4.3', '020', 'ca5e86d87f178128641fe91f2f094875b8c1eb2de9e0d2e9154f5d5cc0336c98'),
        ('4.3', '021', '41439f06883e6bd11c591d9d5e9ae08afbc2abd4b935e1d244b08100076520a9'),
        ('4.3', '022', 'fd4d47bb95c65863f634c4706c65e1e3bae4ee8460c72045c0a0618689061a88'),
        ('4.3', '023', '9ac250c7397a8f53dbc84dfe790d2a418fbf1fe090bcece39b4a5c84a2d300d4'),
        ('4.3', '024', '3b505882a0a6090667d75824fc919524cd44cc3bd89dd08b7c4e622d3f960f6c'),
        ('4.3', '025', '1e5186f5c4a619bb134a1177d9e9de879f3bb85d9c5726832b03a762a2499251'),
        ('4.3', '026', '2ecc12201b3ba4273b63af4e9aad2305168cf9babf6d11152796db08724c214d'),
        ('4.3', '027', '1eb76ad28561d27f7403ff3c76a36e932928a4b58a01b868d663c165f076dabe'),
        ('4.3', '028', 'e8b0dbed4724fa7b9bd8ff77d12c7f03da0fbfc5f8251ef5cb8511eb082b469d'),
        ('4.3', '029', '4cc4a397fe6bc63ecb97d030a4e44258ef2d4e076d0e90c77782968cc43d6292'),
        ('4.3', '030', '85434f8a2f379d0c49a3ff6d9ffa12c8b157188dd739e556d638217d2a58385b'),
        ('4.3', '031', 'cd529f59dd0f2fdd49d619fe34691da6f0affedf87cc37cd460a9f3fe812a61d'),
        ('4.3', '032', '889357d29a6005b2c3308ca5b6286cb223b5e9c083219e5db3156282dd554f4a'),
        ('4.3', '033', 'fb2a7787a13fbe027a7335aca6eb3c21cdbd813e9edc221274b6a9d8692eaa16'),
        ('4.3', '034', 'f1694f04f110defe1330a851cc2768e7e57ddd2dfdb0e3e350ca0e3c214ff889'),
        ('4.3', '035', '370d85e51780036f2386dc18c5efe996eba8e652fc1973f0f4f2ab55a993c1e3'),
        ('4.3', '036', 'ac5f82445b36efdb543dbfae64afed63f586d7574b833e9aa9cd5170bc5fd27c'),
        ('4.3', '037', '33f170dd7400ab3418d749c55c6391b1d161ef2de7aced1873451b3a3fca5813'),
        ('4.3', '038', 'adbeaa500ca7a82535f0e88d673661963f8a5fcdc7ad63445e68bf5b49786367'),
        ('4.3', '039', 'ab94dced2215541097691f60c3eb323cc28ef2549463e6a5334bbcc1e61e74ec'),
        ('4.3', '040', '84bb396b9262992ca5424feab6ed3ec39f193ef5c76dfe4a62b551bd8dd9d76b'),
        ('4.3', '041', '4ec432966e4198524a7e0cd685fe222e96043769c9613e66742ac475db132c1a'),
        ('4.3', '042', 'ac219322db2791da87a496ee6e8e5544846494bdaaea2626270c2f73c1044919'),
        ('4.3', '043', '47a8a3c005b46e25821f4d8f5ccb04c1d653b1c829cb40568d553dc44f7a6180'),
        ('4.3', '044', '9338820630bf67373b44d8ea68409f65162ea7a47b9b29ace06a0aed12567f99'),
        ('4.3', '045', 'ba6ec3978e9eaa1eb3fabdaf3cc6fdf8c4606ac1c599faaeb4e2d69864150023'),
        ('4.3', '046', 'b3b456a6b690cd293353f17e22d92a202b3c8bce587ae5f2667c20c9ab6f688f'),
        ('4.3', '047', 'c69248de7e78ba6b92f118fe1ef47bc86479d5040fe0b1f908ace1c9e3c67c4a'),
        ('4.3', '048', '5b8215451c5d096ca1e115307ffe6613553551a70369525a0778f216c3a4dfa2'),
    ]

    # TODO: patches below are not managed by the GNUMirrorPackage base class
    for ver, num, checksum in patches:
        ver = Version(ver)
        patch('https://ftpmirror.gnu.org/bash/bash-{0}-patches/bash{1}-{2}'.format(ver, ver.joined, num),
              level=0, when='@{0}'.format(ver), sha256=checksum)

    # Modified from:
    # https://github.com/macports/macports-ports/blob/master/shells/bash/files/patch-configure.diff
    patch('patch-configure.diff', when='@:5.0 %apple-clang@12:')

    executables = ['^bash$']

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'GNU bash, version ([\d.]+)', output)
        return match.group(1) if match else None

    def configure_args(self):
        spec = self.spec

        return [
            # https://github.com/Homebrew/legacy-homebrew/pull/23234
            # https://trac.macports.org/ticket/40603
            'CFLAGS=-DSSH_SOURCE_BASHRC',
            'LIBS=' + spec['ncurses'].libs.link_flags,
            '--with-curses',
            '--enable-readline',
            '--with-installed-readline',
            '--with-libiconv-prefix={0}'.format(spec['iconv'].prefix),
        ]

    def check(self):
        make('tests')

    @property
    def install_targets(self):
        args = ['install']

        if self.spec.satisfies('@4.4:'):
            args.append('install-headers')

        return args
