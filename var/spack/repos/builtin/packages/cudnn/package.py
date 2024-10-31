# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform

from spack.package import *

_versions = {
    # cuDNN 9.2.0
    "9.2.0.82-12": {
        "Linux-x86_64": "1362b4d437e37e92c9814c3b4065db5106c2e03268e22275a5869e968cee7aa8",
        "Linux-aarch64": "24cc2a0308dfe412c02c7d41d4b07ec12dacb021ebf8c719de38eb77d22f68c1",
    },
    "9.2.0.82-11": {
        "Linux-x86_64": "99dcb3fa2bf7eed7f35b0f8e58e7d1f04d9a52e01e382efc1de16fed230d3b26"
    },
    # cuDNN 8.9.7
    "8.9.7.29-12": {
        "Linux-x86_64": "475333625c7e42a7af3ca0b2f7506a106e30c93b1aa0081cd9c13efb6e21e3bb",
        "Linux-ppc64le": "8574d291b299f9cc0134304473c9933bd098cc717e8d0876f4aba9f9eebe1b76",
    },
    "8.9.7.29-11": {
        "Linux-x86_64": "a3e2509028cecda0117ce5a0f42106346e82e86d390f4bb9475afc976c77402e",
        "Linux-ppc64le": "f23fd7d59f9d4f743fa926f317dab0d37f6ea21edb2726ceb607bea45b0f9f36",
    },
    # cuDNN 8.9.5
    "8.9.5.30-12": {
        "Linux-x86_64": "2a2eb89a2ab51071151c6082f1e816c702167a711a9372f9f73a7b5c4b06e01a",
        "Linux-ppc64le": "38388ec3c99c6646aaf5c707985cd35e25c67f653d780c4081c2df5557ab665f",
        "Linux-aarch64": "0491f7b02f55c22077eb678bf314c1f917524bd507cf5b658239bf98a47233a1",
    },
    "8.9.5.30-11": {
        "Linux-x86_64": "bbe10e3c08cd7e4aea1012213781e4fe270e1c908263444f567cafefb2cc6525",
        "Linux-ppc64le": "d678f8b2903b95de7eeaef38890c5674705864ea049b2b63e90565f2c0ea682f",
    },
    # cuDNN 8.9.0
    "8.9.0.131-12": {
        "Linux-x86_64": "477631002be61022b60961cba0a501271507a93f81d6b08384bc320cb8706c98",
        "Linux-ppc64le": "ff239e4cbbf21fa18104b62a887686e2197f820ad58817d62e509c735a331829",
        "Linux-aarch64": "fab70f4fb3b933ff502200a1d954d2c6fc205ff9c9b1d271ea4c41e980a66596",
    },
    "8.9.0.131-11": {
        "Linux-x86_64": "3cb82c50723f14b41d43523f222cd52cc9d50b3ad67c380f4be51bd1133daa2d",
        "Linux-ppc64le": "18778de490550c5b584e96560208e5e37678397037946e10a1c2824174c69725",
    },
    # cuDNN 8.8.1
    "8.8.1.3-12": {
        "Linux-x86_64": "79d77a769c7e7175abc7b5c2ed5c494148c0618a864138722c887f95c623777c",
        "Linux-ppc64le": "b0e89021a846952cad8cfc674edce2883f6e344ebd47a2394f706b1136715bc7",
    },
    "8.8.1.3-11": {
        "Linux-x86_64": "af7584cae0cc5524b5913ef08c29ba6154113c60eb0a37a0590a91b515a8a8f9",
        "Linux-ppc64le": "d086003d09d5388aa42142f07483a773aa74b602478b0933e24fc63f56f1658f",
    },
    # cuDNN 8.7.0
    "8.7.0.84-11.8": {
        "Linux-x86_64": "976c4cba7233c97ae74006afab5172976300ba40f5b250a21f8cf71f59c9f76d",
        "Linux-ppc64le": "0433d6d8b6841298e049e8a542750aa330a6e046a52ad95fae0c2f75dabe5575",
        "Linux-aarch64": "cf967f78dbf6c075243cc83aa18759e370db3754aa15b12a0a14e8bf67a3a9d4",
    },
    # cuDNN 8.6.0
    "8.6.0.163-11.8": {
        "Linux-x86_64": "bbc396df47294c657edc09c600674d608cb1bfc80b82dcf4547060c21711159e",
        "Linux-ppc64le": "c8a25e7e3df1bb9c4e18a4f24dd5f25cfd4bbe8b7054e34008e53b2be4f58a80",
        "Linux-aarch64": "a0202278d3cbd4f3adc3f7816bff6071621cb042b0903698b477acac8928ac06",
    },
    # cuDNN 8.5.0
    "8.5.0.96-11.7": {
        "Linux-x86_64": "5454a6fd94f008728caae9adad993c4e85ef36302e26bce43bea7d458a5e7b6d",
        "Linux-ppc64le": "00373c3d5e0b536a5557d0d0eb50706777f213a222b4030e1b71b1bec43d205f",
        "Linux-aarch64": "86780abbecd4634e7363fad1d000ae23b7905a5f8383bddbf7332c6934791dde",
    },
    # cuDNN 8.4.0
    "8.4.0.27-11.6": {
        "Linux-x86_64": "d19bdafd9800c79d29e6f6fffa9f9e2c10d1132d6c2ff10b1593e057e74dd050",
        "Linux-ppc64le": "7ef72353331cf42b357f53cb4a4971fb07e2f0b2ae66e03d54933df52de411c8",
        "Linux-aarch64": "3972ab37b6f0271274931f69c5675c3b61d16f8f5a2dedd422a5efd7b0f358e5",
    },
    "8.4.0.27-10.2": {
        "Linux-x86_64": "14c5e3ca4258271996d1fd959c42d17c582ce4d9aff451f84524469e784fd154"
    },
    # cuDNN 8.3.3
    "8.3.3.40-11.5": {
        "Linux-x86_64": "eabe96c75cf03ea4f5379894d914f1f8ae14ceab121989e84b0836d927fb7731",
        "Linux-ppc64le": "eaedc8dea675767f9445c11d96e6b472110d2fed728db4179153ca7da6503083",
        "Linux-aarch64": "83b1d21b0f6495dfdc2316e6d53489db8ab1b752e4e4d21caca0a08fb2136cdc",
    },
    "8.3.3.40-10.2": {
        "Linux-x86_64": "d8554f2b32e6295d5fc8f3ac25e68f94058b018c801dab9c143e36812f8926ab"
    },
    # cuDNN 8.3.2
    "8.3.2.44-11.5": {
        "Linux-x86_64": "5500953c08c5e5d1dddcfda234f9efbddcdbe43a53b26dc0a82c723fa170c457",
        "Linux-ppc64le": "0581bce48023a3ee71c3a819aaefcabe693eca18b61e2521dc5f8e6e71567b1b",
        "Linux-aarch64": "7eb8c96bfeec98e8aa7cea1e95633d2a9481fc99040eb0311d31bf137a7aa6ea",
    },
    # cuDNN 8.3.1
    "8.3.1.22-11.5": {
        "Linux-x86_64": "f5ff3c69b6a8a9454289b42eca1dd41c3527f70fcf49428eb80502bcf6b02f6e",
        "Linux-ppc64le": "1d2419a20ee193dc6a3a0ba87e79f408286d3d317c9831cbc1f0b7a268c100b0",
        "Linux-aarch64": "ff23a881366c0ee79b973a8921c6dd400628a321557550ad4e0a26a21caad263",
    },
    # cuDNN 8.2.4
    "8.2.4.15-11.4": {
        "Linux-x86_64": "0e5d2df890b9967efa6619da421310d97323565a79f05a1a8cb9b7165baad0d7",
        "Linux-ppc64le": "af8749ca83fd6bba117c8bee31b787b7f204946e864294030ee0091eb7d3577e",
        "Linux-aarch64": "48b11f19e9cd3414ec3c6c357ad228aebbd43282aae372d42cab2af67c32a08b",
    },
    # cuDNN 8.2.0
    "8.2.0.53-11.3": {
        "Linux-x86_64": "7a195dc93a7cda2bdd4d9b73958d259c784be422cd941a9a625aab75309f19dc",
        "Linux-ppc64le": "cfe06735671a41a5e25fc7542d740177ac8eab1ab146bd30f19e0fa836895611",
        "Linux-aarch64": "0f44af94eef7826dc7b41f92aade3d5210891cdb10858bc0a28ba7167909ab7c",
    },
    "8.2.0.53-10.2": {
        "Linux-x86_64": "6ecbc98b3795e940ce0831ffb7cd2c0781830fdd6b1911f950bcaf6d569f807c"
    },
    # cuDNN 8.1.1
    "8.1.1.33-11.2": {
        "Linux-x86_64": "98a8784e92862f20018d20c281b30d4a0cd951f93694f6433ccf4ae9c502ba6a",
        "Linux-ppc64le": "c3e535a5d633ad8f4d50be0b6f8efd084c6c6ed3525c07cbd89fc508b1d76c7a",
        "Linux-aarch64": "4f7e4f5698539659d51f28dff0da11e5445a5ae58439af1d8a8e9f2d93535245",
    },
    "8.1.1.33-10.2": {
        "Linux-x86_64": "2a4a7b99a6e9bfa690eb19bb41e49553f2a7a491a5b3abfcae900e166c5b6ebd"
    },
    # cuDNN 8.1.0
    "8.1.0.77-11.2": {
        "Linux-x86_64": "dbe82faf071d91ba9bcf00480146ad33f462482dfee56caf4479c1b8dabe3ecb",
        "Linux-ppc64le": "0d3f8fa21959e9f94889841cc8445aecf41d2f3c557091b447313afb43034037",
        "Linux-aarch64": "ba16ff486b68a8b50b69b32702612634954de529f39cfff68c12b8bfc1958499",
    },
    "8.1.0.77-10.2": {
        "Linux-x86_64": "c5bc617d89198b0fbe485156446be15a08aee37f7aff41c797b120912f2b14b4"
    },
    # cuDNN 8.0.5
    "8.0.5.39-11.1": {
        "Linux-x86_64": "1d046bfa79399dabcc6f6cb1507918754439442ea0ca9e0fbecdd446f9b00cce",
        "Linux-aarch64": "0c3542c51b42131247cd9f839d0ebefe4e02bb46d1716be1682cb2919278085a",
    },
    "8.0.5.39-11.0": {
        "Linux-x86_64": "4e16ee7895deb4a8b1c194b812ba49586ef7d26902051401d3717511898a9b73",
        "Linux-ppc64le": "05207a02c0b4f22464dbb0ee646693df4a70ae557640ba576ba8678c26393004",
    },
    "8.0.5.39-10.2": {
        "Linux-x86_64": "21f84c05c67bf1ec859e77c38ccd5bf154964fa1c308f449959be4c356e382f3",
        "Linux-ppc64le": "ce128ea090b05e36d00ffe921e45982ca10e8207e40cfc2e0067d0f62d9b36f9",
    },
    "8.0.5.39-10.1": {
        "Linux-x86_64": "90908495298896b33aa95063a3471f93c36627d7ac01c17dc36d75c65eea4a00",
        "Linux-ppc64le": "e43b10bb3932d5e7a598dcc726d16dc9938dd99dd319cd74b3420f3ed65fe5e0",
    },
    # cuDNN 8.0.4
    "8.0.4.30-11.1": {
        "Linux-x86_64": "8f4c662343afce5998ce963500fe3bb167e9a508c1a1a949d821a4b80fa9beab",
        "Linux-ppc64le": "b4ddb51610cbae806017616698635a9914c3e1eb14259f3a39ee5c84e7106712",
    },
    "8.0.4.30-11.0": {
        "Linux-x86_64": "38a81a28952e314e21577432b0bab68357ef9de7f6c8858f721f78df9ee60c35",
        "Linux-ppc64le": "8da8ed689b1a348182ddd3f59b6758a502e11dc6708c33f96e3b4a40e033d2e1",
    },
    "8.0.4.30-10.2": {
        "Linux-x86_64": "c12c69eb16698eacac40aa46b9ce399d4cd86efb6ff0c105142f8a28fcfb980e",
        "Linux-ppc64le": "32a5b92f9e1ef2be90e10f220c4ab144ca59d215eb6a386e93597f447aa6507e",
    },
    "8.0.4.30-10.1": {
        "Linux-x86_64": "eb4b888e61715168f57a0a0a21c281ada6856b728e5112618ed15f8637487715",
        "Linux-ppc64le": "690811bbf04adef635f4a6f480575fc2a558c4a2c98c85c7090a3a8c60dacea9",
    },
    # cuDNN 8.0.3
    "8.0.3.33-11.0": {
        "Linux-x86_64": "8924bcc4f833734bdd0009050d110ad0c8419d3796010cf7bc515df654f6065a",
        "Linux-ppc64le": "c2d0519831137b43d0eebe07522edb4ef5d62320e65e5d5fa840a9856f25923d",
    },
    "8.0.3.33-10.2": {
        "Linux-x86_64": "b3d487c621e24b5711983b89bb8ad34f0378bdbf8a1a4b86eefaa23b19956dcc",
        "Linux-ppc64le": "ff22c9c37af191c9104989d784427cde744cdde879bfebf3e4e55ca6a9634a11",
    },
    "8.0.3.33-10.1": {
        "Linux-x86_64": "4752ac6aea4e4d2226061610d6843da6338ef75a93518aa9ce50d0f58df5fb07",
        "Linux-ppc64le": "c546175f6ec86a11ee8fb9ab5526fa8d854322545769a87d35b1a505992f89c3",
    },
    # cuDNN 8.0.2
    "8.0.2.39-11.0": {
        "Linux-x86_64": "672f46288b8edd98f8d156a4f1ff518201ca6de0cff67915ceaa37f6d6d86345",
        "Linux-ppc64le": "b7c1ce5b1191eb007ba3455ea5f497fdce293a646545d8a6ed93e9bb06d7f057",
    },
    "8.0.2.39-10.2": {
        "Linux-x86_64": "c9cbe5c211360f3cfbc0fb104f0e9096b37e53f89392525679f049276b2f701f",
        "Linux-ppc64le": "c32325ff84a8123491f2e58b3694885a9a672005bc21764b38874688c0e43262",
    },
    "8.0.2.39-10.1": {
        "Linux-x86_64": "82148a68bd6bdaab93af5e05bb1842b8ccb3ab7de7bed41f609a7616c102213d",
        "Linux-ppc64le": "8196ec4f031356317baeccefbc4f61c8fccb2cf0bdef0a6431438918ddf68fb9",
    },
    # cuDNN 8.0
    "8.0.0.180-11.0": {
        "Linux-x86_64": "9e75ea70280a77de815e0bdc85d08b67e081bc99a708b574092142344d2ba07e",
        "Linux-ppc64le": "1229e94731bbca63ee7f5a239f4e1838a51a301d896f3097fbf7377d74704060",
    },
    "8.0.0.180-10.2": {
        "Linux-x86_64": "0c87c12358ee2b99d57c2a8c7560e3bb93e54bb929f5f8bec4964a72a2bb261d",
        "Linux-ppc64le": "59e4ad6db15fcc374976e8052fe39e3f30f34079710fb3c7751a64c853d9243f",
    },
    # cuDNN 7.6.5
    "7.6.5.32-10.2": {
        "Linux-x86_64": "600267f2caaed2fd58eb214ba669d8ea35f396a7d19b94822e6b36f9f7088c20",
        "Linux-ppc64le": "7dc08b6ab9331bfd12207d4802c61db1ad7cace7395b67a6e7b16efa0335668b",
    },
    "7.6.5.32-10.1": {
        "Linux-x86_64": "7eaec8039a2c30ab0bc758d303588767693def6bf49b22485a2c00bf2e136cb3",
        "Darwin-x86_64": "8ecce28a5ed388a2b9b2d239e08d7c550f53b79288e6d9e5eb4c152bfc711aff",
        "Linux-ppc64le": "97b2faf73eedfc128f2f5762784d21467a95b2d5ba719825419c058f427cbf56",
    },
    "7.6.5.32-10.0": {
        "Linux-x86_64": "28355e395f0b2b93ac2c83b61360b35ba6cd0377e44e78be197b6b61b4b492ba",
        "Darwin-x86_64": "6fa0b819374da49102e285ecf7fcb8879df4d0b3cc430cc8b781cdeb41009b47",
        "Linux-ppc64le": "b1717f4570083bbfc6b8b59f280bae4e4197cc1cb50e9d873c05adf670084c5b",
    },
    "7.6.5.32-9.2": {
        "Linux-x86_64": "a2a2c7a8ba7b16d323b651766ee37dcfdbc2b50d920f73f8fde85005424960e4",
        "Linux-ppc64le": "a11f44f9a827b7e69f527a9d260f1637694ff7c1674a3e46bd9ec054a08f9a76",
    },
    "7.6.5.32-9.0": {
        "Linux-x86_64": "bd0a4c0090d5b02feec3f195738968690cc2470b9bc6026e6fe8ff245cd261c8"
    },
    # cuDNN 7.6.4
    "7.6.4.38-10.1": {
        "Linux-x86_64": "32091d115c0373027418620a09ebec3658a6bc467d011de7cdd0eb07d644b099",
        "Darwin-x86_64": "bfced062c3689ced2c1fb49c7d5052e6bc3da6974c1eb707e4dcf8cd209d4236",
        "Linux-ppc64le": "f3615fea50986a4dfd05d7a0cf83396dfdceefa9c209e8bf9691e20a48e420ce",
    },
    "7.6.4.38-10.0": {
        "Linux-x86_64": "417bb5daf51377037eb2f5c87649000ca1b9cec0acb16cfe07cb1d3e9a961dbf",
        "Darwin-x86_64": "af01ab841caec25087776a6b8fc7782883da12e590e24825ad1031f9ae0ed4b1",
        "Linux-ppc64le": "c1725ad6bd7d7741e080a1e6da4b62eac027a94ac55c606cce261e3f829400bb",
    },
    "7.6.4.38-9.2": {
        "Linux-x86_64": "c79156531e641289b6a6952888b9637059ef30defd43c3cf82acf38d67f60a27",
        "Linux-ppc64le": "98d8aae2dcd851558397a9a30b73242f257e1556be17c83650e63a0685969884",
    },
    "7.6.4.38-9.0": {
        "Linux-x86_64": "8db78c3623c192d4f03f3087b41c32cb0baac95e13408b5d9dabe626cb4aab5d"
    },
    # cuDNN 7.6.3
    "7.6.3.30-10.1": {
        "Linux-x86_64": "352557346d8111e2f954c494be1a90207103d316b8777c33e62b3a7f7b708961",
        "Linux-ppc64le": "f274735a8fc31923d3623b1c3d2b1d0d35bb176687077c6a4d4353c6b900d8ee",
    },
    # cuDNN 7.5.1
    "7.5.1.10-10.1": {
        "Linux-x86_64": "2c833f43c9147d9a25a20947a4c5a5f5c33b2443240fd767f63b330c482e68e0",
        "Linux-ppc64le": "a9e23bc83c970daec20874ccd1d8d80b648adf15440ecd0164818b330b1e2663",
    },
    "7.5.1.10-10.0": {
        "Linux-x86_64": "c0a4ec438920aa581dd567117b9c316745b4a451ac739b1e04939a3d8b229985",
        "Linux-ppc64le": "d9205718da5fbab85433476f9ff61fcf4b889d216d6eea26753bbc24d115dd70",
    },
    # cuDNN 7.5.0
    "7.5.0.56-10.1": {
        "Linux-x86_64": "c31697d6b71afe62838ad2e57da3c3c9419c4e9f5635d14b683ebe63f904fbc8",
        "Linux-ppc64le": "15415eb714ab86ab6c7531f2cac6474b5dafd989479b062776c670b190e43638",
    },
    "7.5.0.56-10.0": {
        "Linux-x86_64": "701097882cb745d4683bb7ff6c33b8a35c7c81be31bac78f05bad130e7e0b781",
        "Linux-ppc64le": "f0c1cbd9de553c8e2a3893915bd5fff57b30e368ef4c964d783b6a877869e93a",
    },
    # cuDNN 7.3.0
    "7.3.0.29-9.0": {
        "Linux-x86_64": "403f9043ff2c7b2c5967454872275d07bca11fd41dfc7b21995eadcad6dbe49b"
    },
    # cuDNN 7.2.1
    "7.2.1.38-9.0": {
        "Linux-x86_64": "cf007437b9ac6250ec63b89c25f248d2597fdd01369c80146567f78e75ce4e37"
    },
    # cuDNN 7.1.3
    "7.1.3-9.1": {
        "Linux-x86_64": "dd616d3794167ceb923d706bf73e8d6acdda770751492b921ee6827cdf190228",
        "Linux-ppc64le": "e3b4837f711b98a52faacc872a68b332c833917ef3cf87c0108f1d01af9b2931",
    },
    # cuDNN 6.0
    "6.0-8.0": {
        "Linux-x86_64": "9b09110af48c9a4d7b6344eb4b3e344daa84987ed6177d5c44319732f3bb7f9c"
    },
    # cuDNN 5.1
    "5.1-8.0": {
        "Linux-x86_64": "c10719b36f2dd6e9ddc63e3189affaa1a94d7d027e63b71c3f64d449ab0645ce"
    },
}


