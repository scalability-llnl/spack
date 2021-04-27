# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import itertools
import re
import os
import sys
import llnl.util.tty as tty


class Openmpi(AutotoolsPackage):
    """An open source Message Passing Interface implementation.

    The Open MPI Project is an open source Message Passing Interface
    implementation that is developed and maintained by a consortium
    of academic, research, and industry partners. Open MPI is
    therefore able to combine the expertise, technologies, and
    resources from all across the High Performance Computing
    community in order to build the best MPI library available.
    Open MPI offers advantages for system and software vendors,
    application developers and computer science researchers.
    """

    homepage = "https://www.open-mpi.org"
    url = "https://download.open-mpi.org/release/open-mpi/v4.1/openmpi-4.1.0.tar.bz2"
    list_url = "https://www.open-mpi.org/software/ompi/"
    git = "https://github.com/open-mpi/ompi.git"

    maintainers = ['hppritcha', 'naughtont3']

    executables = ['^ompi_info$']

    version('master', branch='master')

    # Current
    version('4.1.1', sha256='e24f7a778bd11a71ad0c14587a7f5b00e68a71aa5623e2157bafee3d44c07cda')  # libmpi.so.40.30.1

    # Still supported
    version('4.1.0', sha256='73866fb77090819b6a8c85cb8539638d37d6877455825b74e289d647a39fd5b5')  # libmpi.so.40.30.0
    version('4.0.5', preferred=True, sha256='c58f3863b61d944231077f344fe6b4b8fbb83f3d1bc93ab74640bf3e5acac009')  # libmpi.so.40.20.5
    version('4.0.4', sha256='47e24eb2223fe5d24438658958a313b6b7a55bb281563542e1afc9dec4a31ac4')  # libmpi.so.40.20.4
    version('4.0.3', sha256='1402feced8c3847b3ab8252165b90f7d1fa28c23b6b2ca4632b6e4971267fd03')  # libmpi.so.40.20.3
    version('4.0.2', sha256='900bf751be72eccf06de9d186f7b1c4b5c2fa9fa66458e53b77778dffdfe4057')  # libmpi.so.40.20.2
    version('4.0.1', sha256='cce7b6d20522849301727f81282201d609553103ac0b09162cf28d102efb9709')  # libmpi.so.40.20.1
    version('4.0.0', sha256='2f0b8a36cfeb7354b45dda3c5425ef8393c9b04115570b615213faaa3f97366b')  # libmpi.so.40.20.0

    # Retired
    version('3.1.6', sha256='50131d982ec2a516564d74d5616383178361c2f08fdd7d1202b80bdf66a0d279')  # libmpi.so.40.10.4
    version('3.1.5', sha256='fbf0075b4579685eec8d56d34d4d9c963e6667825548554f5bf308610af72133')  # libmpi.so.40.10.4
    version('3.1.4', sha256='17a69e0054db530c7dc119f75bd07d079efa147cf94bf27e590905864fe379d6')  # libmpi.so.40.10.4
    version('3.1.3', sha256='8be04307c00f51401d3fb9d837321781ea7c79f2a5a4a2e5d4eaedc874087ab6')  # libmpi.so.40.10.3
    version('3.1.2', sha256='c654ed847f34a278c52a15c98add40402b4a90f0c540779f1ae6c489af8a76c5')  # libmpi.so.40.10.2
    version('3.1.1', sha256='3f11b648dd18a8b878d057e9777f2c43bf78297751ad77ae2cef6db0fe80c77c')  # libmpi.so.40.10.1
    version('3.1.0', sha256='b25c044124cc859c0b4e6e825574f9439a51683af1950f6acda1951f5ccdf06c')  # libmpi.so.40.10.0
    version('3.0.5', sha256='f8976b95f305efc435aa70f906b82d50e335e34cffdbf5d78118a507b1c6efe8')  # libmpi.so.40.00.5
    version('3.0.4', sha256='2ff4db1d3e1860785295ab95b03a2c0f23420cda7c1ae845c419401508a3c7b5')  # libmpi.so.40.00.5
    version('3.0.3', sha256='fb228e42893fe6a912841a94cd8a0c06c517701ae505b73072409218a12cf066')  # libmpi.so.40.00.4
    version('3.0.2', sha256='d2eea2af48c1076c53cabac0a1f12272d7470729c4e1cb8b9c2ccd1985b2fb06')  # libmpi.so.40.00.2
    version('3.0.1', sha256='663450d1ee7838b03644507e8a76edfb1fba23e601e9e0b5b2a738e54acd785d')  # libmpi.so.40.00.1
    version('3.0.0', sha256='f699bff21db0125d8cccfe79518b77641cd83628725a1e1ed3e45633496a82d7')  # libmpi.so.40.00.0

    version('2.1.6', sha256='98b8e1b8597bbec586a0da79fcd54a405388190247aa04d48e8c40944d4ca86e')  # libmpi.so.20.10.3
    version('2.1.5', sha256='b807ccab801f27c3159a5edf29051cd3331d3792648919f9c4cee48e987e7794')  # libmpi.so.20.10.3
    version('2.1.4', sha256='3e03695ca8bd663bc2d89eda343c92bb3d4fc79126b178f5ddcb68a8796b24e2')  # libmpi.so.20.10.3
    version('2.1.3', sha256='285b3e2a69ed670415524474496043ecc61498f2c63feb48575f8469354d79e8')  # libmpi.so.20.10.2
    version('2.1.2', sha256='3cc5804984c5329bdf88effc44f2971ed244a29b256e0011b8deda02178dd635')  # libmpi.so.20.10.2
    version('2.1.1', sha256='bd7badd4ff3afa448c0d7f3ca0ee6ce003b957e9954aa87d8e4435759b5e4d16')  # libmpi.so.20.10.1
    version('2.1.0', sha256='b169e15f5af81bf3572db764417670f508c0df37ce86ff50deb56bd3acb43957')  # libmpi.so.20.10.0

    version('2.0.4', sha256='4f82d5f7f294becbd737319f74801206b08378188a95b70abe706fdc77a0c20b')  # libmpi.so.20.0.4
    version('2.0.3', sha256='b52c0204c0e5954c9c57d383bb22b4181c09934f97783292927394d29f2a808a')  # libmpi.so.20.0.3
    version('2.0.2', sha256='cae396e643f9f91f0a795f8d8694adf7bacfb16f967c22fb39e9e28d477730d3')  # libmpi.so.20.0.2
    version('2.0.1', sha256='fed74f4ae619b7ebcc18150bb5bdb65e273e14a8c094e78a3fea0df59b9ff8ff')  # libmpi.so.20.0.1
    version('2.0.0', sha256='08b64cf8e3e5f50a50b4e5655f2b83b54653787bd549b72607d9312be44c18e0')  # libmpi.so.20.0.0

    # Ancient
    version('1.10.7', sha256='a089ece151fec974905caa35b0a59039b227bdea4e7933069e94bee4ed0e5a90')  # libmpi.so.12.0.7
    version('1.10.6', sha256='65606184a084a0eda6102b01e5a36a8f02d3195d15e91eabbb63e898bd110354')  # libmpi.so.12.0.6
    version('1.10.5', sha256='a95fa355ed3a905c7c187bc452529a9578e2d6bae2559d8197544ab4227b759e')  # libmpi.so.12.0.5
    version('1.10.4', sha256='fb3c0c4c77896185013b6091b306d29ba592eb40d8395533da5c8bc300d922db')  # libmpi.so.12.0.4
    version('1.10.3', sha256='7484bb664312082fd12edc2445b42362089b53b17fb5fce12efd4fe452cc254d')  # libmpi.so.12.0.3
    version('1.10.2', sha256='8846e7e69a203db8f50af90fa037f0ba47e3f32e4c9ccdae2db22898fd4d1f59')  # libmpi.so.12.0.2
    version('1.10.1', sha256='7919ecde15962bab2e26d01d5f5f4ead6696bbcacb504b8560f2e3a152bfe492')  # libmpi.so.12.0.1
    version('1.10.0', sha256='26b432ce8dcbad250a9787402f2c999ecb6c25695b00c9c6ee05a306c78b6490')  # libmpi.so.12.0.0

    version('1.8.8', sha256='a28382d1e6a36f4073412dc00836ff2524e42b674da9caf6ca7377baad790b94')  # libmpi.so.1.6.3
    version('1.8.7', sha256='da629e9bd820a379cfafe15f842ee9b628d7451856085ccc23ee75ab3e1b48c7')  # libmpi.so.1.6.2
    version('1.8.6', sha256='b9fe3bdfb86bd42cc53448e17f11278531b989b05ff9513bc88ba1a523f14e87')  # libmpi.so.1.6.1
    version('1.8.5', sha256='4cea06a9eddfa718b09b8240d934b14ca71670c2dc6e6251a585ce948a93fbc4')  # libmpi.so.1.6.0
    version('1.8.4', sha256='23158d916e92c80e2924016b746a93913ba7fae9fff51bf68d5c2a0ae39a2f8a')  # libmpi.so.1.6.0
    version('1.8.3', sha256='2ef02dab61febeb74714ff80d508c00b05defc635b391ed2c8dcc1791fbc88b3')  # libmpi.so.1.6.0
    version('1.8.2', sha256='ab70770faf1bac15ef44301fe2186b02f857646545492dd7331404e364a7d131')  # libmpi.so.1.5.2
    version('1.8.1', sha256='171427ebc007943265f33265ec32e15e786763952e2bfa2eac95e3e192c1e18f')  # libmpi.so.1.5.0
    version('1.8',   sha256='35d5db86f49c0c64573b2eaf6d51c94ed8a06a9bb23dda475e602288f05e4ecf')  # libmpi.so.1.5.0

    version('1.7.5', sha256='cb3eef6880537d341d5d098511d390ec853716a6ec94007c03a0d1491b2ac8f2')  # libmpi.so.1.4.0
    version('1.7.4', sha256='ff8e31046c5bacfc6202d67f2479731ccd8542cdd628583ae75874000975f45c')  # libmpi.so.1.3.0
    version('1.7.3', sha256='438d96c178dbf5a1bc92fa1d238a8225d87b64af26ce2a07789faaf312117e45')  # libmpi.so.1.2.0
    version('1.7.2', sha256='82a1c477dcadad2032ab24d9be9e39c1042865965841911f072c49aa3544fd85')  # libmpi.so.1.1.2
    version('1.7.1', sha256='554583008fa34ecdfaca22e46917cc3457a69cba08c29ebbf53eef4f4b8be171')  # libmpi.so.1.1.1
    version('1.7',   sha256='542e44aaef6546798c0d39c0fd849e9fbcd04a762f0ab100638499643253a513')  # libmpi.so.1.1.0

    version('1.6.5', sha256='fe37bab89b5ef234e0ac82dc798282c2ab08900bf564a1ec27239d3f1ad1fc85')  # libmpi.so.1.0.8
    version('1.6.4', sha256='40cb113a27d76e1e915897661579f413564c032dc6e703073e6a03faba8093fa')  # libmpi.so.1.0.7
    version('1.6.3', sha256='0c30cfec0e420870630fdc101ffd82f7eccc90276bc4e182f8282a2448668798')  # libmpi.so.1.0.6
    version('1.6.2', sha256='5cc7744c6cc4ec2c04bc76c8b12717c4011822a2bd7236f2ea511f09579a714a')  # libmpi.so.1.0.3
    version('1.6.1', sha256='077240dd1ab10f0caf26931e585db73848e9815c7119b993f91d269da5901e3a')  # libmpi.so.1.0.3
    version('1.6',   sha256='6e0d8b336543fb9ab78c97d364484923167857d30b266dfde1ccf60f356b9e0e')  # libmpi.so.1.0.3

    version('1.5.5', sha256='660e6e49315185f88a87b6eae3d292b81774eab7b29a9b058b10eb35d892ff23')  # libmpi.so.1.0.3
    version('1.5.4', sha256='81126a95a51b8af4bb0ad28790f852c30d22d989713ec30ad22e9e0a79587ef6')  # libmpi.so.1.0.2
    version('1.5.3', sha256='70745806cdbe9b945d47d9fa058f99e072328e41e40c0ced6dd75220885c5263')  # libmpi.so.1.0.1
    version('1.5.2', sha256='7123b781a9fd21cc79870e7fe01e9c0d3f36935c444922661e24af523b116ab1')  # libmpi.so.1.0.1
    version('1.5.1', sha256='c28bb0bd367ceeec08f739d815988fca54fc4818762e6abcaa6cfedd6fd52274')  # libmpi.so.1.0.0
    version('1.5',   sha256='1882b1414a94917ec26b3733bf59da6b6db82bf65b5affd7f0fcbd96efaca506')  # libmpi.so.1.0.0

    version('1.4.5', sha256='a3857bc69b7d5258cf7fc1ed1581d9ac69110f5c17976b949cb7ec789aae462d')  # libmpi.so.0.0.4
    version('1.4.4', sha256='9ad125304a89232d5b04da251f463fdbd8dcd997450084ba4227e7f7a095c3ed')  # libmpi.so.0.0.3
    version('1.4.3', sha256='220b72b1c7ee35469ff74b4cfdbec457158ac6894635143a33e9178aa3981015')  # libmpi.so.0.0.2
    version('1.4.2', sha256='19129e3d51860ad0a7497ede11563908ba99c76b3a51a4d0b8801f7e2db6cd80')  # libmpi.so.0.0.2
    version('1.4.1', sha256='d4d71d7c670d710d2d283ea60af50d6c315318a4c35ec576bedfd0f3b7b8c218')  # libmpi.so.0.0.1
    version('1.4',   sha256='fa55edef1bd8af256e459d4d9782516c6998b9d4698eda097d5df33ae499858e')  # libmpi.so.0.0.1

    version('1.3.4', sha256='fbfe4b99b0c98f81a4d871d02f874f84ea66efcbb098f6ad84ebd19353b681fc')  # libmpi.so.0.0.1
    version('1.3.3', sha256='e1425853282da9237f5b41330207e54da1dc803a2e19a93dacc3eca1d083e422')  # libmpi.so.0.0.0
    version('1.3.2', sha256='c93ed90962d879a2923bed17171ed9217036ee1279ffab0925ea7eead26105d8')  # libmpi.so.0.0.0
    version('1.3.1', sha256='22d18919ddc5f49d55d7d63e2abfcdac34aa0234427e861e296a630c6c11632c')  # libmpi.so.0.0.0
    version('1.3',   sha256='864706d88d28b586a045461a828962c108f5912671071bc3ef0ca187f115e47b')  # libmpi.so.0.0.0

    version('1.2.9', sha256='0eb36abe09ba7bf6f7a70255974e5d0a273f7f32d0e23419862c6dcc986f1dff')  # libmpi.so.0.0.0
    version('1.2.8', sha256='75b286cb3b1bf6528a7e64ee019369e0601b8acb5c3c167a987f755d1e41c95c')  # libmpi.so.0.0.0
    version('1.2.7', sha256='d66c7f0bb11494023451651d0e61afaef9d2199ed9a91ed08f0dedeb51541c36')  # libmpi.so.0.0.0
    version('1.2.6', sha256='e5b27af5a153a257b1562a97bbf7164629161033934558cefd8e1e644a9f73d3')  # libmpi.so.0.0.0
    version('1.2.5', sha256='3c3aed872c17165131c77bd7a12fe8aec776cb23da946b7d12840db93ab79322')  # libmpi.so.0.0.0
    version('1.2.4', sha256='594a3a0af69cc7895e0d8f9add776a44bf9ed389794323d0b1b45e181a97e538')  # libmpi.so.0.0.0
    version('1.2.3', sha256='f936ca3a197e5b2d1a233b7d546adf07898127683b03c4b37cf31ae22a6f69bb')  # libmpi.so.0.0.0
    version('1.2.2', sha256='aa763e0e6a6f5fdff8f9d3fc988a4ba0ed902132d292c85aef392cc65bb524e6')  # libmpi.so.0.0.0
    version('1.2.1', sha256='a94731d84fb998df33960e0b57ea5661d35e7c7cd9d03d900f0b6a5a72e4546c')  # libmpi.so.0.0.0
    version('1.2',   sha256='ba0bfa3dec2ead38a3ed682ca36a0448617b8e29191ab3f48c9d0d24d87d14c0')  # libmpi.so.0.0.0

    version('1.1.5', sha256='913deaedf3498bd5d06299238ec4d048eb7af9c3afd8e32c12f4257c8b698a91')  # libmpi.so.0.0.0
    version('1.1.4', sha256='21c37f85df7e959f17cc7cb5571d8db2a94ed2763e3e96e5d052aff2725c1d18')  # libmpi.so.0.0.0
    version('1.1.3', sha256='c33f8f5e65cfe872173616cca27ae8dc6d93ea66e0708118b9229128aecc174f')  # libmpi.so.0.0.0
    version('1.1.2', sha256='3bd8d9fe40b356be7f9c3d336013d3865f8ca6a79b3c6e7ef28784f6c3a2b8e6')  # libmpi.so.0.0.0
    version('1.1.1', sha256='dc31aaec986c4ce436dbf31e73275ed1a9391432dcad7609de8d0d3a78d2c700')  # libmpi.so.0.0.0
    version('1.1',   sha256='ebe14801d2caeeaf47b0e437b43f73668b711f4d3fcff50a0d665d4bd4ea9531')  # libmpi.so.0.0.0

    version('1.0.2', sha256='ccd1074d7dd9566b73812d9882c84e446a8f4c77b6f471d386d3e3b9467767b8')  # libmpi.so.0.0.0
    version('1.0.1', sha256='f801b7c8ea6c485ac0709a628a479aeafa718a205ed6bc0cf2c684bc0cc73253')  # libmpi.so.0.0.0
    version('1.0',   sha256='cf75e56852caebe90231d295806ac3441f37dc6d9ad17b1381791ebb78e21564')  # libmpi.so.0.0.0

    patch('ad_lustre_rwcontig_open_source.patch', when="@1.6.5")
    patch('llnl-platforms.patch', when="@1.6.5")
    patch('configure.patch', when="@1.10.1")
    patch('fix_multidef_pmi_class.patch', when="@2.0.0:2.0.1")
    patch('fix-ucx-1.7.0-api-instability.patch', when='@4.0.0:4.0.2')

    # Vader Bug: https://github.com/open-mpi/ompi/issues/5375
    # Haven't release fix for 2.1.x
    patch('btl_vader.patch', when='@2.1.3:2.1.5')

    # Fixed in 3.0.3 and 3.1.3
    patch('btl_vader.patch', when='@3.0.1:3.0.2')
    patch('btl_vader.patch', when='@3.1.0:3.1.2')

    # Make NAG compiler pass the -pthread option to the linker:
    # https://github.com/open-mpi/ompi/pull/6378
    # We support only versions based on Libtool 2.4.6.
    patch('nag_pthread/2.1.4_2.1.999_3.0.1_4.patch', when='@2.1.4:2.1.999,3.0.1:4%nag')
    patch('nag_pthread/2.1.2_2.1.3_3.0.0.patch', when='@2.1.2:2.1.3,3.0.0%nag')
    patch('nag_pthread/2.0.0_2.1.1.patch', when='@2.0.0:2.1.1%nag')
    patch('nag_pthread/1.10.4_1.10.999.patch', when='@1.10.4:1.10.999%nag')

    patch('nvhpc-libtool.patch', when='@develop %nvhpc')
    patch('nvhpc-configure.patch', when='%nvhpc')

    # Fix MPI_Sizeof() in the "mpi" Fortran module for compilers that do not
    # support "IGNORE TKR" functionality (e.g. NAG).
    # The issue has been resolved upstream in two steps:
    #   1) https://github.com/open-mpi/ompi/pull/2294
    #   2) https://github.com/open-mpi/ompi/pull/5099
    # The first one was applied starting version v3.0.0 and backported to
    # v1.10. A subset with relevant modifications is applicable starting
    # version 1.8.4.
    patch('use_mpi_tkr_sizeof/step_1.patch', when='@1.8.4:1.10.6,2:2.999')
    # The second patch was applied starting version v4.0.0 and backported to
    # v2.x, v3.0.x, and v3.1.x.
    patch('use_mpi_tkr_sizeof/step_2.patch', when='@1.8.4:2.1.3,3:3.0.1')
    # To fix performance regressions introduced while fixing a bug in older
    # gcc versions on x86_64, Refs. open-mpi/ompi#8603
    patch('opal_assembly_arch.patch', when='@4.0.0:4.1.1')

    variant(
        'fabrics',
        values=disjoint_sets(
            ('auto',),
            ('psm', 'psm2', 'verbs',
             'mxm', 'ucx', 'ofi',
             'fca', 'hcoll',
             'xpmem', 'cma', 'knem')  # shared memory transports
        ).with_non_feature_values('auto', 'none'),
        description="List of fabrics that are enabled; "
                    "'auto' lets openmpi determine",
    )

    variant(
        'schedulers',
        values=disjoint_sets(
            ('auto',),
            ('alps', 'lsf', 'tm',
             'slurm', 'sge', 'loadleveler')
        ).with_non_feature_values('auto', 'none'),
        description="List of schedulers for which support is enabled; "
                    "'auto' lets openmpi determine",
    )

    # Additional support options
    variant('atomics', default=False, description='Enable built-in atomics')
    variant('java', default=False, description='Build Java support')
    variant('static', default=True, description='Build static libraries')
    variant('sqlite3', default=False, description='Build SQLite3 support')
    variant('vt', default=True, description='Build VampirTrace support')
    variant('thread_multiple', default=False,
            description='Enable MPI_THREAD_MULTIPLE support')
    variant('cuda', default=False, description='Enable CUDA support')
    variant('pmi', default=False, description='Enable PMI support')
    variant('wrapper-rpath', default=True,
            description='Enable rpath support in the wrappers')
    variant('cxx', default=False, description='Enable C++ MPI bindings')
    variant('cxx_exceptions', default=False, description='Enable C++ Exception support')
    variant('gpfs', default=True, description='Enable GPFS support (if present)')
    variant('singularity', default=False,
            description="Build support for the Singularity container")
    variant('lustre', default=False,
            description="Lustre filesystem library support")
    # Adding support to build a debug version of OpenMPI that activates
    # Memchecker, as described here:
    #
    # https://www.open-mpi.org/faq/?category=debugging#memchecker_what
    #
    # This option degrades run-time support, and thus is disabled by default
    variant(
        'memchecker',
        default=False,
        description='Memchecker support for debugging [degrades performance]'
    )

    variant(
        'legacylaunchers',
        default=False,
        description='Do not remove mpirun/mpiexec when building with slurm'
    )
    # Variants to use internal packages
    variant('internal-hwloc', default=False, description='Use internal hwloc')

    provides('mpi')
    provides('mpi@:2.2', when='@1.6.5')
    provides('mpi@:3.0', when='@1.7.5:')
    provides('mpi@:3.1', when='@2.0.0:')

    if sys.platform != 'darwin':
        depends_on('numactl')

    depends_on('autoconf', type='build', when='@develop')
    depends_on('automake', type='build', when='@develop')
    depends_on('libtool',  type='build', when='@develop')
    depends_on('m4',       type='build', when='@develop')

    depends_on('perl',     type='build')
    depends_on('pkgconfig', type='build')

    depends_on('libevent@2.0:', when='@4:')

    depends_on('hwloc@2:', when='@4: ~internal-hwloc')
    # ompi@:3.0.0 doesn't support newer hwloc releases:
    # "configure: error: OMPI does not currently support hwloc v2 API"
    # Future ompi releases may support it, needs to be verified.
    # See #7483 for context.
    depends_on('hwloc@:1.999', when='@:3.999.999 ~internal-hwloc')

    depends_on('hwloc +cuda', when='+cuda ~internal-hwloc')
    depends_on('java', when='+java')
    depends_on('sqlite', when='+sqlite3@:1.11')
    depends_on('zlib', when='@3.0.0:')
    depends_on('valgrind~mpi', when='+memchecker')
    # Singularity release 3 works better
    depends_on('singularity@3.0.0:', when='+singularity')
    depends_on('lustre', when='+lustre')

    depends_on('opa-psm2', when='fabrics=psm2')
    depends_on('rdma-core', when='fabrics=verbs')
    depends_on('mxm', when='fabrics=mxm')
    depends_on('binutils+libiberty', when='fabrics=mxm')
    depends_on('ucx', when='fabrics=ucx')
    depends_on('ucx +thread_multiple', when='fabrics=ucx +thread_multiple')
    depends_on('ucx +thread_multiple', when='@3.0.0: fabrics=ucx')
    depends_on('libfabric', when='fabrics=ofi')
    depends_on('fca', when='fabrics=fca')
    depends_on('hcoll', when='fabrics=hcoll')
    depends_on('xpmem', when='fabrics=xpmem')
    depends_on('knem', when='fabrics=knem')

    depends_on('lsf', when='schedulers=lsf')
    depends_on('openpbs', when='schedulers=tm')
    depends_on('slurm', when='schedulers=slurm')

    depends_on('openssh', type='run')

    # CUDA support was added in 1.7
    conflicts('+cuda', when='@:1.6')
    # PMI support was added in 1.5.5
    conflicts('+pmi', when='@:1.5.4')
    # RPATH support in the wrappers was added in 1.7.4
    conflicts('+wrapper-rpath', when='@:1.7.3')

    conflicts('+cxx', when='@5:',
              msg='C++ MPI bindings are removed in 5.0.X release')
    conflicts('+cxx_exceptions', when='@5:',
              msg='C++ exceptions are removed in 5.0.X release')

    # PSM2 support was added in 1.10.0
    conflicts('fabrics=psm2', when='@:1.8')
    # MXM support was added in 1.5.4
    conflicts('fabrics=mxm', when='@:1.5.3')
    # libfabric (OFI) support was added in 1.10.0
    conflicts('fabrics=ofi', when='@:1.8')
    # fca support was added in 1.5.0 and removed in 5.0.0
    conflicts('fabrics=fca', when='@:1.4,5:')
    # hcoll support was added in 1.7.3:
    conflicts('fabrics=hcoll', when='@:1.7.2')
    # xpmem support was added in 1.7
    conflicts('fabrics=xpmem', when='@:1.6')
    # cma support was added in 1.7
    conflicts('fabrics=cma', when='@:1.6')
    # knem support was added in 1.5
    conflicts('fabrics=knem', when='@:1.4')

    conflicts('schedulers=slurm ~pmi', when='@1.5.4:2.999.999',
              msg='+pmi is required for openmpi(>=1.5.5) to work with SLURM.')
    conflicts('schedulers=loadleveler', when='@3.0.0:',
              msg='The loadleveler scheduler is not supported with '
              'openmpi(>=3.0.0).')
    conflicts('+singularity', when='@5:',
              msg='singularity support has been dropped in OpenMPI 5')

    filter_compiler_wrappers('openmpi/*-wrapper-data*', relative_root='share')

    extra_install_tests = 'examples'

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)(output=str, error=str)
        match = re.search(r'Open MPI: (\S+)', output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version):
        results = []
        for exe in exes:
            variants = ''
            output = Executable(exe)("-a", output=str, error=str)
            # Some of these options we have to find by hoping the
            # configure string is in the ompi_info output. While this
            # is usually true, it's not guaranteed.  For anything that
            # begins with --, we want to use the defaults as provided
            # by the openmpi package in the absense of any other info.

            if re.search(r'--enable-builtin-atomics', output):
                variants += "+atomics"
            match = re.search(r'\bJava bindings: (\S+)', output)
            if match and is_enabled(match.group(1)):
                variants += "+java"
            else:
                variants += "~java"
            if re.search(r'--enable-static', output):
                variants += "+static"
            elif re.search(r'--disable-static', output):
                variants += "~static"
            elif re.search(r'\bMCA (?:coll|oca|pml): monitoring',
                           output):
                # Built multiple variants of openmpi and ran diff.
                # This seems to be the distinguishing feature.
                variants += "~static"
            if re.search(r'\bMCA db: sqlite', output):
                variants += "+sqlite3"
            else:
                variants += "~sqlite3"
            if re.search(r'--enable-contrib-no-build=vt', output):
                variants += '+vt'
            match = re.search(r'MPI_THREAD_MULTIPLE: (\S+?),?', output)
            if match and is_enabled(match.group(1)):
                variants += '+thread_multiple'
            else:
                variants += '~thread_multiple'
            match = re.search(
                r'parameter "mpi_built_with_cuda_support" ' +
                r'\(current value: "(\S+)"',
                output)
            if match and is_enabled(match.group(1)):
                variants += '+cuda'
            else:
                variants += '~cuda'
            match = re.search(r'\bWrapper compiler rpath: (\S+)', output)
            if match and is_enabled(match.group(1)):
                variants += '+wrapper-rpath'
            else:
                variants += '~wrapper-rpath'
            match = re.search(r'\bC\+\+ bindings: (\S+)', output)
            if match and match.group(1) == 'yes':
                variants += '+cxx'
            else:
                variants += '~cxx'
            match = re.search(r'\bC\+\+ exceptions: (\S+)', output)
            if match and match.group(1) == 'yes':
                variants += '+cxx_exceptions'
            else:
                variants += '~cxx_exceptions'
            if re.search(r'--with-singularity', output):
                variants += '+singularity'
            if re.search(r'--with-lustre', output):
                variants += '+lustre'
            match = re.search(r'Memory debugging support: (\S+)', output)
            if match and is_enabled(match.group(1)):
                variants += '+memchecker'
            else:
                variants += '~memchecker'
            if re.search(r'\bMCA (?:ess|prrte): pmi', output):
                variants += '+pmi'
            else:
                variants += '~pmi'

            fabrics = get_options_from_variant(cls, "fabrics")
            used_fabrics = []
            for fabric in fabrics:
                match = re.search(r'\bMCA (?:mtl|btl|pml): %s\b' % fabric,
                                  output)
                if match:
                    used_fabrics.append(fabric)
            if used_fabrics:
                variants += ' fabrics=' + ','.join(used_fabrics) + ' '

            schedulers = get_options_from_variant(cls, "schedulers")
            used_schedulers = []
            for scheduler in schedulers:
                match = re.search(r'\bMCA (?:prrte|ras): %s\b' % scheduler,
                                  output)
                if match:
                    used_schedulers.append(scheduler)
            if used_schedulers:
                variants += ' schedulers=' + ','.join(used_schedulers) + ' '

            # Get the appropriate compiler
            match = re.search(r'\bC compiler absolute: (\S+)', output)
            if match:
                compiler_spec = get_spack_compiler_spec(
                    os.path.dirname(match.group(1)))
                if compiler_spec:
                    variants += "%" + str(compiler_spec)
            results.append(variants)
        return results

    def url_for_version(self, version):
        url = "https://download.open-mpi.org/release/open-mpi/v{0}/openmpi-{1}.tar.bz2"
        return url.format(version.up_to(2), version)

    @property
    def headers(self):
        hdrs = HeaderList(find(self.prefix.include, 'mpi.h', recursive=False))
        if not hdrs:
            hdrs = HeaderList(find(self.prefix, 'mpi.h', recursive=True))
        return hdrs or None

    @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters
        libraries = ['libmpi']

        if 'cxx' in query_parameters:
            libraries = ['libmpi_cxx'] + libraries

        return find_libraries(
            libraries, root=self.prefix, shared=True, recursive=True
        )

    def setup_run_environment(self, env):
        # Because MPI is both a runtime and a compiler, we have to setup the
        # compiler components as part of the run environment.
        env.set('MPICC',  join_path(self.prefix.bin, 'mpicc'))
        env.set('MPICXX', join_path(self.prefix.bin, 'mpic++'))
        env.set('MPIF77', join_path(self.prefix.bin, 'mpif77'))
        env.set('MPIF90', join_path(self.prefix.bin, 'mpif90'))

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_run_environment(env)

        # Use the spack compiler wrappers under MPI
        env.set('OMPI_CC', spack_cc)
        env.set('OMPI_CXX', spack_cxx)
        env.set('OMPI_FC', spack_fc)
        env.set('OMPI_F77', spack_f77)

        # See https://www.open-mpi.org/faq/?category=building#installdirs
        for suffix in ['PREFIX', 'EXEC_PREFIX', 'BINDIR', 'SBINDIR',
                       'LIBEXECDIR', 'DATAROOTDIR', 'DATADIR', 'SYSCONFDIR',
                       'SHAREDSTATEDIR', 'LOCALSTATEDIR', 'LIBDIR',
                       'INCLUDEDIR', 'INFODIR', 'MANDIR', 'PKGDATADIR',
                       'PKGLIBDIR', 'PKGINCLUDEDIR']:
            env.unset('OPAL_%s' % suffix)

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.mpicc = join_path(self.prefix.bin, 'mpicc')
        self.spec.mpicxx = join_path(self.prefix.bin, 'mpic++')
        self.spec.mpifc = join_path(self.prefix.bin, 'mpif90')
        self.spec.mpif77 = join_path(self.prefix.bin, 'mpif77')
        self.spec.mpicxx_shared_libs = [
            join_path(self.prefix.lib, 'libmpi_cxx.{0}'.format(dso_suffix)),
            join_path(self.prefix.lib, 'libmpi.{0}'.format(dso_suffix))
        ]

    # Most of the following with_or_without methods might seem redundant
    # because Spack compiler wrapper adds the required -I and -L flags, which
    # is enough for the configure script to find them. However, we also need
    # the flags in Libtool (lib/*.la) and pkg-config (lib/pkgconfig/*.pc).
    # Therefore, we pass the prefixes explicitly.

    def with_or_without_psm2(self, activated):
        if not activated:
            return '--without-psm2'
        return '--with-psm2={0}'.format(self.spec['opa-psm2'].prefix)

    def with_or_without_verbs(self, activated):
        # Up through version 1.6, this option was named --with-openib.
        # In version 1.7, it was renamed to be --with-verbs.
        opt = 'verbs' if self.spec.satisfies('@1.7:') else 'openib'
        if not activated:
            return '--without-{0}'.format(opt)
        return '--with-{0}={1}'.format(opt, self.spec['rdma-core'].prefix)

    def with_or_without_mxm(self, activated):
        if not activated:
            return '--without-mxm'
        return '--with-mxm={0}'.format(self.spec['mxm'].prefix)

    def with_or_without_ucx(self, activated):
        if not activated:
            return '--without-ucx'
        return '--with-ucx={0}'.format(self.spec['ucx'].prefix)

    def with_or_without_ofi(self, activated):
        # Up through version 3.0.3 this option was name --with-libfabric.
        # In version 3.0.4, the old name was deprecated in favor of --with-ofi.
        opt = 'ofi' if self.spec.satisfies('@3.0.4:') else 'libfabric'
        if not activated:
            return '--without-{0}'.format(opt)
        return '--with-{0}={1}'.format(opt, self.spec['libfabric'].prefix)

    def with_or_without_fca(self, activated):
        if not activated:
            return '--without-fca'
        return '--with-fca={0}'.format(self.spec['fca'].prefix)

    def with_or_without_hcoll(self, activated):
        if not activated:
            return '--without-hcoll'
        return '--with-hcoll={0}'.format(self.spec['hcoll'].prefix)

    def with_or_without_xpmem(self, activated):
        if not activated:
            return '--without-xpmem'
        return '--with-xpmem={0}'.format(self.spec['xpmem'].prefix)

    def with_or_without_knem(self, activated):
        if not activated:
            return '--without-knem'
        return '--with-knem={0}'.format(self.spec['knem'].prefix)

    def with_or_without_lsf(self, activated):
        if not activated:
            return '--without-lsf'
        return '--with-lsf={0}'.format(self.spec['lsf'].prefix)

    def with_or_without_tm(self, activated):
        if not activated:
            return '--without-tm'
        return '--with-tm={0}'.format(self.spec['openpbs'].prefix)

    @run_before('autoreconf')
    def die_without_fortran(self):
        # Until we can pass variants such as +fortran through virtual
        # dependencies depends_on('mpi'), require Fortran compiler to
        # avoid delayed build errors in dependents.
        if (self.compiler.f77 is None) or (self.compiler.fc is None):
            raise InstallError(
                'OpenMPI requires both C and Fortran compilers!'
            )

    @when('@develop')
    def autoreconf(self, spec, prefix):
        perl = which('perl')
        perl('autogen.pl')

    def setup_build_environment(self, env):
        if '~gpfs' in self.spec:
            env.set('ac_cv_header_gpfs_h', 'no')
            env.set('ac_cv_header_gpfs_fcntl_h', 'no')

    def configure_args(self):
        spec = self.spec
        config_args = [
            '--enable-shared',
            '--disable-silent-rules'
        ]

        # All rpath flags should be appended with self.compiler.cc_rpath_arg.
        # Later, we might need to update share/openmpi/mpic++-wrapper-data.txt
        # and mpifort-wrapper-data.txt (see filter_rpaths()).
        wrapper_ldflags = []

        if '+atomics' in spec:
            config_args.append('--enable-builtin-atomics')
        else:
            config_args.append('--disable-builtin-atomics')

        # According to this comment on github:
        #
        # https://github.com/open-mpi/ompi/issues/4338#issuecomment-383982008
        #
        # adding --enable-static silently disables slurm support via pmi/pmi2
        # for versions older than 3.0.3,3.1.3,4.0.0
        # Presumably future versions after 11/2018 should support slurm+static
        if spec.satisfies('schedulers=slurm'):
            if spec.satisfies('+pmi'):
                config_args.append('--with-pmi={0}'.format(
                    spec['slurm'].prefix))
            else:
                config_args.extend(self.with_or_without('pmi'))
            if spec.satisfies('@3.1.3:') or spec.satisfies('@3.0.3'):
                if '+static' in spec:
                    config_args.append('--enable-static')
        else:
            if '+static' in spec:
                config_args.append('--enable-static')
            else:
                config_args.append('--disable-static')

            config_args.extend(self.with_or_without('pmi'))

        if spec.satisfies('@3.0.0:', strict=True):
            config_args.append('--with-zlib={0}'.format(spec['zlib'].prefix))

        if spec.satisfies('@4.0.0:4.0.2'):
            # uct btl doesn't work with some UCX versions so just disable
            config_args.append('--enable-mca-no-build=btl-uct')

        # some scientific packages ignore deprecated/remove symbols. Re-enable
        # them for now, for discussion see
        # https://github.com/open-mpi/ompi/issues/6114#issuecomment-446279495
        if spec.satisfies('@4.0.1:'):
            config_args.append('--enable-mpi1-compatibility')

        # Fabrics
        if 'fabrics=auto' not in spec:
            config_args.extend(self.with_or_without('fabrics'))

        if spec.satisfies('@2.0.0'):
            if 'fabrics=xpmem' in spec and 'platform=cray' in spec:
                config_args.append('--with-cray-xpmem')
            else:
                config_args.append('--without-cray-xpmem')

        # Schedulers
        if 'schedulers=auto' not in spec:
            config_args.extend(self.with_or_without('schedulers'))

        config_args.extend(self.enable_or_disable('memchecker'))
        if spec.satisfies('+memchecker', strict=True):
            config_args.extend([
                '--enable-debug',
                '--with-valgrind={0}'.format(spec['valgrind'].prefix),
            ])

        # Singularity container support
        if spec.satisfies('+singularity @:4.9'):
            singularity_opt = '--with-singularity={0}'.format(
                spec['singularity'].prefix)
            config_args.append(singularity_opt)
        # Lustre filesystem support
        if spec.satisfies('+lustre'):
            lustre_opt = '--with-lustre={0}'.format(spec['lustre'].prefix)
            config_args.append(lustre_opt)
        # external libevent
        if spec.satisfies('@4.0.0:'):
            config_args.append('--with-libevent={0}'.format(spec['libevent'].prefix))
        # Hwloc support
        if '~internal-hwloc' in spec and spec.satisfies('@1.5.2:'):
            config_args.append('--with-hwloc={0}'.format(spec['hwloc'].prefix))
        # Java support
        if spec.satisfies('@1.7.4:'):
            if '+java' in spec:
                config_args.extend([
                    '--enable-java',
                    '--enable-mpi-java',
                    '--with-jdk-dir={0}'.format(spec['java'].home)
                ])
            else:
                config_args.extend([
                    '--disable-java',
                    '--disable-mpi-java'
                ])

        # SQLite3 support
        if spec.satisfies('@1.7.3:1.999'):
            if '+sqlite3' in spec:
                config_args.append('--with-sqlite3')
            else:
                config_args.append('--without-sqlite3')

        # VampirTrace support
        if spec.satisfies('@1.3:1.999'):
            if '+vt' not in spec:
                config_args.append('--enable-contrib-no-build=vt')

        # Multithreading support
        if spec.satisfies('@1.5.4:2.999'):
            if '+thread_multiple' in spec:
                config_args.append('--enable-mpi-thread-multiple')
            else:
                config_args.append('--disable-mpi-thread-multiple')

        # CUDA support
        # See https://www.open-mpi.org/faq/?category=buildcuda
        if spec.satisfies('@1.7:'):
            if '+cuda' in spec:
                # OpenMPI dynamically loads libcuda.so, requires dlopen
                config_args.append('--enable-dlopen')
                # Searches for header files in DIR/include
                config_args.append('--with-cuda={0}'.format(
                    spec['cuda'].prefix))
                if spec.satisfies('@1.7:1.7.2'):
                    # This option was removed from later versions
                    config_args.append('--with-cuda-libdir={0}'.format(
                        spec['cuda'].libs.directories[0]))
                if spec.satisfies('@1.7.2'):
                    # There was a bug in 1.7.2 when --enable-static is used
                    config_args.append('--enable-mca-no-build=pml-bfo')
                if spec.satisfies('%pgi^cuda@7.0:7.999'):
                    # OpenMPI has problems with CUDA 7 and PGI
                    config_args.append(
                        '--with-wrapper-cflags=-D__LP64__ -ta:tesla')
                    if spec.satisfies('%pgi@:15.8'):
                        # With PGI 15.9 and later compilers, the
                        # CFLAGS=-D__LP64__ is no longer needed.
                        config_args.append('CFLAGS=-D__LP64__')
            else:
                config_args.append('--without-cuda')

        if spec.satisfies('%nvhpc@:20.11'):
            # Workaround compiler issues
            config_args.append('CFLAGS=-O1')

        if '+wrapper-rpath' in spec:
            config_args.append('--enable-wrapper-rpath')

            # Disable new dynamic tags in the wrapper (--disable-new-dtags)
            # In the newer versions this can be done with a configure option
            # (for older versions, we rely on filter_compiler_wrappers() and
            # filter_pc_files()):
            if spec.satisfies('@3.0.5:'):
                config_args.append('--disable-wrapper-runpath')

            # Add extra_rpaths and implicit_rpaths into the wrappers.
            wrapper_ldflags.extend([
                self.compiler.cc_rpath_arg + path
                for path in itertools.chain(
                    self.compiler.extra_rpaths,
                    self.compiler.implicit_rpaths())])
        else:
            config_args.append('--disable-wrapper-rpath')

        if spec.satisfies('@:4'):
            if '+cxx' in spec:
                config_args.append('--enable-mpi-cxx')
            else:
                config_args.append('--disable-mpi-cxx')

            if '+cxx_exceptions' in spec:
                config_args.append('--enable-cxx-exceptions')
            else:
                config_args.append('--disable-cxx-exceptions')

        if wrapper_ldflags:
            config_args.append(
                '--with-wrapper-ldflags={0}'.format(' '.join(wrapper_ldflags)))

        return config_args

    @when('+wrapper-rpath')
    @run_after('install')
    def filter_rpaths(self):

        def filter_lang_rpaths(lang_tokens, rpath_arg):
            if self.compiler.cc_rpath_arg == rpath_arg:
                return

            files = find(self.spec.prefix.share.openmpi,
                         ['*{0}-wrapper-data*'.format(t) for t in lang_tokens])
            files.extend(find(self.spec.prefix.lib.pkgconfig,
                              ['ompi-{0}.pc'.format(t) for t in lang_tokens]))

            x = FileFilter(*[f for f in files if not os.path.islink(f)])

            # Replace self.compiler.cc_rpath_arg, which have been added as
            # '--with-wrapper-ldflags', with rpath_arg in the respective
            # language-specific wrappers and pkg-config files.
            x.filter(self.compiler.cc_rpath_arg, rpath_arg,
                     string=True, backup=False)

            if self.spec.satisfies('@:1.10.3,2:2.1.1'):
                # Replace Libtool-style RPATH prefixes '-Wl,-rpath -Wl,' with
                # rpath_arg for old version of OpenMPI, which assumed that CXX
                # and FC had the same prefixes as CC.
                x.filter('-Wl,-rpath -Wl,', rpath_arg,
                         string=True, backup=False)

        filter_lang_rpaths(['c++', 'CC', 'cxx'], self.compiler.cxx_rpath_arg)
        filter_lang_rpaths(['fort', 'f77', 'f90'], self.compiler.fc_rpath_arg)

    @when('@:3.0.4+wrapper-rpath')
    @run_after('install')
    def filter_pc_files(self):
        files = find(self.spec.prefix.lib.pkgconfig, '*.pc')
        x = FileFilter(*[f for f in files if not os.path.islink(f)])

        # Remove this linking flag if present (it turns RPATH into RUNPATH)
        x.filter('{0}--enable-new-dtags'.format(self.compiler.linker_arg), '',
                 string=True, backup=False)

        # NAG compiler is usually mixed with GCC, which has a different
        # prefix for linker arguments.
        if self.compiler.name == 'nag':
            x.filter('-Wl,--enable-new-dtags', '', string=True, backup=False)

    @run_after('install')
    def delete_mpirun_mpiexec(self):
        # The preferred way to run an application when Slurm is the
        # scheduler is to let Slurm manage process spawning via PMI.
        #
        # Deleting the links to orterun avoids users running their
        # applications via mpirun or mpiexec, and leaves srun as the
        # only sensible choice (orterun is still present, but normal
        # users don't know about that).
        if '@1.6: ~legacylaunchers schedulers=slurm' in self.spec:
            exe_list = [self.prefix.bin.mpirun,
                        self.prefix.bin.mpiexec,
                        self.prefix.bin.shmemrun,
                        self.prefix.bin.oshrun
                        ]
            script_stub = join_path(os.path.dirname(__file__),
                                    "nolegacylaunchers.sh")
            for exe in exe_list:
                try:
                    os.remove(exe)
                except OSError:
                    tty.debug("File not present: " + exe)
                else:
                    copy(script_stub, exe)

    @run_after('install')
    def setup_install_tests(self):
        """
        Copy the example files after the package is installed to an
        install test subdirectory for use during `spack test run`.
        """
        self.cache_extra_test_sources(self.extra_install_tests)

    def _test_bin_ops(self):
        info = ([], ['Ident string: {0}'.format(self.spec.version), 'MCA'],
                0)

        ls = (['-n', '1', 'ls', '..'],
              ['openmpi-{0}'.format(self.spec.version)], 0)

        checks = {
            'mpirun': ls,
            'ompi_info': info,
            'oshmem_info': info,
            'oshrun': ls,
            'shmemrun': ls,
        }

        for exe in checks:
            options, expected, status = checks[exe]
            reason = 'test: checking {0} output'.format(exe)
            self.run_test(exe, options, expected, status, installed=True,
                          purpose=reason, skip_missing=True)

    def _test_check_versions(self):
        comp_vers = str(self.spec.compiler.version)
        spec_vers = str(self.spec.version)
        checks = {
            # Binaries available in at least versions 2.0.0 through 4.0.3
            'mpiCC': comp_vers,
            'mpic++': comp_vers,
            'mpicc': comp_vers,
            'mpicxx': comp_vers,
            'mpiexec': spec_vers,
            'mpif77': comp_vers,
            'mpif90': comp_vers,
            'mpifort': comp_vers,
            'mpirun': spec_vers,
            'ompi_info': spec_vers,
            'ortecc': comp_vers,
            'orterun': spec_vers,

            # Binaries available in versions 2.0.0 through 2.1.6
            'ompi-submit': spec_vers,
            'orte-submit': spec_vers,

            # Binaries available in versions 2.0.0 through 3.1.5
            'ompi-dvm': spec_vers,
            'orte-dvm': spec_vers,
            'oshcc': comp_vers,
            'oshfort': comp_vers,
            'oshmem_info': spec_vers,
            'oshrun': spec_vers,
            'shmemcc': comp_vers,
            'shmemfort': comp_vers,
            'shmemrun': spec_vers,

            # Binary available in version 3.1.0 through 3.1.5
            'prun': spec_vers,

            # Binaries available in versions 3.0.0 through 3.1.5
            'oshCC': comp_vers,
            'oshc++': comp_vers,
            'oshcxx': comp_vers,
            'shmemCC': comp_vers,
            'shmemc++': comp_vers,
            'shmemcxx': comp_vers,
        }

        for exe in checks:
            expected = checks[exe]
            purpose = 'test: ensuring version of {0} is {1}' \
                .format(exe, expected)
            self.run_test(exe, '--version', expected, installed=True,
                          purpose=purpose, skip_missing=True)

    def _test_examples(self):
        # First build the examples
        self.run_test('make', ['all'], [],
                      purpose='test: ensuring ability to build the examples',
                      work_dir=join_path(self.install_test_root,
                                         self.extra_install_tests))

        # Now run those with known results
        have_spml = self.spec.satisfies('@2.0.0:2.1.6')

        hello_world = (['Hello, world', 'I am', '0 of', '1'], 0)

        max_red = (['0/1 dst = 0 1 2'], 0)

        missing_spml = (['No available spml components'], 1)

        no_out = ([''], 0)

        ring_out = (['1 processes in ring', '0 exiting'], 0)

        strided = (['not in valid range'], 255)

        checks = {
            'hello_c': hello_world,
            'hello_cxx': hello_world,
            'hello_mpifh': hello_world,
            'hello_oshmem': hello_world if have_spml else missing_spml,
            'hello_oshmemcxx': hello_world if have_spml else missing_spml,
            'hello_oshmemfh': hello_world if have_spml else missing_spml,
            'hello_usempi': hello_world,
            'hello_usempif08': hello_world,
            'oshmem_circular_shift': ring_out if have_spml else missing_spml,
            'oshmem_max_reduction': max_red if have_spml else missing_spml,
            'oshmem_shmalloc': no_out if have_spml else missing_spml,
            'oshmem_strided_puts': strided if have_spml else missing_spml,
            'oshmem_symmetric_data': no_out if have_spml else missing_spml,
            'ring_c': ring_out,
            'ring_cxx': ring_out,
            'ring_mpifh': ring_out,
            'ring_oshmem': ring_out if have_spml else missing_spml,
            'ring_oshmemfh': ring_out if have_spml else missing_spml,
            'ring_usempi': ring_out,
            'ring_usempif08': ring_out,
        }

        for exe in checks:
            expected = checks[exe]
            reason = 'test: checking example {0} output'.format(exe)
            self.run_test(exe, [], expected, 0, installed=True,
                          purpose=reason, skip_missing=True)

    def test(self):
        """Perform smoke tests on the installed package."""
        # Simple version check tests on known packages
        self._test_check_versions()

        # Test the operation of selected executables
        self._test_bin_ops()

        # Test example programs pulled from the build
        self._test_examples()


def get_spack_compiler_spec(path):
    spack_compilers = spack.compilers.find_compilers([path])
    actual_compiler = None
    # check if the compiler actually matches the one we want
    for spack_compiler in spack_compilers:
        if os.path.dirname(spack_compiler.cc) == path:
            actual_compiler = spack_compiler
            break
    return actual_compiler.spec if actual_compiler else None


def is_enabled(text):
    if text in set(['t', 'true', 'enabled', 'yes', '1']):
        return True
    return False


# This code gets all the fabric names from the variants list
# Idea taken from the AutotoolsPackage source.
def get_options_from_variant(self, name):
    values = self.variants[name].values
    if getattr(values, 'feature_values', None):
        values = values.feature_values
    return values
