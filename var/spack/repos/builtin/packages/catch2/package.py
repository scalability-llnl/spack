# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Catch2(CMakePackage):
    """Catch2 is a multi-paradigm test framework for C++, which also
    supports Objective-C (and maybe C)."""

    homepage = "https://github.com/catchorg/Catch2"
    url      = "https://github.com/catchorg/Catch2/archive/v2.9.1.tar.gz"

    variant('single_header', default=True,
            description='Install a single header only.')

    # - "make install" was added in 1.7.0
    # - pkg-config package was added in 2.0.1
    # - CMake config package was added in 2.1.2
    conflicts('~single_header', when='@:1.6.1')

    version('2.9.1', sha256='0b36488aca6265e7be14da2c2d0c748b4ddb9c70a1ea4da75736699c629f14ac')
    version('2.9.0', sha256='00040cad9b6d6bb817ebd5853ff6dda23f9957153d8c4eedf85def0c9e787c42')
    version('2.8.0', sha256='b567c37446cd22c8550bfeb7e2fe3f981b8f3ab8b2148499a522e7f61b8a481d')
    version('2.7.2', sha256='9f4116da13d8402b5145f95ab91ae0173cd27b804152d3bb2d4f9b6e64852af7')
    version('2.7.1', sha256='04b303517284572c277597004a33c3f8c02a4d12ba73d5a4cb73b4a369dfef0b')
    version('2.7.0', sha256='d4655e87c0ccda5a2e78bf4256fce8036feb969399503dcc8272f4c90347d9c0')
    version('2.6.1', sha256='b57c2d3362102a77955d3cd0181b792c496520349bfefee8379b9d35b8819f80')
    version('2.6.0', sha256='4c94a685557328eb1b0ed1017ca37c3a378742dc03b558cf02267b6ba8579577')
    version('2.5.0', sha256='720c84d18f4dc9eb23379941df2054e7bcd5ff9c215e4d620f8533a130d128ae')
    version('2.4.2', sha256='9f3caf00749f9aa378d40db5a04019c684419457fd56cee625714de1bff45a92')
    version('2.4.1', sha256='e1b559d77bd857cb0f773e3e826ac1d7e016cf14057fd14b9e99ec3b2c6b809f')
    version('2.4.0', sha256='ab176de36b886a33aa745fcf34642eac853bf677bda518a88655dc750c72d756')
    version('2.3.0', sha256='aaf6bbf81ce8522131bae2ea4d013a77b003bbb2017614f5872d5787687f8f5f')
    # releases 2.3.0+ changed to "catch2/catch.hpp" header
    version('2.2.3', sha256='45e5e12cc5a98e098b0960d70c0d99b7168b711e85fb947dcd4d68ec3f8b8826')
    version('2.2.2', sha256='e93aacf012579093fe6b4e686ff0488975cabee1e6b4e4f27a0acd898e8f09fd')
    version('2.2.1', sha256='3938bc896f8de570bc56d25606fc128437ee53590a95cf3e005710176a1a1ce4')
    version('2.1.0', sha256='a8f9805174916c23bf59ed45f72c21ce092e2848c139f4c6d396aeeb5ce2dfb3')
    version('2.0.1', sha256='5f31b93712e65d363f257ad0f0c02cfbed7a3988979d5f320ad7771e513d4cc8')
    version('1.12.1', sha256='9a0b4722a9864fa0728241ecca2e4c1b3de8e60a5d6fe3f92dec7b8bbfbc850d')
    version('1.12.0', sha256='adab7275bddcd8b5ba28478db513371137188beef5ef40489edb1c34fe2bf421')
    version('1.11.0', sha256='b6f30b548aa15e42d299f3fdb15f69df4777c1b20ca24d8d7dee552d76870eff')
    version('1.10.0', sha256='6e5e686c9e83ff92d622dd04281e9893957a812cfc97d2d1028a988e4bc6a31e')
    version('1.9.7', sha256='175245fba4e76dca8528289c0ae23690c2270bd0fde51b8b145a5576cf70e785')
    version('1.9.6', sha256='5dc4b9b38d8755173987bb47af29491656e413b64eb06e1a03cfb9c26bae0a0e')
    version('1.9.5', sha256='6531b3817066ea8ab96e7a7fbda7e68a43134e6e62fdc5d8c394a451d54b1b9b')
    version('1.9.4', sha256='d40a17198b0c45c1f8164e3af71a2ce759e71d08772c9066b36ccd7781fb5e64')
    version('1.9.3', sha256='2e3a48781d7e57cb7afdfc3c189c8a05d99ebb7f62cc8813b63c9b75cd6045dc')
    version('1.9.2', sha256='b42070df2ff568bb407d327c431cfbc19a40bd06a19228956772dc32e8c9eb45')
    version('1.9.1', sha256='d3fd58730471969b46ed234f5995927cf4324b33474c3746bf17ad3cbc40132d')
    version('1.9.0', sha256='acf3d9c864e06866f9993c71017d672fa7b951347402155b365e58e117ec9c2c')
    version('1.8.2', sha256='85e7acf9df4763e7df3e832df393eaf52b52a1d0bfc4ab751566e3bdbe616642')
    version('1.8.1', sha256='12fd706b63251f8fae1c32013815de33decec4e63a4a8f99af0af1fe0690c53d')
    version('1.8.0', sha256='713d6a6d98f7402bcc2d10a00121a37aec284e6b34b34121d2a09fc1c838e5bc')
    version('1.7.2', sha256='4aeca774db0ebbea0f86548e1c742fbc4c67c8cf0da550fbfe3e55efa1cc2178')
    version('1.7.1', sha256='46b289866f9b44c850cc1e48d0ead479494fd8ef0cdb9eda88b1dfd5b990556a')
    version('1.7.0', sha256='55ff8904d1215aadaa003ae50e1ad82747c655004b43bf30c656cb20e1c89050')
    version('1.6.1', sha256='83ad2744529b3b507eee188dba23baf6b5c038fccbbe4b3256172c04420292e4')
    version('1.6.0', sha256='9a7aed27cc58eee0e694135503dcc7fc99c7ec254416cff44fe10166a5f1f68c')
    version('1.5.9', sha256='0ba04d0eefcf5a1d4c9e9e79f051f1f93de704ea4429a247f69ec76c2c6647cd')
    version('1.5.0', sha256='bbf0ce7f72a1a8892956bc4caba9ead930b8662d908baa0b2e2ec6b164307d22')
    version('1.4.0', sha256='57512b298ca3e2ff44e87c17c926d5f9edf29e13549480e912fddfab5ba63b74')
    version('1.3.5', sha256='f15730d81b4173fb860ce3561768de7d41bbefb67dc031d7d1f5ae2c07f0a472')
    version('1.3.0', sha256='245f6ee73e2fea66311afa1da59e5087ddab8b37ce64994ad88506e8af28c6ac')

    @when('+single_header')
    def cmake(self, spec, prefix):
        pass

    @when('+single_header')
    def build(self, spec, prefix):
        pass

    @when('+single_header')
    def install(self, spec, prefix):
        mkdirp(prefix.include)
        if spec.satisfies('@2.3.0:'):
            install_tree('single_include', prefix.include)
        else:
            install(join_path('single_include', 'catch.hpp'), prefix.include)
        # fakes out spack so it installs a module file
        mkdirp(join_path(prefix, 'bin'))
