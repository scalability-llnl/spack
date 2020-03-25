# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack import *


class IntelMkl(IntelPackage):
    """Intel Math Kernel Library."""

    homepage = "https://software.intel.com/en-us/intel-mkl"

    version('2020.0.166', sha256='f6d92deb3ff10b11ba3df26b2c62bb4f0f7ae43e21905a91d553e58f0f5a8ae0',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/16232/l_mkl_2020.0.166.tgz')
    version('2019.5.281', sha256='9995ea4469b05360d509c9705e9309dc983c0a10edc2ae3a5384bc837326737e',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15816/l_mkl_2019.5.281.tgz')
    version('2019.4.243', sha256='fcac7b0369665d93f0c4dd98afe2816aeba5410e2b760655fe55fc477f8f33d0',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15540/l_mkl_2019.4.243.tgz')
    version('2019.3.199', sha256='06de2b54f4812e7c39a118536259c942029fe1d6d8918ad9df558a83c4162b8f',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15275/l_mkl_2019.3.199.tgz')
    version('2019.2.187', sha256='2bf004e6b5adb4f956993d6c20ea6ce289bb630314dd501db7f2dd5b9978ed1d',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15095/l_mkl_2019.2.187.tgz')
    version('2019.1.144', sha256='5205a460a9c685f7a442868367389b2d0c25e1455346bc6a37c5b8ff90a20fbb',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/14895/l_mkl_2019.1.144.tgz')
    version('2019.0.117', sha256='4e1fe2c705cfc47050064c0d6c4dee1a8c6740ac1c4f64dde9c7511c4989c7ad',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13575/l_mkl_2019.0.117.tgz')
    version('2018.4.274', sha256='18eb3cde3e6a61a88f25afff25df762a560013f650aaf363f7d3d516a0d04881',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13725/l_mkl_2018.4.274.tgz')
    version('2018.3.222', sha256='108d59c0927e58ce8c314db6c2b48ee331c3798f7102725f425d6884eb6ed241',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13005/l_mkl_2018.3.222.tgz')
    version('2018.2.199', sha256='e28d12173bef9e615b0ded2f95f59a42b3e9ad0afa713a79f8801da2bfb31936',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12725/l_mkl_2018.2.199.tgz')
    version('2018.1.163', sha256='f6dc263fc6f3c350979740a13de1b1e8745d9ba0d0f067ece503483b9189c2ca',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12414/l_mkl_2018.1.163.tgz')
    version('2018.0.128', sha256='c368baa40ca88057292512534d7fad59fa24aef06da038ea0248e7cd1e280cec',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12070/l_mkl_2018.0.128.tgz')
    version('2017.4.239', sha256='dcac591ed1e95bd72357fd778edba215a7eab9c6993236373231cc16c200c92a',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12147/l_mkl_2017.4.239.tgz')
    version('2017.3.196', sha256='fd7295870fa164d6138c9818304f25f2bb263c814a6c6539c9fe4e104055f1ca',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11544/l_mkl_2017.3.196.tgz')
    version('2017.2.174', sha256='0b8a3fd6bc254c3c3d9d51acf047468c7f32bf0baff22aa1e064d16d9fea389f',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11306/l_mkl_2017.2.174.tgz')
    version('2017.1.132', sha256='8c6bbeac99326d59ef3afdc2a95308c317067efdaae50240d2f4a61f37622e69',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11024/l_mkl_2017.1.132.tgz')
    version('2017.0.098', sha256='f2233e8e011f461d9c15a853edf7ed0ae8849aa665a1ec765c1ff196fd70c4d9',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9662/l_mkl_2017.0.098.tgz')
    # built from parallel_studio_xe_2016.3.x
    version('11.3.3.210', sha256='ff858f0951fd698e9fb30147ea25a8a810c57f0126c8457b3b0cdf625ea43372',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9068/l_mkl_11.3.3.210.tgz')
    # built from parallel_studio_xe_2016.2.062
    version('11.3.2.181', sha256='bac04a07a1fe2ae4996a67d1439ee90c54f31305e8663d1ccfce043bed84fc27',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8711/l_mkl_11.3.2.181.tgz')

    depends_on('cpio', type='build')

    provides('blas')
    provides('lapack')
    provides('scalapack')
    provides('mkl')
    provides('fftw-api@3', when='@2017:')

    # Note: there is no libmkl_gnu_thread on macOS
    # if sys.platform == 'darwin':
    #    conflicts('threads=openmp', when='%gcc')
