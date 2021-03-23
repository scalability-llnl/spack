# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os.path
import platform


# The viewer and trace viewer tar files and sha256sum depend on the
# version and machine type.  Starting with 2019.08, the name of the
# tar file contains the version number.
def viewer_url(ver, mach):
    ver2 = ('-' + ver) if ver >= '2019.08' else ''
    return (
        'http://hpctoolkit.org/download/hpcviewer/{0}/'
        'hpcviewer{1}-linux.gtk.{2}.tgz'
    ).format(ver, ver2, mach)


def trace_url(ver, mach):
    ver2 = ('-' + ver) if ver >= '2019.08' else ''
    return (
        'http://hpctoolkit.org/download/hpcviewer/{0}/'
        'hpctraceviewer{1}-linux.gtk.{2}.tgz'
    ).format(ver, ver2, mach)


class Hpcviewer(Package):
    """Binary distribution of hpcviewer and hpctraceviewer for the Rice
    HPCToolkit (Linux x86_64, ppc64le and aarch64).  Note: hpctoolkit
    databases are platform independent, so you don't need to install
    hpctoolkit to run the viewers and it's common to run hpcrun and
    hpcviewer on different machines."""

    homepage = "http://hpctoolkit.org"
    maintainers = ['mwkrentel']

    viewer_sha = {
        ('2021.03', 'aarch64'): '1b1f7f51a319a159aa96dee21b2cd77ee23b01df263ea122980fa1567e4dab8d',
        ('2021.03', 'ppc64le'): '8fc4683a9e61263ac78fe35391930b0cdc8e84dd50f8d41dcd0c6d8072b02937',
        ('2021.03', 'x86_64'):  '40b4453fe662b896a853d869486b481ded0d29abdf5e50aab2d8f3bdf8940b04',
        ('2021.01', 'aarch64'): 'fe797a1c97943f7509c36a570198291e674cd4a793c1d6538a2761d66542dc52',
        ('2021.01', 'ppc64le'): 'ba4035de2ae208280c3744000ea08d2d7f8c31bd7095f722e442ddc289648063',
        ('2021.01', 'x86_64'):  '99eba4e1c613203c4658f2874d0e79e1620db7a22ac7dcb810801886ba9f8a79',
        ('2020.12', 'ppc64le'): 'ce0d741aa8849621c03183dbf11a0dc1f6d296e3de80e25976a7f2a2750899c4',
        ('2020.12', 'x86_64'):  '29c5e1427893f0652e863fd6d54a8585077662597e5073532ec9f3b116626498',
        ('2020.07', 'x86_64'):  '19951662626c7c9817c4a75269c85810352dc48ae9a62dfb6ce4a5b502de2118',
        ('2020.07', 'ppc64'):   '3f5d9358ef8ff9ba4f6dcaa4d7132f41ba55f0c132d9fd1e2f6da18341648a4e',
        ('2020.07', 'ppc64le'): 'e236a8578dc247279d1021aa35bac47e2d4864b906efcef76c0610ee0086b353',
        ('2020.05', 'x86_64'):  '27f99c94a69abd005303fb58360b0d1b3eb7d223cab81c38ae6ccdd83ec15106',
        ('2020.05', 'ppc64'):   '469bce07a75476c132d3791ca49e38db015917c9c36b4810e477bc1c54a13d68',
        ('2020.05', 'ppc64le'): 'fc4491bf6d9eaf2b7f2d39b722c978597a881ece557fb05a4cf27caabb9e0b99',
        ('2020.04', 'x86_64'):  '5944c7b1e518b25d143df72b06a69cffb0bfc92186eb5efee2178fc2814a0b8b',
        ('2020.04', 'ppc64'):   'ba60615a550aa77a17eb94272b62365a22298cebc6dc2cb7463686741e58d874',
        ('2020.04', 'ppc64le'): '128494077979b447875ed730f1e8c5470fafcd52ae6debe61625031248d91f7c',
        ('2020.02', 'x86_64'):  'af1f514547a9325aee30eb891b31e38c7ea3f33d2d1978b44f83e7daa3d5de6b',
        ('2020.02', 'ppc64'):   '7bb4926202db663aedd5a6830778c5f73f6b08a65d56861824ea95ba83b1f59c',
        ('2020.02', 'ppc64le'): 'cfcebb7ba301affd6d21d2afd43c540e6dd4c5bc39b0d20e8bd1e4fed6aa3481',
        ('2020.01', 'x86_64'):  '3cd5a2a382cec1d64c8bd0abaf2b1461dcd4092a4b4074ddbdc1b96d2a0b4220',
        ('2020.01', 'ppc64'):   '814394a5f410033cc1019526c268ef98b5b381e311fcd39ae8b2bde6c6ff017c',
        ('2020.01', 'ppc64le'): 'e830e956b8088c415fb25ef44a8aca16ebcb27bcd34536866612343217e3f9e4',
        ('2019.12', 'x86_64'):  '6ba149c8d23d9913291655602894f7a91f9c838e69ae5682fd7b605467255c2d',
        ('2019.12', 'ppc64'):   '787257272381fac26401e1013952bea94635172503e7abf8063081fe03f08384',
        ('2019.12', 'ppc64le'): 'fd20891fdae6dd5c2313cdd98e53c52023a0cf146a1121d0c889ebedc08a8bb9',
        ('2019.09', 'x86_64'):  '40982a43880fe646b7f9d03ac4911b55f8a4464510eb8c7304ffaf4d4205ecc6',
        ('2019.09', 'ppc64'):   '3972d604bd160c058185b6f8f3f3a63c4031046734b29cc386c24e40831e6798',
        ('2019.09', 'ppc64le'): 'c348f442b7415aadb94ead06bd35e96442a49a9768fd8c972ca707d77d61e0c3',
        ('2019.08', 'x86_64'):  '249aae6a23dca19286ee15909afbeba5e515388f1c1ad87f572454534fccb9f2',
        ('2019.08', 'ppc64'):   'f91b4772c92c05a4a35c88eec094604f3c233c7233adeede97acba38592da379',
        ('2019.08', 'ppc64le'): 'b1bd5c76b37f225a01631193e0a62524bd41a54b3354a658fdfd0f66c444cc28',
        ('2019.07', 'x86_64'):  'e999781d6a7d178cb1db5b549650024fa9b19891e933bac8b0441d24e7bf015c',
        ('2019.07', 'ppc64'):   '057ce0e2d6be5639639f762fb43b116fe31fb855745abaf4ea26bd281cffaab1',
        ('2019.07', 'ppc64le'): '40d6928e0761568168f3ce34f3ed320916ea60bda830dd74513897ef77386b28',
        ('2019.04', 'x86_64'):  'c524498ef235171e298c8142b7e73b0a1f7c433f9c471fb692d31f0685e53aa4',
        ('2019.04', 'ppc64'):   'dc9daee886ba72c0615db909860ee1aed0979f12c0d113efbe721ddabdf55199',
        ('2019.04', 'ppc64le'): 'dddabccef156996d390653639096ad3e27b7384a5754f42084f50c4a50a9009b',
        ('2019.02', 'x86_64'):  'e24368a3ec27b82736a781971a8371abfe7744b2a4f68b7b41d76f84af306b83',
        ('2019.02', 'ppc64'):   '72c1ef1a5682c3273e900bb248f126428a02dfe728af0c49c7ee8381938d1e18',
        ('2019.02', 'ppc64le'): '02aaf27bb5b0f72d5b5738289bce60f6ef0ef7327ca96a890892509a09adc946',
    }

    trace_sha = {
        ('2020.07', 'x86_64'):  '52aea55b1d40b9453c106ac5a83020a08839b9be1e71dbd1a9f471e5f3a55d43',
        ('2020.07', 'ppc64'):   '3d9222310a18618704015aecbcab7f7c5a2cedbd5ecd8ace1bfc7e98d11b8d36',
        ('2020.07', 'ppc64le'): '2f0a8b95033a5816d468b87c8c139f08a307714e2e27a1cb4a35e1c5a8083cca',
        ('2020.05', 'x86_64'):  'a0b925099a00c10fcb38e937068e50937175fd46dc086121525e546a63a7fd83',
        ('2020.05', 'ppc64'):   '40526f62f36e5b6438021c2b557256638d41a6b8f4e101534b5230ac644a9b85',
        ('2020.05', 'ppc64le'): 'c16e83b59362adcebecd4231374916a2b3a3c016f75a45b24e8398f777a24f89',
        ('2020.04', 'x86_64'):  '695f7a06479c2b6958a6ebc3985b7ed777e7e126c04424ce980b224690f769f3',
        ('2020.04', 'ppc64'):   '78cfadaf7bc6130cc4257241499b36f4f1c47f22d0daa29f5e733ca824a87b3c',
        ('2020.04', 'ppc64le'): '28c225023accbc85a19c6d8fdcc14dae64a475ed5de2b94f18e58aab4edd2c09',
        ('2020.02', 'x86_64'):  'b7b634e91108aa50a2e8647ac6bac87df775ae38aff078545efaa84735e0a666',
        ('2020.02', 'ppc64'):   'a3e845901689e1b32bc6ab2826c6ac6ed352df4839090fa530b20f747e6e0957',
        ('2020.02', 'ppc64le'): 'a64a283f61e706d988952a7cede9fac0328b09d2d0b64e4c08acc54e38781c98',
        ('2020.01', 'x86_64'):  '9459177a2445e85d648384e2ccee20524592e91a74d615262f32d0876831cd7c',
        ('2020.01', 'ppc64'):   '02366a2ba30b9b2450d50cf44933288f04fae5bf9868eef7bb2ae1b49d4f454e',
        ('2020.01', 'ppc64le'): '39970e84e397ed96bc994e7b8db3b7b3aab4e3155fa7ca8e68b9274bb58115f0',
        ('2019.12', 'x86_64'):  '6339b36e655e2c2b07af4cb40946f325acc46da3ec590d36069661e69b046a92',
        ('2019.12', 'ppc64'):   'fe4ee5af22a983fa0ddbfbd97fa6676f07492400536e900188455f21e489c59b',
        ('2019.12', 'ppc64le'): '2688ea834c546b9e2c6e9d69d271a62dd00f6bc7ff4cb874563ba8d0ae5824e3',
        ('2019.09', 'x86_64'):  '8d7ce0710570bb8cd424d88cc4b5bfe821330f24fef84bbbbb370fa291b60a14',
        ('2019.09', 'ppc64'):   'dfb3fe8283cbaeaa1653e8c8bf68267a3f25886bc452309b10f88a7b1e713ec6',
        ('2019.09', 'ppc64le'): 'c1b6ab4f6c91e3a226e8629de62e718c92318ffd83d03db3c40678d578b99b20',
        ('2019.08', 'x86_64'):  '6cefed6a397298ab31cadd10831f5d5533d3f634a4a76bb93f686e603a42c5ed',
        ('2019.08', 'ppc64'):   '64ca5605c89dd3065cacaeee4a8e2ac14b47953530711ed9e04666c8435e44e8',
        ('2019.08', 'ppc64le'): 'bee03b5cb2de7e8556cf1249f98ece7848c13a0de6b8ba71786c430da68f7bcc',
        ('2019.07', 'x86_64'):  '267052cf742d12bbe900bc03bc7c47c8e1704fbaad0e1a3fc77b73dc506d5a68',
        ('2019.07', 'ppc64'):   '5ae63d8e2f2edf5c3b982d3663311e4d55f9b378f512926b3ebadab27ba72e22',
        ('2019.07', 'ppc64le'): 'c2883714cbafa5252432c52d1d32ab5f34554b33a9bad20dcd2c0632388fbee5',
        ('2019.04', 'x86_64'):  'f5f908c0e52c97a72af1af8519f4b191298fe52bd811dd06a051b68cd7bcce27',
        ('2019.04', 'ppc64'):   '221683c992e4fe2cd9079ad2ebb531d99d04a3cbb3a8860f795b276b1eaeab19',
        ('2019.04', 'ppc64le'): 'fe539c6a165a72bba6ea7bdb34a90d862d427c4d55095c97794d54e6dd9d3075',
        ('2019.02', 'x86_64'):  '5ff11317a638318295821204ffcb1276e9da1684cd5f298410ae2bf78ce88b6b',
        ('2019.02', 'ppc64'):   '95b2a7d848ecb924591c248f5e47c641646ef90a071db48237ddb96c4b71a8fb',
        ('2019.02', 'ppc64le'): '01a159306e7810efe07157ec823ac6ca7570ec2014c95db599a3f90eee33355c',
    }

    for key in viewer_sha.keys():
        if key[1] == platform.machine():
            version(key[0], url=viewer_url(*key), sha256=viewer_sha[key])

            # Current versions include the viewer and trace viewer in
            # one tar file.  Before 2020.07, the trace viewer was a
            # separate tar file (resource).
            if key in trace_sha:
                resource(name='hpctraceviewer', url=trace_url(*key),
                         sha256=trace_sha[key], placement='TRACE',
                         when='@{0}'.format(key[0]))

    depends_on('java@11:', type=('build', 'run'), when='@2021.0:')
    depends_on('java@8', type=('build', 'run'), when='@:2020.99')

    conflicts('platform=darwin', msg='hpcviewer requires a manual install on MacOS, see homepage')

    # Both hpcviewer and trace viewer have an install script.
    def install(self, spec, prefix):
        args = [
            '--java', spec['java'].home,
            prefix
        ]

        # Sometimes the script is install.sh, sometimes install.
        inst_path = join_path('.', 'install.sh')
        if not os.path.exists(inst_path):
            inst_path = join_path('.', 'install')

        inst = Executable(inst_path)
        inst(*args)

        # Older versions used a separate resource for the traceviewer.
        if os.path.isdir('TRACE'):
            cd('TRACE')
            inst = Executable(inst_path)
            inst(*args)
