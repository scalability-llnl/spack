# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import re


class Findutils(AutotoolsPackage, GNUMirrorPackage):
    """The GNU Find Utilities are the basic directory searching
       utilities of the GNU operating system."""

    homepage = "https://www.gnu.org/software/findutils/"
    gnu_mirror_path = "findutils/findutils-4.8.0.tar.xz"

    def url_for_version(self, version):
        # Before 4.7.0 it used tar.gz instead of tar.xz
        if version < Version("4.7.0"):
            self.gnu_mirror_path = "findutils/findutils-{0}.tar.gz".format(version)

        return super(Findutils, self).url_for_version(version)

    executables = ['^find$']

    version('4.8.0',  sha256='57127b7e97d91282c6ace556378d5455a9509898297e46e10443016ea1387164')
    version('4.7.0',  sha256='c5fefbdf9858f7e4feb86f036e1247a54c79fc2d8e4b7064d5aaa1f47dfa789a')
    version('4.6.0',  sha256='ded4c9f73731cd48fec3b6bdaccce896473b6d8e337e9612e16cf1431bb1169d')
    version('4.4.2',  sha256='434f32d171cbc0a5e72cfc5372c6fc4cb0e681f8dce566a0de5b6fccd702b62a')
    version('4.4.1',  sha256='77a5b85d7fe0dd9c1093e010b61f765707364ec2c89c4f432c1c616215bcc138')
    version('4.4.0',  sha256='fb108c2959f17baf3559da9b3854495b9bb69fb13309fdd05576c66feb661ea9')
    version('4.2.33', sha256='813cd9405aceec5cfecbe96400d01e90ddad7b512d3034487176ce5258ab0f78')
    version('4.2.32', sha256='87bd8804f3c2fa2fe866907377afd8d26a13948a4bb1761e5e95d0494a005217')
    version('4.2.31', sha256='e0d34b8faca0b3cca0703f6c6b498afbe72f0ba16c35980c10ec9ef7724d6204')
    version('4.2.30', sha256='344b9cbb4034907f80398c6a6d3724507ff4b519036f13bb811d12f702043af4')
    version('4.2.29', sha256='1a9ed8db0711f8419156e786b6aecd42dd05df29e53e380d8924e696f7071ae0')
    version('4.2.28', sha256='aa27de514b44eb763d276ad8f19fef31a07bd63ac7ca6870d2be5cd58de862c8')
    version('4.2.27', sha256='546bc7932e716beaa960116766ea4d890f292c6fbde221ec10cdd8ec37329654')
    version('4.2.26', sha256='74fa9030b97e074cbeb4f6c8ec964c5e8292cf5a62b195086113417f75ab836a')
    version('4.2.25', sha256='a2bc59e80ee599368584f4ac4a6e647011700e1b5230e65eb3170c603047bb51')
    version('4.2.23', sha256='d3ca95bf003685c3c34eb59e41c5c4b366fb582a53c4cfa9da0424d98ff23be3')
    version('4.2.20', sha256='4e4d72a4387fcc942565c45460e632001db6bde0a46338a6a1b59b956fd3e031')
    version('4.2.18', sha256='05c33f3e46fa11275f89ae968af70c83b01a2c578ec4fa5abf5c33c7e4afe44d')
    version('4.2.15', sha256='5ede832e70c1691a59e6d5e5ebc2b843120d631b93cd60b905b2edeb078d3719')
    version('4.1.20', sha256='8c5dd50a5ca54367fa186f6294b81ec7a365e36d670d9feac62227cb513e63ab')
    version('4.1',    sha256='487ecc0a6c8c90634a11158f360977e5ce0a9a6701502da6cb96a5a7ec143fac')

    patch('nvhpc.patch', when='%nvhpc')

    build_directory = 'spack-build'

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'find \(GNU findutils\)\s+(\S+)', output)
        return match.group(1) if match else None
