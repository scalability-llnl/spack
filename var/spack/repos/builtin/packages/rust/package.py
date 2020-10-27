# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.util.rust import rust_archs, RustQuery

import inspect
from six import iteritems


class Rust(Package):
    """The Rust programming language toolchain

    This package can bootstrap any version of the Rust compiler since Rust
    1.23. It does this by downloading the platform-appropriate binary
    distribution of the desired version of the rust compiler, and then building
    that compiler from source.
    """

    homepage = "https://www.rust-lang.org"
    url = "https://static.rust-lang.org/dist/rustc-1.42.0-src.tar.gz"
    git = "https://github.com/rust-lang/rust.git"

    maintainers = ["AndrewGaspar"]

    phases = ['configure', 'install']

    extendable = True

    variant(
        'rustfmt',
        default=True,
        description='Formatting tool for Rust code'
    )

    variant(
        'analysis',
        default=True,
        description='Outputs code analysis that can be consumed by other tools'
    )

    variant(
        'clippy',
        default=True,
        description='Linting tool for Rust'
    )

    variant(
        'rls',
        default=False,
        description='The Rust Language Server can be used for IDE integration'
    )

    variant(
        'src',
        default=True,
        description='Install Rust source files'
    )
    variant(
        'extra_targets', default='none', multi=True,
        description='Triples for extra targets to enable. For supported targets, see: https://doc.rust-lang.org/nightly/rustc/platform-support.html'
    )

    depends_on('python@2.7:', type='build')
    depends_on('python@2.7:2.8', when='@:1.43', type='build')
    depends_on('gmake@3.81:', type='build')
    depends_on('cmake@3.4.3:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('openssl')
    depends_on('libssh2')
    depends_on('libgit2')

    # Pre-release Versions
    version('master', branch='master', submodules=True)

    # These version strings are officially supported, but aren't explicitly
    # listed because there's no stable checksum for them.
    # version('nightly')
    # version('beta')

    # Version Notes:
    # Here's some information on why your favorite Rust version may be missing.
    #
    # < 1.23:
    # Rust seems to eagerly search for ar next to cc. Spack makes wrappers for
    # cc and c++, but not for ar, so no ar is found. In future versions, ar
    # can be specified in the config.
    #
    # < 1.17:
    # The `x.py` bootstrapping script did not exist prior to Rust 1.17. It
    # would be possible to support both, but for simplicitly, we only support
    # Rust 1.17 and newer
    version('1.47.0', sha256='3185df064c4747f2c8b9bb8c4468edd58ff4ad6d07880c879ac1b173b768d81d')
    version('1.46.0', sha256='2d6a3b7196db474ba3f37b8f5d50a1ecedff00738d7846840605b42bfc922728')
    version('1.45.1', sha256='ea53e6424e3d1fe56c6d77a00e72c5d594b509ec920c5a779a7b8e1dbd74219b')
    version('1.44.1', sha256='7e2e64cb298dd5d5aea52eafe943ba0458fa82f2987fdcda1ff6f537b6f88473')
    version('1.44.0', sha256='bf2df62317e533e84167c5bc7d4351a99fdab1f9cd6e6ba09f51996ad8561100')
    version('1.43.1', sha256='cde177b4a8c687da96f20de27630a1eb55c9d146a15e4c900d5c31cd3c3ac41d')
    version('1.43.0', sha256='75f6ac6c9da9f897f4634d5a07be4084692f7ccc2d2bb89337be86cfc18453a1')
    version('1.42.0', sha256='d2e8f931d16a0539faaaacd801e0d92c58df190269014b2360c6ab2a90ee3475')
    version('1.41.1', sha256='38c93d016e6d3e083aa15e8f65511d3b4983072c0218a529f5ee94dd1de84573')
    version('1.41.0', sha256='5546822c09944c4d847968e9b7b3d0e299f143f307c00fa40e84a99fabf8d74b')
    version('1.40.0', sha256='dd97005578defc10a482bff3e4e728350d2099c60ffcf1f5e189540c39a549ad')
    version('1.39.0', sha256='b4a1f6b6a93931f270691aba4fc85eee032fecda973e6b9c774cd06857609357')
    version('1.38.0', sha256='644263ca7c7106f8ee8fcde6bb16910d246b30668a74be20b8c7e0e9f4a52d80')
    version('1.37.0', sha256='120e7020d065499cc6b28759ff04153bfdc2ac9b5adeb252331a4eb87cbe38c3')
    version('1.36.0', sha256='04c4e4d7213d036d6aaed392841496d272146312c0290f728b7400fccd15bb1b')
    version('1.35.0', sha256='5a4d637a716bac18d085f44dd87ef48b32195f71b967d872d80280b38cff712d')
    version('1.34.2', sha256='c69a4a85a1c464368597df8878cb9e1121aae93e215616d45ad7d23af3052f56')
    version('1.34.1', sha256='b0c785264d17e1dac4598627c248a2d5e07dd39b6666d1881fcfc8e2cf4c40a7')
    version('1.34.0', sha256='7ac85acffd79dd3a7c44305d9eaabd1f1e7116e2e6e11e770e4bf5f92c0f1f59')
    version('1.33.0', sha256='5a01a8d7e65126f6079042831385e77485fa5c014bf217e9f3e4aff36a485d94')
    version('1.32.0', sha256='4c594c7712a0e7e8eae6526c464bf6ea1d82f77b4f61717c3fc28fb27ba2224a')
    version('1.31.1', sha256='91d2fc22f08d986adab7a54eb3a6a9b99e490f677d2d092e5b9e4e069c23686a')
    version('1.30.1', sha256='36a38902dbd9a3e1240d46ab0f2ca40d2fd07c2ab6508ed7970c6c4c036b5b29')
    version('1.30.0', sha256='cd0ba83fcca55b64c0c9f23130fe731dfc1882b73ae21bef96be8f2362c108ee')
    version('1.29.2', sha256='5088e796aa2e47478cdf41e7243fc5443fafab0a7c70a11423e57c80c04167c9')
    version('1.29.1', sha256='f1b0728b66ce6bce6d72bbe5ea9e3a24ea22a045665da2ed8fcdfad14f61a349')
    version('1.29.0', sha256='a4eb34ffd47f76afe2abd813f398512d5a19ef00989d37306217c9c9ec2f61e9')
    version('1.28.0', sha256='1d5a81729c6f23a0a23b584dd249e35abe9c6f7569cee967cc42b1758ecd6486')
    version('1.27.2', sha256='9a818c50cdb7880abeaa68b3d97792711e6c64c1cdfb6efdc23f75b8ced0e15d')
    version('1.27.1', sha256='2133beb01ddc3aa09eebc769dd884533c6cfb08ce684f042497e097068d733d1')
    version('1.27.0', sha256='2cb9803f690349c9fd429564d909ddd4676c68dc48b670b8ddf797c2613e2d21')
    version('1.26.2', sha256='fb9ecf304488c9b56600ab20cfd1937482057f7e5db7899fddb86e0774548700')
    version('1.26.1', sha256='70a7961bd8ec43b2c01e9896e90b0a06804a7fbe0a5c05acc7fd6fed19500df0')
    version('1.26.0', sha256='4fb09bc4e233b71dcbe08a37a3f38cabc32219745ec6a628b18a55a1232281dd')
    version('1.25.0', sha256='eef63a0aeea5147930a366aee78cbde248bb6e5c6868801bdf34849152965d2d')
    version('1.24.1', sha256='3ea53d45e8d2e9a41afb3340cf54b9745f845b552d802d607707cf04450761ef')
    version('1.24.0', sha256='bb8276f6044e877e447f29f566e4bbf820fa51fea2f912d59b73233ffd95639f')
    version('1.23.0', sha256='7464953871dcfdfa8afcc536916a686dd156a83339d8ec4d5cb4eb2fe146cb91')

    # The Rust bootstrapping process requires a bootstrapping compiler. The
    # easiest way to do this is to download the binary distribution of the
    # same version of the compiler and build with that.
    #
    # This dictionary contains a version: hash dictionary for each supported
    # Rust target.
    rust_releases = {
        '1.47.0': {
            'x86_64-unknown-linux-gnu':      'd0e11e1756a072e8e246b05d54593402813d047d12e44df281fbabda91035d96',
            'powerpc64le-unknown-linux-gnu': '5760c3b1897ea70791320c2565f3eef700a3d54059027b84bbe6b8d6157f81c8',
            'aarch64-unknown-linux-gnu':     '753c905e89a714ab9bce6fe1397b721f29c0760c32f09d2f328af3d39919c8e6',
            'x86_64-apple-darwin':           '84e5be6c5c78734deba911dcf80316be1e4c7da2c59413124d039ad96620612f'
        },
        '1.46.0': {
            'x86_64-unknown-linux-gnu':      'e3b98bc3440fe92817881933f9564389eccb396f5f431f33d48b979fa2fbdcf5',
            'powerpc64le-unknown-linux-gnu': '89e2f4761d257f017a4b6aa427f36ac0603195546fa2cfded8c899789832941c',
            'aarch64-unknown-linux-gnu':     'f0c6d630f3dedb3db69d69ed9f833aa6b472363096f5164f1068c7001ca42aeb',
            'x86_64-apple-darwin':           '82d61582a3772932432a99789c3b3bd4abe6baca339e355048ca9efb9ea5b4db'
        },
        '1.45.1': {
            'x86_64-unknown-linux-gnu':      '76dc9f05b3bfd0465d6e6d22bc9fd5db0b473e3548e8b3d266ecfe4d9e5dca16',
            'powerpc64le-unknown-linux-gnu': '271846e4f5adc9a33754794c2ffab851f9e0313c8c1315264e7db5c8f63ab7ab',
            'aarch64-unknown-linux-gnu':     'd17fd560e8d5d12304835b71a7e22ac2c3babf4b9768db6a0e89868b4444f728',
            'x86_64-apple-darwin':           '7334c927e4d2d12d209bf941b97ba309e548413e241d2d263c39c6e12b3ce154'
        },
        '1.44.1': {
            'x86_64-unknown-linux-gnu':      'a41df89a461a580536aeb42755e43037556fba2e527dd13a1e1bb0749de28202',
            'powerpc64le-unknown-linux-gnu': '22deeca259459db31065af7c862fcab7fbfb623200520c65002ed2ba93d87ad2',
            'aarch64-unknown-linux-gnu':     'a2d74ebeec0b6778026b6c37814cdc91d14db3b0d8b6d69d036216f4d9cf7e49',
            'x86_64-apple-darwin':           'a5464e7bcbce9647607904a4afa8362382f1fc55d39e7bbaf4483ac00eb5d56a'
        },
        '1.44.0': {
            'x86_64-unknown-linux-gnu':      'eaa34271b4ac4d2c281831117d4d335eed0b37fe7a34477d9855a6f1d930a624',
            'powerpc64le-unknown-linux-gnu': '97038ea935c7a5b21f5aaaaad409c514e2b2ae8ea55994ba39645f453e98bc9f',
            'aarch64-unknown-linux-gnu':     'bcc916003cb9c7ff44f5f9af348020b422dbc5bd4fe49bdbda2de6ce0a1bb745',
            'x86_64-apple-darwin':           'f20388b80b2b0a8b122d89058f785a2cf3b14e93bcac53471d60fdb4106ffa35'
        },
        '1.43.1': {
            'x86_64-unknown-linux-gnu':      '25cd71b95bba0daef56bad8c943a87368c4185b90983f4412f46e3e2418c0505',
            'powerpc64le-unknown-linux-gnu': '1670f00b00cc1bed38d523a25dba7420de3c06986c15a0248e06299f80ce6124',
            'aarch64-unknown-linux-gnu':     'fbb612387a64c9da2869725afffc1f66a72d6e7ba6667ba717cd52c33080b7fb',
            'x86_64-apple-darwin':           'e1c3e1426a9e615079159d6b619319235e3ca7b395e7603330375bfffcbb7003'
        },
        '1.43.0': {
            'x86_64-unknown-linux-gnu':      '069f34fa5cef92551724c83c36360df1ac66fe3942bc1d0e4d341ce79611a029',
            'powerpc64le-unknown-linux-gnu': 'c75c7ae4c94715fd6cc43d1d6fdd0952bc151f7cbe3054f66d99a529d5bb996f',
            'aarch64-unknown-linux-gnu':     'e5fa55f333c10cdae43d147438a80ffb435d6c7b9681cd2e2f0857c024556856',
            'x86_64-apple-darwin':           '504e8efb2cbb36f5a3db7bb36f339a1e5216082c910ad19039c370505cfbde99'
        },
        '1.42.0': {
            'x86_64-unknown-linux-gnu':      '7d1e07ad9c8a33d8d039def7c0a131c5917aa3ea0af3d0cc399c6faf7b789052',
            'powerpc64le-unknown-linux-gnu': '805b08fa1e0aad4d706301ca1f13e2d80810d385cece2c15070360b3c4bd6e4a',
            'aarch64-unknown-linux-gnu':     'fdd39f856a062af265012861949ff6654e2b7103be034d046bec84ebe46e8d2d',
            'x86_64-apple-darwin':           'db1055c46e0d54b99da05e88c71fea21b3897e74a4f5ff9390e934f3f050c0a8'
        },
        '1.41.1': {
            'x86_64-unknown-linux-gnu':      'a6d5a3b3f574aafc8f787fea37aad9fb8a7946b383ae5348146927192ff0bef0',
            'powerpc64le-unknown-linux-gnu': 'f9b53ca636625b3a2dd87600b6274223c11f866c9b5a34b638ea0013186659d3',
            'aarch64-unknown-linux-gnu':     'd54c0f9165b86216b6f1b499f451141407939c5dc6b36c89a3772895a1370242',
            'x86_64-apple-darwin':           '16615288cf74239783de1b435d329f3d56ed13803c7c10cd4b207d7c8ffa8f67'
        },
        '1.41.0': {
            'x86_64-unknown-linux-gnu':      '343ba8ef7397eab7b3bb2382e5e4cb08835a87bff5c8074382c0b6930a41948b',
            'powerpc64le-unknown-linux-gnu': 'ba231b0d8273d6928f61e2be3456e816a1de8050135e20c0623dc7a6ea03ba68',
            'aarch64-unknown-linux-gnu':     '79ddfb5e2563d0ee09a567fbbe121a2aed3c3bc61255b2787f2dd42183a10f27',
            'x86_64-apple-darwin':           'b6504003ab70b11f278e0243a43ba9d6bf75e8ad6819b4058a2b6e3991cc8d7a'
        },
        '1.40.0': {
            'x86_64-unknown-linux-gnu':      'fc91f8b4bd18314e83a617f2389189fc7959146b7177b773370d62592d4b07d0',
            'powerpc64le-unknown-linux-gnu': 'b1a23e35c383f99e647df6a9239b1dc9313e293deb70a76ba58e8ebe55ef623b',
            'aarch64-unknown-linux-gnu':     '639271f59766d291ebdade6050e7d05d61cb5c822a3ef9a1e2ab185fed68d729',
            'x86_64-apple-darwin':           '749ca5e0b94550369cc998416b8854c13157f5d11d35e9b3276064b6766bcb83'
        },
        '1.39.0': {
            'x86_64-unknown-linux-gnu':      'b10a73e5ba90034fe51f0f02cb78f297ed3880deb7d3738aa09dc5a4d9704a25',
            'powerpc64le-unknown-linux-gnu': '53b3fd942c52709f7e6fe11ea572d086e315a57a40b84b9b3290ac0ec8c7c84a',
            'aarch64-unknown-linux-gnu':     'e27dc8112fe577012bd88f30e7c92dffd8c796478ce386c49465c03b6db8209f',
            'x86_64-apple-darwin':           '3736d49c5e9592844e1a5d5452883aeaf8f1e25d671c1bc8f01e81c1766603b5'
        },
        '1.38.0': {
            'x86_64-unknown-linux-gnu':      'adda26b3f0609dbfbdc2019da4a20101879b9db2134fae322a4e863a069ec221',
            'powerpc64le-unknown-linux-gnu': 'f9ed1bb6525abdd4dd6ef10782ad45d2f71496e0c3c88e806b510c81a91c4ff7',
            'aarch64-unknown-linux-gnu':     '06afd6d525326cea95c3aa658aaa8542eab26f44235565bb16913ac9d12b7bda',
            'x86_64-apple-darwin':           'bd301b78ddcd5d4553962b115e1dca5436dd3755ed323f86f4485769286a8a5a'
        },
        '1.37.0': {
            'x86_64-unknown-linux-gnu':      'cb573229bfd32928177c3835fdeb62d52da64806b844bc1095c6225b0665a1cb',
            'powerpc64le-unknown-linux-gnu': '27c59ec40e9e9f71490dc00bf165156ae3ea77c20ffa4b5e5fd712e67527b477',
            'aarch64-unknown-linux-gnu':     '263ef98fa3a6b2911b56f89c06615cdebf6ef676eb9b2493ad1539602f79b6ba',
            'x86_64-apple-darwin':           'b2310c97ffb964f253c4088c8d29865f876a49da2a45305493af5b5c7a3ca73d'
        },
        '1.36.0': {
            'x86_64-unknown-linux-gnu':      '15e592ec52f14a0586dcebc87a957e472c4544e07359314f6354e2b8bd284c55',
            'powerpc64le-unknown-linux-gnu': '654a7a18d881811c09f630b0c917825b586e94a6142eceaede6b8046718e4054',
            'aarch64-unknown-linux-gnu':     'db78c24d93756f9fe232f081dbc4a46d38f8eec98353a9e78b9b164f9628042d',
            'x86_64-apple-darwin':           '91f151ec7e24f5b0645948d439fc25172ec4012f0584dd16c3fb1acb709aa325'
        },
        '1.35.0': {
            'x86_64-unknown-linux-gnu':      'cf600e2273644d8629ed57559c70ca8db4023fd0156346facca9ab3ad3e8f86c',
            'powerpc64le-unknown-linux-gnu': 'a933955adec386d75d126e78df5b9941936e156acb3353fc44b85995a81c7bb2',
            'aarch64-unknown-linux-gnu':     '31e6da56e67838fd2874211ae896a433badf67c13a7b68481f1d5f7dedcc5952',
            'x86_64-apple-darwin':           'ac14b1c7dc330dcb53d8641d74ebf9b32aa8b03b9d650bcb9258030d8b10dbd6'
        },
        '1.34.2': {
            'x86_64-unknown-linux-gnu':      '2bf6622d980a52832bae141304e96f317c8a1ccd2dfd69a134a14033e6e43c0f',
            'powerpc64le-unknown-linux-gnu': '4ddd55014bbd954b3499859bfa3146bff471de21c1d73fc6e7cccde290fc1918',
            'aarch64-unknown-linux-gnu':     '15fc6b7ec121df9d4e42483dd12c677203680bec8c69b6f4f62e5a35a07341a8',
            'x86_64-apple-darwin':           '6fdd4bf7fe26dded0cd57b41ab5f0500a5a99b7bc770523a425e9e34f63d0fd8'
        },
        '1.34.1': {
            'x86_64-unknown-linux-gnu':      '8e2eead11bd5bf61409e29018d007c6fc874bcda2ff54db3d04d1691e779c14e',
            'powerpc64le-unknown-linux-gnu': '94ac92d08afcfa2d77ae207e91b57c00cb48ff7ba08a27ed3deb2493f33e8fb1',
            'aarch64-unknown-linux-gnu':     '0565e50dae58759a3a5287abd61b1a49dfc086c4d6acf2ce604fe1053f704e53',
            'x86_64-apple-darwin':           'f4e46b9994ccfab4a84059298d1dc8fd446b1bbb7449462e0459948f7debea0e'
        },
        '1.34.0': {
            'x86_64-unknown-linux-gnu':      '170647ed41b497dc937a6b2556700210bc4be187b1735029ef9ccf52e2cb5ab8',
            'powerpc64le-unknown-linux-gnu': '3027e87802e161cce6f3a23d961f6d73b9ed6e829b2cd7af5dfccf6e1207e552',
            'aarch64-unknown-linux-gnu':     '370c3a8fb9a69df36d645a95e622fb59ac5b513baecddde706cedaf20defa269',
            'x86_64-apple-darwin':           'e6bea8d865cc7341c17fa3b8f25f7989e6b04f53e9da24878addc524f3a32664'
        },
        '1.33.0': {
            'x86_64-unknown-linux-gnu':      '6623168b9ee9de79deb0d9274c577d741ea92003768660aca184e04fe774393f',
            'powerpc64le-unknown-linux-gnu': 'db885aa4c2c6896c85257be2ade5c9edea660ca6878970683e8d5796618329b5',
            'aarch64-unknown-linux-gnu':     'a308044e4076b62f637313ea803fa0a8f340b0f1b53136856f2c43afcabe5387',
            'x86_64-apple-darwin':           '864e7c074a0b88e38883c87c169513d072300bb52e1d320a067bd34cf14f66bd'
        },
        '1.32.0': {
            'x86_64-unknown-linux-gnu':      'e024698320d76b74daf0e6e71be3681a1e7923122e3ebd03673fcac3ecc23810',
            'powerpc64le-unknown-linux-gnu': 'd6d5c9154f4459465d68ebd4fa1e17bad4b6cfe219667dddd9123c3bfb5dd839',
            'aarch64-unknown-linux-gnu':     '60def40961728212da4b3a9767d5a2ddb748400e150a5f8a6d5aa0e1b8ba1cee',
            'x86_64-apple-darwin':           'f0dfba507192f9b5c330b5984ba71d57d434475f3d62bd44a39201e36fa76304'
        },
        '1.31.1': {
            'x86_64-unknown-linux-gnu':      'a64685535d0c457f49a8712a096a5c21564cd66fd2f7da739487f028192ebe3c',
            'powerpc64le-unknown-linux-gnu': 'a6f61b7a8a06a2b0a785391cc3e6bb8004aa72095eea80db1561039f5bb3e975',
            'aarch64-unknown-linux-gnu':     '29a7c6eb536fefd0ca459e48dfaea006aa8bff8a87aa82a9b7d483487033632a',
            'x86_64-apple-darwin':           '8398b1b303bdf0e7605d08b87070a514a4f588797c6fb3593718cb9cec233ad6'
        },
        '1.30.1': {
            'x86_64-unknown-linux-gnu':      'a01a493ed8946fc1c15f63e74fc53299b26ebf705938b4d04a388a746dfdbf9e',
            'powerpc64le-unknown-linux-gnu': 'a7d4806e6702bdbad5017eeddc62f7ff7eb2438b1b9c39cbc90c2b1207f8e65f',
            'aarch64-unknown-linux-gnu':     '6d87d81561285abd6c1987e07b60b2d723936f037c4b46eedcc12e8566fd3874',
            'x86_64-apple-darwin':           '3ba1704a7defe3d9a6f0c1f68792c084da83bcba85e936d597bac0c019914b94'
        },
        '1.30.0': {
            'x86_64-unknown-linux-gnu':      'f620e3125cc505c842150bd873c0603432b6cee984cdae8b226cf92c8aa1a80f',
            'powerpc64le-unknown-linux-gnu': '0b53e257dc3d9f3d75cd97be569d3bf456d2c0af57ed0bd5e7a437227d8f465a',
            'aarch64-unknown-linux-gnu':     '9690c7c50eba5a8461184ee4138b4c284bad31ccc4aa1f2ddeec58b253e6363e',
            'x86_64-apple-darwin':           '07008d90932712282bc599f1e9a226e97879c758dc1f935e6e2675e45694cc1b'
        },
        '1.29.2': {
            'x86_64-unknown-linux-gnu':      'e9809825c546969a9609ff94b2793c9107d7d9bed67d557ed9969e673137e8d8',
            'powerpc64le-unknown-linux-gnu': '344003b808c20424c4699c9452bd37cdee23857dd4aa125e67d1d6e4bc992091',
            'aarch64-unknown-linux-gnu':     'e11461015ca7106ef8ebf00859842bf4be518ee170226cb8eedaaa666946509f',
            'x86_64-apple-darwin':           '63f54e3013406b39fcb5b84bcf5e8ce85860d0b97a1e156700e467bf5fb5d5f2'
        },
        '1.29.1': {
            'x86_64-unknown-linux-gnu':      'b36998aea6d58525f25d89f1813b6bfd4cad6ff467e27bd11e761a20dde43745',
            'powerpc64le-unknown-linux-gnu': '26a6d652ade6b6a96e6af18e846701ee28f912233372dfe15432139252f88958',
            'aarch64-unknown-linux-gnu':     '2685224f67b2ef951e0e8b48829f786cbfed95e19448ba292ac33af719843dbe',
            'x86_64-apple-darwin':           '07b07fbd6fab2390e19550beb8008745a8626cc5e97b72dc659061c1c3b3d008'
        },
        '1.29.0': {
            'x86_64-unknown-linux-gnu':      '09f99986c17b1b6b1bfbc9dd8785e0e4693007c5feb67915395d115c1a3aea9d',
            'powerpc64le-unknown-linux-gnu': 'd6954f1da53f7b3618fba3284330d99b6142bb25d9febba6dbfedad59ca53329',
            'aarch64-unknown-linux-gnu':     '0ed3be0fd9f847afeb4e587fff61f6769ea61b53719d3ea999326284e8975b36',
            'x86_64-apple-darwin':           '28a0473637585742f6d80ccd8afd88b6b400e65d623c33cb892412759444da93'
        },
        '1.28.0': {
            'x86_64-unknown-linux-gnu':      '2a1390340db1d24a9498036884e6b2748e9b4b057fc5219694e298bdaa37b810',
            'powerpc64le-unknown-linux-gnu': '255818156ec1f795ed808a44b4fdb8019187d5ebb7f837ae8f55a1ca40862bb6',
            'aarch64-unknown-linux-gnu':     '9b6fbcee73070332c811c0ddff399fa31965bec62ef258656c0c90354f6231c1',
            'x86_64-apple-darwin':           '5d7a70ed4701fe9410041c1eea025c95cad97e5b3d8acc46426f9ac4f9f02393'
        },
        '1.27.2': {
            'x86_64-unknown-linux-gnu':      '5028a18e913ef3eb53e8d8119d2cc0594442725e055a9361012f8e26f754f2bf',
            'powerpc64le-unknown-linux-gnu': '11034d150e811d4903b09fd42f0cb76d467a6365a158101493405fff1054572f',
            'aarch64-unknown-linux-gnu':     'cf84da70269c0e50bb3cc3d248bae1ffcd70ee69dc5a4e3513b54fefc6685fb4',
            'x86_64-apple-darwin':           '30c5cc58759caa4efdf2ea7d8438633139c98bee3408beb29ceb26985f3f5f70'
        },
        '1.27.1': {
            'x86_64-unknown-linux-gnu':      '435778a837af764da2a7a7fb4d386b7b78516c7dfc732d892858e9a8a539989b',
            'powerpc64le-unknown-linux-gnu': 'a08e6b6fed3329fcd1220b2ee4cd7a311d99121cf780fb6e1c6353bfeddfb176',
            'aarch64-unknown-linux-gnu':     'd1146b240e6f628224c3a67e3aae2a57e6c25d544115e5ece9ce91861ec92b3a',
            'x86_64-apple-darwin':           '475be237962d6aef1038a2faada26fda1e0eaea5d71d6950229a027a9c2bfe08'
        },
        '1.27.0': {
            'x86_64-unknown-linux-gnu':      '235ad78e220b10a2d0267aea1e2c0f19ef5eaaff53ad6ff8b12c1d4370dec9a3',
            'powerpc64le-unknown-linux-gnu': '847774a751e848568215739d384e3baf4d6ec37d27fb3add7a8789208c213aff',
            'aarch64-unknown-linux-gnu':     'e74ebc33dc3fc19e501a677a87b619746efdba2901949a0319176352f556673a',
            'x86_64-apple-darwin':           'a1d48190992e01aac1a181bce490c80cb2c1421724b4ff0e2fb7e224a958ce0f'
        },
        '1.26.2': {
            'x86_64-unknown-linux-gnu':      'd2b4fb0c544874a73c463993bde122f031c34897bb1eeb653d2ba2b336db83e6',
            'powerpc64le-unknown-linux-gnu': 'ea045869074ae3617eeb51207ce183e6915784b9ed615ecb92ce082ddb86ec1f',
            'aarch64-unknown-linux-gnu':     '3dfad0dc9c795f7ee54c2099c9b7edf06b942adbbf02e9ed9e5d4b5e3f1f3759',
            'x86_64-apple-darwin':           'f193705d4c0572a358670dbacbf0ffadcd04b3989728b442f4680fa1e065fa72'
        },
        '1.26.1': {
            'x86_64-unknown-linux-gnu':      'b7e964bace1286696d511c287b945f3ece476ba77a231f0c31f1867dfa5080e0',
            'powerpc64le-unknown-linux-gnu': 'ad8b2f6dd8c5cca1251d65b75ed2120aae3c5375d2c8ed690259cf4a652d7d3c',
            'aarch64-unknown-linux-gnu':     'd4a369053c2dfd5f457de6853557dab563944579fa4bb55bc919bacf259bff6d',
            'x86_64-apple-darwin':           'ebf898b9fa7e2aafc53682a41f18af5ca6660ebe82dd78f28cd9799fe4dc189a'
        },
        '1.26.0': {
            'x86_64-unknown-linux-gnu':      '13691d7782577fc9f110924b26603ade1990de0b691a3ce2dc324b4a72a64a68',
            'powerpc64le-unknown-linux-gnu': '3ba3a4905730ec01007ca1096d9fc3780f4e81f71139a619e1f526244301b7f4',
            'aarch64-unknown-linux-gnu':     'e12dc84bdb569cdb382268a5fe6ae6a8e2e53810cb890ec3a7133c20ba8451ac',
            'x86_64-apple-darwin':           '38708803c3096b8f101d1919ee2d7e723b0adf1bc1bb986b060973b57d8c7c28'
        },
        '1.25.0': {
            'x86_64-unknown-linux-gnu':      '06fb45fb871330a2d1b32a27badfe9085847fe824c189ddc5204acbe27664f5e',
            'powerpc64le-unknown-linux-gnu': '79eeb2a7fafa2e0f65f29a1dc360df69daa725347e4b6a533684f1c07308cc6e',
            'aarch64-unknown-linux-gnu':     '19a43451439e515a216d0a885d14203f9a92502ee958abf86bf7000a7d73d73d',
            'x86_64-apple-darwin':           'fcd0302b15e857ba4a80873360cf5453275973c64fa82e33bfbed02d88d0ad17'
        },
        '1.24.1': {
            'x86_64-unknown-linux-gnu':      '4567e7f6e5e0be96e9a5a7f5149b5452828ab6a386099caca7931544f45d5327',
            'powerpc64le-unknown-linux-gnu': '6f6c4bebbd7d6dc9989bf372c512dea55af8f56a1a0cfe97784667f0ac5430ee',
            'aarch64-unknown-linux-gnu':     '64bb25a9689b18ddadf025b90d9bdb150b809ebfb74432dc69cc2e46120adbb2',
            'x86_64-apple-darwin':           '9d4aacdb5849977ea619d399903c9378163bd9c76ea11dac5ef6eca27849f501'
        },
        '1.24.0': {
            'x86_64-unknown-linux-gnu':      '336cf7af6c857cdaa110e1425719fa3a1652351098dc73f156e5bf02ed86443c',
            'powerpc64le-unknown-linux-gnu': '25d9b965a63ad2f345897028094d4c7eafa432237b478754ccbcc299f80629c8',
            'aarch64-unknown-linux-gnu':     'a981de306164b47f3d433c1d53936185260642849c79963af7e07d36b063a557',
            'x86_64-apple-darwin':           '1aecba7cab4bc1a9e0e931c04aa00849e930b567d243da7b676ede8f527a2992'
        },
        '1.23.0': {
            'x86_64-unknown-linux-gnu':      '9a34b23a82d7f3c91637e10ceefb424539dcfa327c2dcd292ff10c047b1fdc7e',
            'powerpc64le-unknown-linux-gnu': '60f1a1cc182c516de08c1f42ada01604a3d94383e9dded6b237ae2233999437b',
            'aarch64-unknown-linux-gnu':     '38379fbd976d2286cb73f21466db40a636a583b9f8a80af5eea73617c7912bc7',
            'x86_64-apple-darwin':           '9274e977322bb4b153f092255ac9bd85041142c73eaabf900cb2ef3d3abb2eba'
        }
    }

    # Specifies the strings which represent a pre-release Rust version. These
    # always bootstrap with the latest beta release.
    #
    # NOTE: These are moving targets, and therefore have no stable checksum. Be
    # sure to specify "-n" or "--no-checksum" when installing these versions.
    rust_prerelease_versions = ["beta", "nightly", "master"]

    for prerelease_version in rust_prerelease_versions:
        for rust_target, rust_arch_list in iteritems(rust_archs):
            for rust_arch in rust_arch_list:
                # All pre-release builds are built with the latest beta
                # compiler.
                resource(
                    name='rust-beta-{target}'.format(
                        target=rust_target
                    ),
                    url='https://static.rust-lang.org/dist/rust-beta-{target}.tar.gz'.format(
                        target=rust_target
                    ),
                    # Fake SHA - checksums should never be checked for
                    # pre-release builds, anyway
                    sha256='0000000000000000000000000000000000000000000000000000000000000000',
                    destination='spack_bootstrap_stage',
                    when='@{version} platform={platform} target={target}'\
                    .format(
                        version=prerelease_version,
                        platform=rust_arch['platform'],
                        target=rust_arch['target']
                    )
                )

    # This loop generates resources for each binary distribution, and maps
    # them to the version of the compiler they bootstrap. This is in place
    # of listing each resource explicitly, which would be potentially even
    # more verbose.
    #
    # NOTE: This loop should technically specify the architecture to be the
    # _host_ architecture, not the target architecture, in order to support
    # cross compiling. I'm not sure Spack provides a way to specify a
    # distinction in the when clause, though.
    for rust_version, rust_targets in iteritems(rust_releases):
        for rust_target, rust_sha256 in iteritems(rust_targets):
            for rust_arch in rust_archs[rust_target]:
                resource(
                    name='rust-{version}-{target}'.format(
                        version=rust_version,
                        target=rust_target
                    ),
                    url='https://static.rust-lang.org/dist/rust-{version}-{target}.tar.gz'.format(
                        version=rust_version,
                        target=rust_target
                    ),
                    sha256=rust_sha256,
                    destination='spack_bootstrap_stage',
                    when='@{version} platform={platform} target={target}'\
                    .format(
                        version=rust_version,
                        platform=rust_arch['platform'],
                        target=rust_arch['target']
                    )
                )

    # This routine returns the target architecture we intend to build for.
    def get_rust_target(self):
        if 'platform=linux' in self.spec or 'platform=cray' in self.spec:
            if 'target=x86_64:' in self.spec:
                return 'x86_64-unknown-linux-gnu'
            elif 'target=ppc64le:' in self.spec:
                return 'powerpc64le-unknown-linux-gnu'
            elif 'target=aarch64:' in self.spec:
                return 'aarch64-unknown-linux-gnu'
        elif 'platform=darwin target=x86_64:' in self.spec:
            return 'x86_64-apple-darwin'

        raise InstallError(
            "rust is not supported for '{0}'".format(
                self.spec.architecture
            ))

    def check_newer(self, version):
        if '@master' in self.spec or '@beta' in self.spec or \
           '@nightly' in self.spec:
            return True

        return '@{0}:'.format(version) in self.spec

    def configure(self, spec, prefix):
        target = self.get_rust_target()

        # Bootstrapping compiler selection:
        # Pre-release compilers use the latest beta release for the
        # bootstrapping compiler.
        # Versioned releases bootstrap themselves.
        if '@beta' in spec or '@nightly' in spec or '@master' in spec:
            bootstrap_version = 'beta'
        else:
            bootstrap_version = spec.version
        # See the NOTE above the resource loop - should be host architecture,
        # not target aarchitecture if we're to support cross-compiling.
        bootstrapping_install = Executable(
            './spack_bootstrap_stage/rust-{version}-{target}/install.sh'
            .format(
                version=bootstrap_version,
                target=target
            )
        )
        # install into the staging area
        bootstrapping_install('--prefix={0}'.format(
            join_path(self.stage.source_path, 'spack_bootstrap')
        ))

        boot_bin = join_path(self.stage.source_path, 'spack_bootstrap/bin')

        # Always build rustc and cargo
        tools = ['rustc', 'cargo']
        # Only make additional components available in 'rust-bootstrap'
        if '+rustfmt' in self.spec:
            tools.append('rustfmt')
        if '+analysis' in self.spec:
            tools.append('analysis')
        if '@1.33: +clippy' in self.spec:
            tools.append('clippy')
        if '+rls' in self.spec:
            tools.append('rls')
        if '+src' in self.spec:
            tools.append('src')

        ar = which('ar', required=True)

        extra_targets = []
        if self.spec.variants['extra_targets'].value != ('none',):
            extra_targets = list(self.spec.variants['extra_targets'].value)

        targets = [self.get_rust_target()] + extra_targets
        target_spec = 'target=[' + \
            ','.join('"{0}"'.format(target) for target in targets) + ']'
        target_specs = '\n'.join(
            '[target.{0}]\nar = "{1}"\n'.format(target, ar.path)
            for target in targets)

        # build.tools was introduced in Rust 1.25
        tools_spec = \
            'tools={0}'.format(tools) if self.check_newer('1.25') else ''
        # This is a temporary fix due to rust 1.42 breaking self bootstrapping
        # See: https://github.com/rust-lang/rust/issues/69953
        #
        # In general, this should be safe because bootstrapping typically
        # ensures everything but the bootstrapping script is warning free for
        # the latest set of warning.
        deny_warnings_spec = \
            'deny-warnings = false' if '@1.42.0' in self.spec else ''

        # "Nightly" and master builds want a path to rustfmt - otherwise, it
        # will try to download rustfmt from the Internet. We'll give it rustfmt
        # for the bootstrapping compiler, but it ultimately shouldn't matter
        # because this package never invokes it. To be clear, rustfmt from the
        # bootstrapping compiler is probably incorrect. See: src/stage0.txt in
        # Rust to see what the current "official" rustfmt version for Rust is.
        if '@master' in spec or '@nightly' in spec:
            rustfmt_spec = \
                'rustfmt="{0}"'.format(join_path(boot_bin, 'rustfmt'))
        else:
            rustfmt_spec = ''

        with open('config.toml', 'w') as out_file:
            out_file.write("""\
[build]
cargo = "{cargo}"
rustc = "{rustc}"
docs = false
vendor = true
extended = true
verbose = 2
{target_spec}
{tools_spec}
{rustfmt_spec}

[rust]
channel = "stable"
rpath = true
{deny_warnings_spec}

{target_specs}

[install]
prefix = "{prefix}"
sysconfdir = "etc"
""".format(
                cargo=join_path(boot_bin, 'cargo'),
                rustc=join_path(boot_bin, 'rustc'),
                prefix=prefix,
                deny_warnings_spec=deny_warnings_spec,
                target_spec=target_spec,
                target_specs=target_specs,
                tools_spec=tools_spec,
                rustfmt_spec=rustfmt_spec
            )
            )

    def install(self, spec, prefix):
        jobs = inspect.getmodule(self).make_jobs

        rustflags = []

        target_cpu = \
            RustQuery(
                Executable(
                    join_path(
                        self.stage.source_path,
                        'spack_bootstrap/bin/rustc'
                    )
                )
            ).target_cpu(self.spec)

        if target_cpu:
            rustflags.extend(["-C", "target-cpu={0}".format(target_cpu)])

        python('./x.py', 'install', '-j', str(jobs), extra_env={
            # vendored libgit2 wasn't correctly building (couldn't find the
            # vendored libssh2), so let's just have spack build it
            'LIBSSH2_SYS_USE_PKG_CONFIG': '1',
            'LIBGIT2_SYS_USE_PKG_CONFIG': '1',
            'RUSTFLAGS': " ".join(rustflags)
        })

    def setup_dependent_package(self, module, dependent_spec):
        """Called before cargo modules' build() methods."""

        module.cargo = Executable(join_path(self.prefix.bin, 'cargo'))
        module.cargo.add_default_arg('--locked')
        module.cargo.add_default_arg('--offline')
