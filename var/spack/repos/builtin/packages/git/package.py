# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
import re
import os
from spack import *


class Git(AutotoolsPackage):
    """Git is a free and open source distributed version control
    system designed to handle everything from small to very large
    projects with speed and efficiency.
    """

    homepage = "http://git-scm.com"
    url      = "https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.12.0.tar.gz"

    executables = ['^git$']

    # In order to add new versions here, add a new list entry with:
    # * version: {version}
    # * sha256: the sha256sum of the git-{version}.tar.gz
    # * sha256_manpages: the sha256sum of the corresponding manpage from
    #       https://www.kernel.org/pub/software/scm/git/git-manpages-{version}.tar.gz
    # You can find the source here: https://mirrors.edge.kernel.org/pub/software/scm/git/sha256sums.asc
    releases = [
        {
            'version': '2.29.0',
            'sha256': 'fa08dc8424ef80c0f9bf307877f9e2e49f1a6049e873530d6747c2be770742ff',
            'sha256_manpages': '8f3bf70ddb515674ce2e19572920a39b1be96af12032b77f1dd57898981fb151'
        },
        {
            'version': '2.28.0',
            'sha256': 'f914c60a874d466c1e18467c864a910dd4ea22281ba6d4d58077cb0c3f115170',
            'sha256_manpages': '3cfca28a88d5b8112ea42322b797a500a14d0acddea391aed0462aff1ab11bf7'
        },
        {
            'version': '2.27.0',
            'sha256': '77ded85cbe42b1ffdc2578b460a1ef5d23bcbc6683eabcafbb0d394dffe2e787',
            'sha256_manpages': '414e4b17133e54d846f6bfa2479f9757c50e16c013eb76167a492ae5409b8947'
        },
        {
            'version': '2.26.0',
            'sha256': 'aa168c2318e7187cd295a645f7370cc6d71a324aafc932f80f00c780b6a26bed',
            'sha256_manpages': 'c1ffaf0b4cd1e80a0eb0d4039e208c9d411ef94d5da44e38363804e1a7961218'
        },
        {
            'version': '2.25.0',
            'sha256': 'a98c9b96d91544b130f13bf846ff080dda2867e77fe08700b793ab14ba5346f6',
            'sha256_manpages': '22b2380842ef75e9006c0358de250ead449e1376d7e5138070b9a3073ef61d44'
        },
        {
            'version': '2.21.0',
            'sha256': '85eca51c7404da75e353eba587f87fea9481ba41e162206a6f70ad8118147bee',
            'sha256_manpages': '14c76ebb4e31f9e55cf5338a04fd3a13bced0323cd51794ccf45fc74bd0c1080'
        },
        {
            'version': '2.20.1',
            'sha256': 'edc3bc1495b69179ba4e272e97eff93334a20decb1d8db6ec3c19c16417738fd',
            'sha256_manpages': 'e9c123463abd05e142defe44a8060ce6e9853dfd8c83b2542e38b7deac4e6d4c'
        },
        {
            'version': '2.19.2',
            'sha256': 'db893ad69c9ac9498b09677c5839787eba2eb3b7ef2bc30bfba7e62e77cf7850',
            'sha256_manpages': '60334ecd59ee10319af4a7815174d10991d1afabacd3b3129d589f038bf25542'
        },
        {
            'version': '2.19.1',
            'sha256': 'ec4dc96456612c65bf6d944cee9ac640145ec7245376832b781cb03e97cbb796',
            'sha256_manpages': 'bd27f58dc90a661e3080b97365eb7322bfa185de95634fc59d98311925a7d894'
        },
        {
            'version': '2.18.0',
            'sha256': '94faf2c0b02a7920b0b46f4961d8e9cad08e81418614102898a55f980fa3e7e4',
            'sha256_manpages': '6cf38ab3ad43ccdcd6a73ffdcf2a016d56ab6b4b240a574b0bb96f520a04ff55'
        },
        {
            'version': '2.17.1',
            'sha256': 'ec6452f0c8d5c1f3bcceabd7070b8a8a5eea11d4e2a04955c139b5065fd7d09a',
            'sha256_manpages': '9732053c1a618d2576c1751d0249e43702f632a571f84511331882beb360677d'
        },
        {
            'version': '2.17.0',
            'sha256': '7a0cff35dbb14b77dca6924c33ac9fe510b9de35d5267172490af548ec5ee1b8',
            'sha256_manpages': '41b58c68e90e4c95265c75955ddd5b68f6491f4d57b2f17c6d68e60bbb07ba6a'
        },
        {
            'version': '2.15.1',
            'sha256': '85fca8781a83c96ba6db384cc1aa6a5ee1e344746bafac1cbe1f0fe6d1109c84',
            'sha256_manpages': '472454c494c9a7f50ad38060c3eec372f617de654b20f3eb3be59fc17a683fa1',
        },
        {
            'version': '2.14.1',
            'sha256': '01925349b9683940e53a621ee48dd9d9ac3f9e59c079806b58321c2cf85a4464',
            'sha256_manpages': '8c5810ce65d44cd333327d3a115c5b462712a2f81225d142e07bd889ad8dc0e0',
        },
        {
            'version': '2.13.0',
            'sha256': '9f2fa8040ebafc0c2caae4a9e2cb385c6f16c0525bcb0fbd84938bc796372e80',
            'sha256_manpages': 'e764721796cad175a4cf9a4afe7fb4c4fc57582f6f9a6e214239498e0835355b',
        },
        {
            'version': '2.12.2',
            'sha256': 'd9c6d787a24670d7e5100db2367c250ad9756ef8084fb153a46b82f1d186f8d8',
            'sha256_manpages': '6e7ed503f1190734e57c9427df356b42020f125fa36ab0478777960a682adf50',
        },
        {
            'version': '2.12.1',
            'sha256': '65d62d10caf317fc1daf2ca9975bdb09dbff874c92d24f9529d29a7784486b43',
            'sha256_manpages': '35e46b8acd529ea671d94035232b1795919be8f3c3a363ea9698f1fd08d7d061',
        },
        {
            'version': '2.12.0',
            'sha256': '882f298daf582a07c597737eb4bbafb82c6208fe0e73c047defc12169c221a92',
            'sha256_manpages': '1f7733a44c59f9ae8dd321d68a033499a76c82046025cc2a6792299178138d65',
        },
        {
            'version': '2.11.1',
            'sha256': 'a1cdd7c820f92c44abb5003b36dc8cb7201ba38e8744802399f59c97285ca043',
            'sha256_manpages': 'ee567e7b0f95333816793714bb31c54e288cf8041f77a0092b85e62c9c2974f9',
        },
        {
            'version': '2.11.0',
            'sha256': 'd3be9961c799562565f158ce5b836e2b90f38502d3992a115dfb653d7825fd7e',
            'sha256_manpages': '437a0128acd707edce24e1a310ab2f09f9a09ee42de58a8e7641362012dcfe22',
        },
        {
            'version': '2.9.3',
            'sha256': 'a252b6636b12d5ba57732c8469701544c26c2b1689933bd1b425e603cbb247c0',
            'sha256_manpages': '8ea1a55b048fafbf0c0c6fcbca4b5b0f5e9917893221fc7345c09051d65832ce',
        },
        {
            'version': '2.9.2',
            'sha256': '3cb09a3917c2d8150fc1708f3019cf99a8f0feee6cd61bba3797e3b2a85be9dc',
            'sha256_manpages': 'ac5c600153d1e4a1c6494e250cd27ca288e7667ad8d4ea2f2386f60ba1b78eec',
        },
        {
            'version': '2.9.1',
            'sha256': 'c2230873bf77f93736473e6a06501bf93eed807d011107de6983dc015424b097',
            'sha256_manpages': '324f5f173f2bd50b0102b66e474b81146ccc078d621efeb86d7f75e3c1de33e6',
        },
        {
            'version': '2.9.0',
            'sha256': 'bff7560f5602fcd8e37669e0f65ef08c6edc996e4f324e4ed6bb8a84765e30bd',
            'sha256_manpages': '35ba69a8560529aa837e395a6d6c8d42f4d29b40a3c1cc6e3dc69bb1faadb332',
        },
        {
            'version': '2.8.4',
            'sha256': '626e319f8a24fc0866167ea5f6bf3e2f38f69d6cb2e59e150f13709ca3ebf301',
            'sha256_manpages': '953a8eadaf4ae96dbad2c3ec12384c677416843917ef83d94b98367ffd55afc0',
        },
        {
            'version': '2.8.3',
            'sha256': '2dad50c758339d6f5235309db620e51249e0000ff34aa2f2acbcb84c2123ed09',
            'sha256_manpages': '2dad50c758339d6f5235309db620e51249e0000ff34aa2f2acbcb84c2123ed09',
        },
        {
            'version': '2.8.2',
            'sha256': 'a029c37ee2e0bb1efea5c4af827ff5afdb3356ec42fc19c1d40216d99e97e148',
            'sha256_manpages': '82d322211aade626d1eb3bcf3b76730bfdd2fcc9c189950fb0a8bdd69c383e2f',
        },
        {
            'version': '2.8.1',
            'sha256': 'cfc66324179b9ed62ee02833f29d39935f4ab66874125a3ab9d5bb9055c0cb67',
            'sha256_manpages': 'df46de0c172049f935cc3736361b263c5ff289b77077c73053e63ae83fcf43f4',
        },
        {
            'version': '2.8.0',
            'sha256': '2c6eee5506237e0886df9973fd7938a1b2611ec93d07f64ed3447493ebac90d1',
            'sha256_manpages': '2c48902a69df3bec3b8b8f0350a65fd1b662d2f436f0e64d475ecd1c780767b6',
        },
        {
            'version': '2.7.3',
            'sha256': '30d067499b61caddedaf1a407b4947244f14d10842d100f7c7c6ea1c288280cd',
            'sha256_manpages': '84b487c9071857ab0f15f11c4a102a583d59b524831cda0dc0954bd3ab73920b',
        },
        {
            'version': '2.7.1',
            'sha256': 'b4ab42798b7fb038eaefabb0c32ce9dbde2919103e5e2a35adc35dd46258a66f',
            'sha256_manpages': '0313cf4d283336088883d8416692fb6c547512233e11dbf06e5b925b7e762d61',
        },
    ]

    for release in releases:
        version(release['version'], sha256=release['sha256'])
        resource(
            name='git-manpages',
            url="https://www.kernel.org/pub/software/scm/git/git-manpages-{0}.tar.gz".format(
                release['version']),
            sha256=release['sha256_manpages'],
            placement='git-manpages',
            when='@{0}'.format(release['version']))

    variant('tcltk', default=False,
            description='Gitk: provide Tcl/Tk in the run environment')

    depends_on('curl')
    depends_on('expat')
    depends_on('gettext')
    depends_on('iconv')
    depends_on('libidn2')
    depends_on('openssl')
    depends_on('pcre', when='@:2.13')
    depends_on('pcre2', when='@2.14:')
    depends_on('perl')
    depends_on('zlib')
    depends_on('openssh', type='run')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('tk',       type=('build', 'link'), when='+tcltk')

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'git version (\S+)', output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version_str):
        prefix = os.path.dirname(exes[0])
        variants = ''
        if 'gitk' in os.listdir(prefix):
            variants += '+tcltk'
        else:
            variants += '~tcltk'
        return variants

    # See the comment in setup_build_environment re EXTLIBS.
    def patch(self):
        filter_file(r'^EXTLIBS =$',
                    '#EXTLIBS =',
                    'Makefile')

    def setup_build_environment(self, env):
        # We use EXTLIBS rather than LDFLAGS so that git's Makefile
        # inserts the information into the proper place in the link commands
        # (alongside the # other libraries/paths that configure discovers).
        # LDFLAGS is inserted *before* libgit.a, which requires libintl.
        # EXTFLAGS is inserted *after* libgit.a.
        # This depends on the patch method above, which keeps the Makefile
        # from stepping on the value that we pass in via the environment.
        #
        # The test avoids failures when git is an external package.
        # In that case the node in the DAG gets truncated and git DOES NOT
        # have a gettext dependency.
        if 'gettext' in self.spec:
            if self.spec['gettext'].prefix != '/usr':
                env.append_flags('EXTLIBS', '-L{0} -lintl'.format(
                    self.spec['gettext'].prefix.lib))
            env.append_flags('CFLAGS', '-I{0}'.format(
                self.spec['gettext'].prefix.include))

    def configure_args(self):
        spec = self.spec

        configure_args = [
            '--with-curl={0}'.format(spec['curl'].prefix),
            '--with-expat={0}'.format(spec['expat'].prefix),
            '--with-iconv={0}'.format(spec['iconv'].prefix),
            '--with-openssl={0}'.format(spec['openssl'].prefix),
            '--with-perl={0}'.format(spec['perl'].command.path),
            '--with-zlib={0}'.format(spec['zlib'].prefix),
        ]

        if '^pcre' in self.spec:
            configure_args.append('--with-libpcre={0}'.format(
                spec['pcre'].prefix))
        if '^pcre2' in self.spec:
            configure_args.append('--with-libpcre2={0}'.format(
                spec['pcre2'].prefix))
        if '+tcltk' in self.spec:
            configure_args.append('--with-tcltk={0}'.format(
                self.spec['tk'].prefix.bin.wish))
        else:
            configure_args.append('--without-tcltk')

        return configure_args

    @run_after('configure')
    def filter_rt(self):
        if sys.platform == 'darwin':
            # Don't link with -lrt; the system has no (and needs no) librt
            filter_file(r' -lrt$', '', 'Makefile')

    def check(self):
        make('test')

    @run_after('install')
    def install_completions(self):
        install_tree('contrib/completion', self.prefix.share)

    @run_after('install')
    def install_manpages(self):
        prefix = self.prefix

        with working_dir('git-manpages'):
            install_tree('man1', prefix.share.man.man1)
            install_tree('man5', prefix.share.man.man5)
            install_tree('man7', prefix.share.man.man7)
