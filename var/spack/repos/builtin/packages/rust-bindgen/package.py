# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RustBindgen(CargoPackage):
    """bindgen automatically generates Rust FFI bindings to C (and some C++)
    libraries."""

    homepage = "https://rust-lang.github.io/rust-bindgen/"
    crates_io = "bindgen"
    git = "https://github.com/rust-lang/rust-bindgen.git"

    maintainers = ['AndrewGaspar']

    depends_on('llvm@6.0:', type=('build', 'run'))

    version('master', branch='master')
    version('0.53.2', sha256='6bb26d6a69a335b8cb0e7c7e9775cd5666611dc50a37177c3f2cedcfc040e8c8')
    version('0.53.1', sha256='99de13bb6361e01e493b3db7928085dcc474b7ba4f5481818e53a89d76b8393f')
    version('0.53.0', sha256='4cb4969a64504090d6de8522f7f02b5f88e0f0ae4ab193b24a94b0ee954d5a06')
    version('0.52.0', sha256='f1c85344eb535a31b62f0af37be84441ba9e7f0f4111eb0530f43d15e513fe57')
    version('0.51.1-oldsyn', sha256='ae8266cdd336dfd53d71a95c33251232f64553b8770ebd85158039b3a734244b')
    version('0.51.1', sha256='ebd71393f1ec0509b553aa012b9b58e81dadbdff7130bd3b8cba576e69b32f75')
    version('0.51.0', sha256='18270cdd7065ec045a6bb4bdcd5144d14a78b3aedb3bc5111e688773ac8b9ad0')
    version('0.50.1', sha256='cb0e5a5f74b2bafe0b39379f616b5975e08bcaca4e779c078d5c31324147e9ba')
    version('0.50.0', sha256='65a913de3fa2fa95f2c593bb7e33b1be1ce1ce8a83f34b6bb02e6f01400b96cc')
    version('0.49.4', sha256='4c07087f3d5731bf3fb375a81841b99597e25dc11bd3bc72d16d43adf6624a6e')
    version('0.49.2', sha256='846a1fba6535362a01487ef6b10f0275faa12e5c5d835c5c1c627aabc46ccbd6')
    version('0.49.1', sha256='6bd7710ac8399ae1ebe1e3aac7c9047c4f39f2c94b33c997f482f49e96991f7c')
    version('0.49.0', sha256='33e1b67a27bca31fd12a683b2a3618e275311117f48cfcc892e18403ff889026')
    version('0.48.1', sha256='9d3d411fd93fd296e613bdac1d16755a6a922a4738e1c8f6a5e13542c905f3ca')
    version('0.48.0', sha256='19fca463d0927d64463fefd492baf4a57c3c2d7ec15c53ac87648fc141d26913')
    version('0.47.3', sha256='df683a55b54b41d5ea8ebfaebb5aa7e6b84e3f3006a78f010dadc9ca88469260')
    version('0.47.2', sha256='2162f593f5f3636eb727875b3fb93a4448dd41f84de5f228c9f4c9f5fc873270')
    version('0.47.1', sha256='91f5aa1a54c5997396b59cfac31af9c1cbcaa988958c4ce84364257b2cadfad0')
    version('0.47.0', sha256='e0b63e59b7fc083dffe1b508aad0bd43cc9df5f3e1bf5490054a405391d96982')
    version('0.46.0', sha256='8f7f7f0701772b17de73e4f5cbcb1dd6926f4706cba4c1ab62c5367f8bdc94e1')
    version('0.45.0', sha256='e144fcd207ac9c7325d2c012050e7d8839634defe1a3e8d303124ed0a77c6bea')
    version('0.44.0', sha256='d8de1946c252145e09ed00ea90a8685fce15b8f94bb4dc1a0daaf2a9b375be61')
    version('0.43.2', sha256='6d52d263eacd15d26cbcf215d254b410bd58212aaa2d3c453a04b2d3b3adcf41')
    version('0.43.1', sha256='49a944a85a9f2a49c602cad1e87cebe90963190d8a3c12101f608300f2210f2f')
    version('0.43.0', sha256='b41df015ccbc22b038641bd84d0aeeff01e0a4c0714ed35ed0e9a3dd8ad8d732')
    version('0.42.3', sha256='e0f199ccbabf5e9f9e13a3096534e80c9ce37aee440789dafaa47190e283245c')
    version('0.42.2', sha256='751b358f96b5108a3325b921806aaf067b048734d3234d01ca906636f670b630')
    version('0.42.1', sha256='14484e10ac96069b4dd7705141350804ccbe676fe275ed51088441ca616bc575')
    version('0.42.0', sha256='7eccf097969d4fd652335376d5bf632e2980b0e847401a5a6e2baaf99dd7fd10')
    version('0.41.0', sha256='e64eeb92e16bd21d6c95738458f80b2c95bad56cc8eeef7fdfaaf70268c56fe3')
    version('0.40.0', sha256='8f4c4ffe91e0f26bdcc5a8dd58cbf0358ad772b8ec1ae274a11a0ba54ec175f4')
    version('0.39.0', sha256='eac4ed5f2de9efc3c87cb722468fa49d0763e98f999d539bfc5e452c13d85c91')
    version('0.38.0', sha256='27f1b60c5c6cd7eb6a664b5fdde58dbfc1e6a8497118836211a85b9a56fafe2d')
    version('0.37.4', sha256='1b25ab82877ea8fe6ce1ce1f8ac54361f0218bad900af9eb11803994bf67c221')
    version('0.37.3', sha256='a847bea78e36c3d5d99ca99cac82a24d56e5f2105e402f3941a190bf92146579')
    version('0.37.0', sha256='429d032f8d65efdf12b2b799c84e339de7fe8e173e539911863887a935d202e9')
    version('0.36.1', sha256='acc8fa644dc2b6f6c2d391ccea460da1ad9bf2271c4e9ffaad88d2dd727a7295')
    version('0.36.0', sha256='cc7003ec1f7f5579901b5805f401a0defa450b14497c3cba4fbc0496f85ba429')
    version('0.35.0', sha256='b023955126e7909ab9fc1d1973965b8b004f1f388afb5c589640ab483b3b0ad2')
    version('0.33.2', sha256='603ed8d8392ace9581e834e26bd09799bf1e989a79bd1aedbb893e72962bdc6e')
    version('0.33.1', sha256='1657d607dd7a8e10b3181149f60f3b27ea0eac81058c09a1c791b8f6ead91f19')
    version('0.33.0', sha256='0333cac869708a8bd43e9620edb3bf587567c71111c480dc24675c078cb3ba3b')
    version('0.32.3', sha256='8b242e11a8f446f5fc7b76b37e81d737cabca562a927bd33766dac55b5f1177f')
    version('0.32.2', sha256='6ed9557522980fcdb4986097c2ea9d2504eafa7e5818f393110205b5325a52ce')
    version('0.32.1', sha256='6e0e57fd015c86d16b28d6409995045124a07665f36b38ca1992b1caf882fde6')
    version('0.32.0', sha256='65efe03fbddd7a7c6e959df4c13e564aa37041f9b48d8938adc18478b181a267')
    version('0.31.3', sha256='57253399c086f4f29e57ffd3b5cdbc23a806a00292619351aa4cfa39cb49d4ea')
    version('0.31.2', sha256='03c4e953809a480741ffbd58d8d241bb8b21ada7847f5ce3dd9b9af4e097d37d')
    version('0.31.1', sha256='bf1fb3a1a76b7ecabffe97f15ee6c9aa1772f464908911c58ea2682cca79e7a8')
    version('0.31.0', sha256='1dc6e0375c88727cabb08cc65b421de906e9735537e8233727b295b88762ef97')
    version('0.30.0', sha256='33024f55a754d920637461adf87fb485702a69bdf7ac1d307b7e18da93bae505')
    version('0.29.1', sha256='ba610cba0c1727ed837316540068b51349b8268c073906067b7c3948598929bd')
    version('0.29.0', sha256='0c338079dafc81bef7d581f494b906603d12359c4306979eae6ca081925a4984')
    version('0.28.0', sha256='16a8070d69d86935d11b0778dbdbc83a0a799d982e521baa62d0812b727734be')
    version('0.26.3', sha256='c57d6c0f6e31f8dcf4d12720a3c2a9ffb70638772a5784976cf4fce52145f22a')
    version('0.26.2', sha256='ac098a1ae2e8d2ba24f61d8a771c53c5135965709c46b76ccf06cf42b95313e6')
    version('0.26.1', sha256='04488a91af8f15eec4d88eb59e2c4e982c03ff31582acf2f5623e2e6d8ae9e0b')
    version('0.26.0', sha256='8365681d0e2d7804e235e251bba2c55c9693ed8fee9c873231dfca3e730d57ce')
    version('0.25.5', sha256='cc7973dbc2990511877ad9e5e50a312f02fbbc9b356c30bb102307424fa73630')
    version('0.25.4', sha256='823896c0be9d01f45ad67d3120e5f56248d4cbc667969dd05bc0212f096939a6')
    version('0.25.3', sha256='2e28791695e6e29a82038bd0489a760f362157dc1a3b2bbac9b6be3ddd984ff7')
    version('0.25.2', sha256='40ff59df105083f9fbce1218e957ada39ebf595ae1204bc0ec9a8692c2e5a7aa')
    version('0.25.1', sha256='708a688675f9d2e7c73018e17f5997beacc9a5ca87a0cb60c13093915facda32')
    version('0.25.0', sha256='ccaf8958532d7e570e905266ee2dc1094c3e5c3c3cfc2c299368747a30a5e654')
    version('0.24.0', sha256='21a1de90068c1e58dd31b71daab70e1a1e54212b43cc6c4714e7c8acefb28992')
    version('0.23.1', sha256='a1c9555b6fec94761d3e6a9c633745949fbda8d355a783cedf9f4b8e6a0c8c77')
    version('0.23.0', sha256='a873e994bac5056462430f7ba1db28dcad6086d68d63f3fdd76154e961963510')
    version('0.22.1', sha256='88f9d9abd7964621201c558021ff4f39b7b4d571a9a56a88844da9971e2344ce')
    version('0.22.0', sha256='facc480c409c373db3c870e377ce223e5e07d979efc2604691dc6f583e8ded0f')
    version('0.21.2', sha256='9cee948f9ad10626c930b6f8651d53534c00dbb1243c36cf99576be2554f332b')
    version('0.21.1', sha256='cba697ecbf51e4a1d1d84c6dee5339d22a5f9f5e04694e53e873ea26257a73f2')
    version('0.21.0', sha256='a241672a338c62a9b82d0650e2f5c39df69843df872358506ffb04f35aba3bf6')
    version('0.20.5', sha256='e3dc42e1889c6b5b78c5c5b000e4855f7c996d3e54bde789fa96d58c4b5aed13')
    version('0.20.4', sha256='a4acbca02456eaa2e3f586536c14bfeb2c4a45da329305a13c11853ed8ed3e2b')
    version('0.20.3', sha256='8d41dc1ba26eecde8c7028169778615716a81258829352ccd398d6a09f40cbe6')
    version('0.20.2', sha256='712c11d1fc3d402340a8b3c1548b3a7b62774f128ea9abf9e8dca3d08a32bf76')
    version('0.20.1', sha256='589db39348732112d392d08cb52153ad415762a895469fdc10cbaa0a8ade8198')
    version('0.20.0', sha256='145f3e7f8d75b288254e4a5b2b794243c4d8234891811e7cbb2b032cab06c337')
    version('0.19.2', sha256='003f95e0fb6cf3d1fee8c62b2ec35135509477989fab15c358e0efa3972bdef6')
    version('0.19.1', sha256='3bb3928f5b6694e40942ad191fc7e23052d0df5d2fe0600f582ac2e766e817f4')
    version('0.19.0', sha256='29fd83732ffd8c70521defec44c45ea61948e4fc9d66785430fb757d03760704')
    version('0.18.0', sha256='d91f4c64f47a76ee516bb546fd5ec4b310784d594e80c19cafb2a10afc9c502b')
    version('0.17.0', sha256='51cef5292215c1d051e7e44a3da845160c2a364b64157e92ce07a35c800c35f6')
    version('0.16.0', sha256='2aaf4e25abdf4db6aa2ed9f3f35f10ef1218072cd92f86662902d4a9eb2364b1')
    version('0.15.0', sha256='b79cad593c9c821593607afe00617e5c1f001f1485c4d43b942cd2879bf93c0c')
    version('0.14.0', sha256='a476e8be29811cab3ff7c4b818c7943b9ff302dc312e5fc4b23b4020c2dde9d1')
    version('0.0.2',  sha256='b0ebcf96a386d8cfb38502abfc16325715d9a32d5916ff3121dd1698e23a4021')

    # rust-bindgen has a dependency on libclang - add path
    def setup_build_environment(self, env):
        env.append_flags(
            'LLVM_CONFIG_PATH',
            join_path(self.spec['llvm'].prefix.bin, 'llvm-config'))
