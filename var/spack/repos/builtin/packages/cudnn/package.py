# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *
import platform

_versions = {
    # cuDNN 8.0.4
    '8.0.4.30-11.1': {
        'Linux-x86_64' : ('8f4c662343afce5998ce963500fe3bb167e9a508c1a1a949d821a4b80fa9beab'),
        'Linux-ppc64le': ('b4ddb51610cbae806017616698635a9914c3e1eb14259f3a39ee5c84e7106712')},
    '8.0.4.30-11.0': {
        'Linux-x86_64' : ('38a81a28952e314e21577432b0bab68357ef9de7f6c8858f721f78df9ee60c35'),
        'Linux-ppc64le': ('8da8ed689b1a348182ddd3f59b6758a502e11dc6708c33f96e3b4a40e033d2e1')},
    '8.0.4.30-10.2': {
        'Linux-x86_64' : ('c12c69eb16698eacac40aa46b9ce399d4cd86efb6ff0c105142f8a28fcfb980e'),
        'Linux-ppc64le': ('32a5b92f9e1ef2be90e10f220c4ab144ca59d215eb6a386e93597f447aa6507e')},
    '8.0.4.30-10.1': {
        'Linux-x86_64' : ('eb4b888e61715168f57a0a0a21c281ada6856b728e5112618ed15f8637487715'),
        'Linux-ppc64le': ('690811bbf04adef635f4a6f480575fc2a558c4a2c98c85c7090a3a8c60dacea9')},

    # cuDNN 8.0.3
    '8.0.3.33-11.0': {
        'Linux-x86_64' : ('8924bcc4f833734bdd0009050d110ad0c8419d3796010cf7bc515df654f6065a'),
        'Linux-ppc64le': ('c2d0519831137b43d0eebe07522edb4ef5d62320e65e5d5fa840a9856f25923d')},
    '8.0.3.33-10.2': {
        'Linux-x86_64' : ('b3d487c621e24b5711983b89bb8ad34f0378bdbf8a1a4b86eefaa23b19956dcc'),
        'Linux-ppc64le': ('ff22c9c37af191c9104989d784427cde744cdde879bfebf3e4e55ca6a9634a11')},
    '8.0.3.33-10.1': {
        'Linux-x86_64' : ('4752ac6aea4e4d2226061610d6843da6338ef75a93518aa9ce50d0f58df5fb07'),
        'Linux-ppc64le': ('c546175f6ec86a11ee8fb9ab5526fa8d854322545769a87d35b1a505992f89c3')},

    # cuDNN 8.0.2
    '8.0.2.39-11.0': {
        'Linux-x86_64' : ('672f46288b8edd98f8d156a4f1ff518201ca6de0cff67915ceaa37f6d6d86345'),
        'Linux-ppc64le': ('b7c1ce5b1191eb007ba3455ea5f497fdce293a646545d8a6ed93e9bb06d7f057')},
    '8.0.2.39-10.2': {
        'Linux-x86_64' : ('c9cbe5c211360f3cfbc0fb104f0e9096b37e53f89392525679f049276b2f701f'),
        'Linux-ppc64le': ('c32325ff84a8123491f2e58b3694885a9a672005bc21764b38874688c0e43262')},
    '8.0.2.39-10.1': {
        'Linux-x86_64' : ('82148a68bd6bdaab93af5e05bb1842b8ccb3ab7de7bed41f609a7616c102213d'),
        'Linux-ppc64le': ('8196ec4f031356317baeccefbc4f61c8fccb2cf0bdef0a6431438918ddf68fb9')},

    # cuDNN 8.0
    '8.0.0.180-11.0': {
        'Linux-x86_64' : ('9e75ea70280a77de815e0bdc85d08b67e081bc99a708b574092142344d2ba07e'),
        'Linux-ppc64le': ('1229e94731bbca63ee7f5a239f4e1838a51a301d896f3097fbf7377d74704060')},
    '8.0.0.180-10.2': {
        'Linux-x86_64' : ('0c87c12358ee2b99d57c2a8c7560e3bb93e54bb929f5f8bec4964a72a2bb261d'),
        'Linux-ppc64le': ('59e4ad6db15fcc374976e8052fe39e3f30f34079710fb3c7751a64c853d9243f')},

    # cuDNN 7.6.5
    '7.6.5.32-10.2': {
        'Linux-x86_64' : ('600267f2caaed2fd58eb214ba669d8ea35f396a7d19b94822e6b36f9f7088c20'),
        'Linux-ppc64le': ('7dc08b6ab9331bfd12207d4802c61db1ad7cace7395b67a6e7b16efa0335668b')},
    '7.6.5.32-10.1': {
        'Linux-x86_64' : ('7eaec8039a2c30ab0bc758d303588767693def6bf49b22485a2c00bf2e136cb3'),
        'Darwin-x86_64': ('8ecce28a5ed388a2b9b2d239e08d7c550f53b79288e6d9e5eb4c152bfc711aff'),
        'Linux-ppc64le': ('97b2faf73eedfc128f2f5762784d21467a95b2d5ba719825419c058f427cbf56')},

    '7.6.5.32-10.0': {
        'Linux-x86_64' : ('28355e395f0b2b93ac2c83b61360b35ba6cd0377e44e78be197b6b61b4b492ba'),
        'osx-x86_64'   : ('6fa0b819374da49102e285ecf7fcb8879df4d0b3cc430cc8b781cdeb41009b47'),
        'Linux-ppc64le': ('b1717f4570083bbfc6b8b59f280bae4e4197cc1cb50e9d873c05adf670084c5b')},

    '7.6.5.32-9.2': {
        'Linux-x86_64' : ('a2a2c7a8ba7b16d323b651766ee37dcfdbc2b50d920f73f8fde85005424960e4'),
        'Linux-ppc64le': ('a11f44f9a827b7e69f527a9d260f1637694ff7c1674a3e46bd9ec054a08f9a76')},

    '7.6.5.32-9.0': {
        'Linux-x86_64' : ('bd0a4c0090d5b02feec3f195738968690cc2470b9bc6026e6fe8ff245cd261c8')},

    # cuDNN 7.6.4
    '7.6.4.38-10.1': {
        'Linux-x86_64' : ('32091d115c0373027418620a09ebec3658a6bc467d011de7cdd0eb07d644b099'),
        'Darwin-x86_64': ('bfced062c3689ced2c1fb49c7d5052e6bc3da6974c1eb707e4dcf8cd209d4236'),
        'Linux-ppc64le': ('f3615fea50986a4dfd05d7a0cf83396dfdceefa9c209e8bf9691e20a48e420ce')},

    '7.6.4.38-10.0': {
        'Linux-x86_64' : ('417bb5daf51377037eb2f5c87649000ca1b9cec0acb16cfe07cb1d3e9a961dbf'),
        'Darwin-x86_64': ('af01ab841caec25087776a6b8fc7782883da12e590e24825ad1031f9ae0ed4b1'),
        'Linux-ppc64le': ('c1725ad6bd7d7741e080a1e6da4b62eac027a94ac55c606cce261e3f829400bb')},

    '7.6.4.38-9.2': {
        'Linux-x86_64' : ('c79156531e641289b6a6952888b9637059ef30defd43c3cf82acf38d67f60a27'),
        'Linux-ppc64le': ('98d8aae2dcd851558397a9a30b73242f257e1556be17c83650e63a0685969884')},

    '7.6.4.38-9.0': {
        'Linux-x86_64' : ('8db78c3623c192d4f03f3087b41c32cb0baac95e13408b5d9dabe626cb4aab5d')},

    # cuDNN 7.6.3
    '7.6.3.30-10.1': {
        'Linux-x86_64' : ('352557346d8111e2f954c494be1a90207103d316b8777c33e62b3a7f7b708961'),
        'Linux-ppc64le': ('f274735a8fc31923d3623b1c3d2b1d0d35bb176687077c6a4d4353c6b900d8ee')},

    # cuDNN 7.5.1
    '7.5.1.10-10.1': {
        'Linux-x86_64' : ('2c833f43c9147d9a25a20947a4c5a5f5c33b2443240fd767f63b330c482e68e0'),
        'Linux-ppc64le': ('a9e23bc83c970daec20874ccd1d8d80b648adf15440ecd0164818b330b1e2663')},

    '7.5.1.10-10.0': {
        'Linux-x86_64' : ('c0a4ec438920aa581dd567117b9c316745b4a451ac739b1e04939a3d8b229985'),
        'Linux-ppc64le': ('d9205718da5fbab85433476f9ff61fcf4b889d216d6eea26753bbc24d115dd70')},

    # cuDNN 7.5.0
    '7.5.0.56-10.1': {
        'Linux-x86_64' : ('c31697d6b71afe62838ad2e57da3c3c9419c4e9f5635d14b683ebe63f904fbc8'),
        'Linux-ppc64le': ('15415eb714ab86ab6c7531f2cac6474b5dafd989479b062776c670b190e43638')},

    '7.5.0.56-10.0': {
        'Linux-x86_64' : ('701097882cb745d4683bb7ff6c33b8a35c7c81be31bac78f05bad130e7e0b781'),
        'Linux-ppc64le': ('f0c1cbd9de553c8e2a3893915bd5fff57b30e368ef4c964d783b6a877869e93a')},

    # cuDNN 7.3.0
    '7.3.0.29-9.0': {
        'Linux-x86_64' : ('403f9043ff2c7b2c5967454872275d07bca11fd41dfc7b21995eadcad6dbe49b')},

    # cuDNN 7.2.1
    '7.2.1.38-9.0': {
        'Linux-x86_64' : ('cf007437b9ac6250ec63b89c25f248d2597fdd01369c80146567f78e75ce4e37')},

    # cuDNN 7.1.3
    '7.1.3-9.1': {
        'Linux-x86_64' : ('dd616d3794167ceb923d706bf73e8d6acdda770751492b921ee6827cdf190228'),
        'Linux-ppc64le': ('e3b4837f711b98a52faacc872a68b332c833917ef3cf87c0108f1d01af9b2931')},

    # cuDNN 6.0
    '6.0-8.0': {
        'Linux-x86_64': ('9b09110af48c9a4d7b6344eb4b3e344daa84987ed6177d5c44319732f3bb7f9c')},

    # cuDNN 5.1
    '5.1-8.0': {
        'Linux-x86_64': ('c10719b36f2dd6e9ddc63e3189affaa1a94d7d027e63b71c3f64d449ab0645ce')},

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

    maintainers = ['adamjstewart', 'bvanessen']

    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg = packages.get(key)
        cudnn_ver, cuda_ver = ver.split('-')
        long_ver ="{0}-{1}".format(cudnn_ver, cuda_ver) 
        if pkg:
            version(long_ver, sha256=pkg[0], expand=False)
            # Add constraints matching CUDA version to cuDNN version
            cuda_req = 'cuda@{0}.0:{0}.099'.format(cuda_ver)
            cudnn_ver_req = '@{0}'.format(long_ver)
            depends_on(cuda_req, when=cudnn_ver_req)

    def url_for_version(self, version):
        url = 'https://developer.download.nvidia.com/compute/redist/cudnn/v{0}/cudnn-{1}-{2}-v{3}.tgz'
        # Get the system and machine arch for building the file path
        sys = "{0}-{1}".format(platform.system(), platform.machine())
        # Munge it to match Nvidia's naming scheme
        sys_key = sys.lower().replace('x86_64','x64').replace('Darwin', 'osx')

        if version >= Version('7.2'):
            directory = version[:3]
            ver = version[:4]
            cuda = version[4:]
        elif version >= Version('7.1'):
            directory = version[:3]
            ver = version[:2]
            cuda = version[3:]
        elif version >= Version('7.0'):
            directory = version[:3]
            ver = version[0]
            cuda = version[3:]
        else:
            directory = version[:2]
            ver = version[:2]
            cuda = version[2:]

        return url.format(directory, cuda, sys_key, ver)

    def setup_run_environment(self, env):
        if 'target=ppc64le: platform=linux' in self.spec:
            env.set('cuDNN_ROOT', os.path.join(
                self.prefix, 'targets', 'ppc64le-linux'))

    def install(self, spec, prefix):
        install_tree('.', prefix)

        if 'target=ppc64le: platform=linux' in spec:
            target_lib = os.path.join(prefix, 'targets',
                                      'ppc64le-linux', 'lib')
            if os.path.isdir(target_lib) and not os.path.isdir(prefix.lib):
                symlink(target_lib, prefix.lib)
            target_include = os.path.join(prefix, 'targets',
                                          'ppc64le-linux', 'include')
            if os.path.isdir(target_include) \
               and not os.path.isdir(prefix.include):
                symlink(target_include, prefix.include)
