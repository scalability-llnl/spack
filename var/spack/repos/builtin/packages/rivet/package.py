# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Rivet(AutotoolsPackage):
    """Rivet - the particle-physics MC analysis toolkit"""

    homepage = "https://rivet.hepforge.org/"
    url      = "https://rivet.hepforge.org/downloads/?f=Rivet-3.1.2.tar.bz2"

    tags = ['hep']

    version('3.1.3',  sha256='53ddce41705b9c22b2eaa90603f6659aa9bf46c466d8772ca9dbe4430972e021')
    version('3.1.2',  sha256='c041d09644f4eae7c212d82237033267fbc1583dfbb4e3e67377f86cece9577a')
    version('3.1.1',  sha256='7c98b26af5f859bc65200499d15765e4b056b4cf233b34176f27a7e6bc4cf9b1')
    version('3.1.0',  sha256='4e156daee5eb10bd1573ef32d4a6a6df74788cd9180fc977db93ef4cb281000c')
    version('3.0.2',  sha256='9624d6cdcad77eafde40312cf6a1c97f4263f22faf9244b198c140b2c256d2f3')
    version('3.0.1',  sha256='e7551168b86a05c9c029c319c313a0aa142a476195e7ff986c896c1b868f89dd')
    version('3.0.0',  sha256='3944434d3791dccb54f7b2257589df6252cc7c065ce9deb57fbef466ff9e62b1')
    version('2.7.2b', sha256='e9f0a709f8226cde54f9406d36efab1e1b8ed0c6574fbcb1d72a186b09188106', deprecated=True)
    version('2.7.2',  sha256='a6634537c005660e56514b70ab9efb9d466c50685d6fb45ed03e9e1988479f02', deprecated=True)
    version('2.7.1',  sha256='b4145d8369b8a9fa0ada7ba2e5a2e9992d8e4a12ca4874d835246d2e708cbdef', deprecated=True)
    version('2.7.0',  sha256='34ad6a0b47dc4736feac8580a275e8b3a46df8fbeefd91e813add0a1525aacaf', deprecated=True)
    version('2.6.2',  sha256='9dde49d5c02038a295f03d2972f85be8746205bdb5ca1eab868b2c9129ade37a', deprecated=True)
    version('2.6.1',  sha256='e490d1f35aafa3e175690ae92f862c07a5fe2c51f693c88c87789f0441c89022', deprecated=True)
    version('2.6.0',  sha256='fb3229dccd31ea40b0af09974253073f6ad0a3a97e9a0cf44b53748ea8e2f900', deprecated=True)
    version('2.5.4',  sha256='772252193698d994fd111f790e72a4024df7572d492e3d5a9e840a074c5527e2', deprecated=True)
    version('2.5.3',  sha256='99e10330564ac479c6637d317c08882889a272db8ee204ad45a6ee1dcb291de4', deprecated=True)
    version('2.5.2',  sha256='70aa27764a14159c94c0b753a0c3d3600ac669def398cb2d8a6c63ae17704f05', deprecated=True)
    version('2.5.1',  sha256='14ee5828de217e96a30e666192515a2083afee030d81d36fc6bea948e9f7810a', deprecated=True)
    version('2.5.0',  sha256='c59ff35715be0caf65d6ba808b3badad0f6f7e7758f2049fb6ba43ed579bd4af', deprecated=True)
    version('2.4.3',  sha256='18aafecab6c3baeac871a9743946433c2dc01825d8fe291b157719a15c342682', deprecated=True)
    version('2.4.2',  sha256='accb146f3082719781a51eec879427c31401577c44f60b27ec8450102fe68aff', deprecated=True)
    version('2.4.1',  sha256='c14f0f58d1792d84d62c62b44ebb94db004776feba83fd8186bba898d55123cf', deprecated=True)
    version('2.4.0',  sha256='5ee2f34a277ed058b8aef750d946b40d4cf781023b9adab03ca95e803a39fb06', deprecated=True)
    version('2.3.0',  sha256='dd07702981d586e4b97b0fa56ae08cd08a631a952322a9b52e7622a46a7741ab', deprecated=True)
    version('2.2.1',  sha256='9e64ba19d567bdf4d0cc42b435491c4363b5fec90170d034445a99a1e752b691', deprecated=True)
    version('2.2.0',  sha256='3bdafe2007ff54c4734e0c8bc6ba9dc97028d4c41d538201b9582a869af8ae1a', deprecated=True)
    version('2.1.2',  sha256='40a20c1ee186326e5bfd906e0bc88f16dc740551be9cc274e9a826873d9c1eed', deprecated=True)
    version('2.1.1',  sha256='eefa936de6f6c34a6bab39899841f3189d7621c8ba227032f0f32e6e20dfcf85', deprecated=True)
    version('2.1.0',  sha256='58a1ca7b5a47719933782c050e67d0eb3823a7384cfc3c434fece41724c307e6', deprecated=True)
    version('2.0.0',  sha256='038f81f92fbba001ed23b56c1229a4f3b41e0c32e00bc92ea58d042909e3855a', deprecated=True)
    version('1.9.0',  sha256='55ef552b351328c287194aa99fa2b797e6632dc3fa88dfccd58264602012e044', deprecated=True)
    version('1.8.3',  sha256='aa82742fd4d7c68bfbef1367c4c605e06f9fed479a753db96aa6659407fcc4fd', deprecated=True)
    version('1.8.2',  sha256='56be98d31693253543f3e657c8f8edc7979c89fdb0ede1bdddfb3a9f5d4cfc3a', deprecated=True)
    version('1.8.1',  sha256='7e06d22350bec30220186e796caa93e9bfebd8d771a7efd35673897248437c61', deprecated=True)
    version('1.8.0',  sha256='7b28f9163f74583b1542b87c48f28a3ad1338da6136d8e3ca0aeba21095f5fe0', deprecated=True)
    version('1.7.0',  sha256='180741f590f210474b686d60241ad59e008221751ead21f0950c59aff93e54fd', deprecated=True)
    version('1.6.0',  sha256='1affd9e779f48477402e4150f315b3179204cbbc920db2d0129cd9c38bd18b26', deprecated=True)
    version('1.5.1',  sha256='9f24e9824286d5b0302c7e440f4803a8e3b8da50e1260e78c3b3c2eb587b317a', deprecated=True)
    version('1.5.0',  sha256='b7fe63e8caacc5c038ab567fe505d275288eedaa1aed6c379057629eef126006', deprecated=True)
    version('1.4.0',  sha256='067c94659bb7859904e20e72a676f94f103e6e012b7dba8071f51e8a6e624dbb', deprecated=True)
    version('1.3.0',  sha256='5ce41c8492c2fcf809a7135bf8335a01a98ea85fb556b3d00bd4260151efd12f', deprecated=True)
    version('1.2.1',  sha256='2d0380b819f778d8d9c2a462af90bd6a6188121e4edcc6202d936130b59bab17', deprecated=True)
    version('1.2.0',  sha256='ff5869f6dc9465f429e54686e12c39becac57a83273542179a59bac7561b6404', deprecated=True)
    version('1.1.3',  sha256='4be3cd9e6f808cdc5511991be2756f5fa838b6ecd01806fdbe7aec0aa382f946', deprecated=True)
    version('1.1.2',  sha256='a15b5d3339481446dec1b719d7d531a87a2e9d11c9fe8044e270ea69611b07c8', deprecated=True)
    version('1.1.1',  sha256='bd87fefee6bb8368216755342dc80ab3f8f3c813732dd03c6f94135d45f7036b', deprecated=True)

    variant('hepmc', default='2', values=('2', '3'),
            description="HepMC version to link against")

    conflicts('hepmc=3', when='@:2.99', msg='HepMC support was added in 3.0')

    # According to A. Buckley (main Rivet developer):
    # "typically a given Rivet version will work with
    # all YODA releases of that middle-digit version,
    # and maybe older. Generally it's always a good idea
    # to be using the latest versions of both.". The versions below
    # are taken from LCG stack which, in most cases, is the definition
    # of "latest" at the moment of release.
    depends_on('yoda@1.0.4', when='@2.0.0')
    depends_on('yoda@1.0.5', when='@2.1.0')
    depends_on('yoda@1.0.6', when='@2.1.1')
    depends_on('yoda@1.1.0', when='@2.1.2')
    depends_on('yoda@1.3.0', when='@2.2.0')
    depends_on('yoda@1.3.1', when='@2.2.1')
    depends_on('yoda@1.4.0', when='@2.3.0')
    depends_on('yoda@1.5.5', when='@2.4.0')
    depends_on('yoda@1.5.9', when='@2.4.2')
    depends_on('yoda@1.6.1', when='@2.4.3')
    depends_on('yoda@1.6.2', when='@2.5.0')
    depends_on('yoda@1.6.3', when='@2.5.1')
    depends_on('yoda@1.6.5', when='@2.5.2')
    depends_on('yoda@1.6.6', when='@2.5.3')
    depends_on('yoda@1.6.7', when='@2.5.4')
    depends_on('yoda@1.7.1', when='@2.6.1')
    depends_on('yoda@1.7.4', when='@2.6.2')
    depends_on('yoda@1.7.5', when='@2.7.2')
    depends_on('yoda@1.7.5', when='@2.7.2b')
    depends_on('yoda@1.7.7', when='@3.0.1')
    depends_on('yoda@1.8.0', when='@3.1.0')
    depends_on('yoda@1.8.2', when='@3.1.1')
    depends_on('yoda@1.8.3', when='@3.1.2')
    depends_on('yoda@1.8.5', when='@3.1.3')

    # The following versions were not a part of LCG stack
    # and thus the exact version of YODA is unknown
    depends_on('yoda@1.7.0:1.7.999', when='@2.6.0,2.7.0,2.7.1,3.0.0,3.0.2')
    depends_on('yoda@1.5.0:1.5.999', when='@2.4.1')

    depends_on('hepmc',  type=('build', 'run'), when='hepmc=2')
    depends_on('hepmc3', type=('build', 'run'), when='hepmc=3')
    depends_on('boost', when='@:2.5.0', type=('build', 'run'))
    depends_on('fastjet', type=('build', 'run'))
    depends_on('fjcontrib', type=('build', 'run'), when='@3.0.0:')
    depends_on('gsl', type=('build', 'run'), when='@:2.6.0,2.6.2:2.99.99')
    depends_on('python', type=('build', 'run'))
    depends_on('py-cython@0.24.0:', type='build')
    depends_on('swig', type=('build', 'run'))
    depends_on('yaml-cpp', when='@2.0.0:2.1.2', type=('build', 'run'))

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    patch('rivet-1.8.2.patch', when='@1.8.2', level=0)
    patch('rivet-1.9.0.patch', when='@1.9.0', level=0)
    patch('rivet-2.2.0.patch', when='@2.2.0', level=0)
    patch('rivet-2.2.1.patch', when='@2.2.1', level=0)
    patch('rivet-2.4.0.patch', when='@2.4.0', level=0)
    patch('rivet-2.4.2.patch', when='@2.4.2', level=0)
    patch('rivet-2.4.3.patch', when='@2.4.3', level=0)
    patch('rivet-2.5.1.patch', when='@2.5.1', level=0)
    patch('rivet-2.5.2.patch', when='@2.5.2', level=0)
    patch('rivet-2.5.3.patch', when='@2.5.3', level=0)
    patch('rivet-2.5.4.patch', when='@2.5.4', level=0)
    patch('rivet-2.6.0.patch', when='@2.6.0', level=0)
    patch('rivet-2.6.1.patch', when='@2.6.1', level=0)
    patch('rivet-2.6.2.patch', when='@2.6.2', level=0)
    patch('rivet-2.7.0.patch', when='@2.7.0', level=0)
    patch('rivet-3.0.0.patch', when='@3.0.0', level=0)
    patch('rivet-3.0.1.patch', when='@3.0.1', level=0)
    patch('rivet-3.1.0.patch', when='@3.1.0', level=0)
    patch('rivet-3.1.1.patch', when='@3.1.1', level=0)

    @run_before('configure')
    def copy_gsl_m4(self):
        if self.spec.satisfies('@2.6.2:'):
            copy(join_path(os.path.dirname(__file__), 'gsl.m4'), 'm4/gsl.m4')

    @property
    def force_autoreconf(self):
        return self.version >= Version('2.6.2')

    def setup_build_environment(self, env):
        # this avoids an "import site" error in the build
        env.unset('PYTHONHOME')
        fjcontrib_home = self.spec['fjcontrib'].prefix
        env.prepend_path('LD_LIBRARY_PATH', fjcontrib_home.lib)

    def flag_handler(self, name, flags):
        if self.spec.satisfies('@3.1.2:') and name == 'cxxflags':
            flags.append('-faligned-new')
            return (None, None, flags)
        return (flags, None, None)

    def configure_args(self):
        args = []
        if self.spec.variants['hepmc'].value == '2':
            args += ['--with-hepmc=' + self.spec['hepmc'].prefix]
        else:
            args += ['--with-hepmc3=' + self.spec['hepmc'].prefix]

        if self.spec.satisfies('@:1.999.999'):
            args += ['--with-boost-incpath=' + self.spec['boost'].includes]
        else:
            if self.spec.satisfies('@:2.5.0'):
                args += ['--with-boost=' + self.spec['boost'].prefix]

        args += ['--with-fastjet=' + self.spec['fastjet'].prefix]
        if self.spec.satisfies('@2:'):
            args += ['--with-yoda=' + self.spec['yoda'].prefix]

        if self.spec.satisfies('@:2.6.0,2.6.2:2.99.99'):
            args += ['--with-gsl=' + self.spec['gsl'].prefix]

        if self.spec.satisfies('@3.0.0:'):
            args += ['--with-fjcontrib=' + self.spec['fjcontrib'].prefix]

        if self.spec.satisfies('@:2.5.1'):
            args += ['--enable-unvalidated']

        if self.spec.satisfies('@2:2.4.99'):
            args += ['--enable-stdcxx11']

        args += ['--disable-pdfmanual']

        return args