class Cudnn(Package):
    """NVIDIA cuDNN is a GPU-accelerated library of primitives for deep
    neural networks"""

    homepage = "https://developer.nvidia.com/cudnn"

    # Latest versions available at:
    #     https://developer.nvidia.com/rdp/cudnn-download
    # Archived versions available at:
    #     https://developer.nvidia.com/rdp/cudnn-archive
    # Note that download links don't work from command line,
    # need to use modified URLs like in url_for_version.
    maintainers("adamjstewart", "bvanessen")

    skip_version_audit = ["platform=darwin", "platform=windows"]

    license("MIT")

    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg = packages.get(key)
        cudnn_ver, cuda_ver = ver.split("-")
        long_ver = "{0}-{1}".format(cudnn_ver, cuda_ver)
        if pkg:
            version(long_ver, sha256=pkg)
            # Add constraints matching CUDA version to cuDNN version
            # cuDNN builds for CUDA 11.x are compatible with all CUDA 11.x:
            # https://docs.nvidia.com/deeplearning/cudnn/support-matrix/index.html#fntarg_2
            if Version(cuda_ver) >= Version("11"):
                cuda_ver = Version(cuda_ver).up_to(1)
            depends_on("cuda@{}".format(cuda_ver), when="@{}".format(long_ver))

    def url_for_version(self, version):
        # Get the system and machine arch for building the file path
        sys = "{0}-{1}".format(platform.system(), platform.machine())
        # Munge it to match Nvidia's naming scheme
        sys_key = sys.lower()
        if version < Version("8.3.1"):
            sys_key = (
                sys_key.replace("x86_64", "x64")
                .replace("darwin", "osx")
                .replace("aarch64", "aarch64sbsa")
            )
        elif version < Version("8.8.0"):
            sys_key = sys_key.replace("aarch64", "sbsa")

        if version >= Version("8.3.1"):
            # NOTE: upload layout changed for 8.3.1, they include a 10.2
            # artifact for cuda@10.2 x86_64, but the runtime is only supported
            # for cuda@11.  See
            # https://docs.nvidia.com/deeplearning/cudnn/release-notes/rel_8.html
            # As such, hacking the `directory` to include the extra
            # local_installers/11.5 is included as this may not happen again.
            directory = version[:3]
            ver = version[:4]
            cuda = version[4:]
            directory = "{0}/local_installers/{1}".format(directory, cuda)
        elif version >= Version("7.2"):
            directory = version[:3]
            ver = version[:4]
            cuda = version[4:]
        elif version >= Version("7.1"):
            directory = version[:3]
            ver = version[:2]
            cuda = version[3:]
        elif version >= Version("7.0"):
            directory = version[:3]
            ver = version[0]
            cuda = version[3:]
        else:
            directory = version[:2]
            ver = version[:2]
            cuda = version[2:]

        # 8.8.0 changed the base url again
        if version >= Version("8.8.0"):
            url = "https://developer.download.nvidia.com/compute/cudnn/redist/cudnn/{0}/cudnn-{0}-{1}_cuda{2}-archive.tar.xz"
            return url.format(sys_key, ver, cuda.up_to(1))
        # 8.5.0 removed minor from cuda version
        elif version >= Version("8.5.0"):
            url = "https://developer.download.nvidia.com/compute/redist/cudnn/v{0}/cudnn-{1}-{2}_cuda{3}-archive.tar.xz"
            return url.format(directory, sys_key, ver, cuda.up_to(1))
        # 8.3.1 switched to xzip tarballs and reordered url parts.
        elif version >= Version("8.3.1"):
            url = "https://developer.download.nvidia.com/compute/redist/cudnn/v{0}/cudnn-{1}-{2}_cuda{3}-archive.tar.xz"
            return url.format(directory, sys_key, ver, cuda)
        else:
            url = "https://developer.download.nvidia.com/compute/redist/cudnn/v{0}/cudnn-{1}-{2}-v{3}.tgz"
            return url.format(directory, cuda, sys_key, ver)

    def setup_run_environment(self, env):
        # Package is not compiled, and does not work unless LD_LIBRARY_PATH is set
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)

        if self.spec.satisfies("target=ppc64le: platform=linux"):
            env.set("cuDNN_ROOT", os.path.join(self.prefix, "targets", "ppc64le-linux"))

    def install(self, spec, prefix):
        install_tree(".", prefix)

        if spec.satisfies("target=ppc64le: platform=linux"):
            target_lib = os.path.join(prefix, "targets", "ppc64le-linux", "lib")
            if os.path.isdir(target_lib) and not os.path.isdir(prefix.lib):
                symlink(target_lib, prefix.lib)
            target_include = os.path.join(prefix, "targets", "ppc64le-linux", "include")
            if os.path.isdir(target_include) and not os.path.isdir(prefix.include):
                symlink(target_include, prefix.include)
