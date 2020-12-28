# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class IntelDaal(IntelPackage):
    """Intel Data Analytics Acceleration Library."""

    homepage = "https://software.intel.com/en-us/daal"

    version('2020.2.254', sha256='08528bc150dad312ff2ae88ce12d6078ed8ba2f378f4bf3daf0fbbb9657dce1e',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/16822/l_daal_2020.2.254.tgz')
    version('2020.1.217', sha256='3f84dea0ce1038ac1b9c25b3e2c02e9fac440fa36cc8adfce69edfc06fe0edda',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/16536/l_daal_2020.1.217.tgz')
    version('2020.0.166', sha256='695166c9ab32ac5d3006d6d35162db3c98734210507144e315ed7c3b7dbca9c1',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/16234/l_daal_2020.0.166.tgz')
    version('2019.5.281', sha256='e92aaedbe35c9daf1c9483260cb2363da8a85fa1aa5566eb38cf4b1f410bc368',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15818/l_daal_2019.5.281.tgz')
    version('2019.4.243', sha256='c74486a555ca5636c2ac1b060d5424726c022468f3ee0898bb46e333cda6f7b8',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15552/l_daal_2019.4.243.tgz')
    version('2019.3.199', sha256='1f7d9cdecc1091b03f1ee6303fc7566179d1e3f1813a98ef7a6239f7d456b8ef',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15277/l_daal_2019.3.199.tgz')
    version('2019.2.187', sha256='2982886347e9376e892a5c4e22fa1d4b7b843e1ae988a107dd2d0a639f257765',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15097/l_daal_2019.2.187.tgz')
    version('2019.1.144', sha256='1672afac568c93e185283cf7e044d511381092ebc95d7204c4dccb83cc493197',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/14869/l_daal_2019.1.144.tgz')
    version('2019.0.117', sha256='85ac8e983bc9b9cc635e87cb4ec775ffd3695e44275d20fdaf53c19ed280d69f',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13577/l_daal_2019.0.117.tgz')
    version('2018.3.222', sha256='378fec529a36508dd97529037e1164ff98e0e062a9a47ede99ccf9e91493d1e2',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13007/l_daal_2018.3.222.tgz')
    version('2018.2.199', sha256='cee30299b3ffaea515f5a9609f4df0f644579c8a1ba2b61747b390f6caf85b14',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12727/l_daal_2018.2.199.tgz')
    version('2018.1.163', sha256='ac96b5a6c137cda18817d9b3505975863f8f53347225ebb6ccdaaf4bdb8dc349',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12414/l_daal_2018.1.163.tgz')
    version('2018.0.128', sha256='d13a7cd1b6779971f2ba46797447de9409c98a4d2f0eb0dc9622d9d63ac8990f',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12072/l_daal_2018.0.128.tgz')
    version('2017.4.239', sha256='cc4b608f59f3b2fafee16389102a763d27c46f6d136a6cfa89847418a8ea7460',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12148/l_daal_2017.4.239.tgz')
    version('2017.3.196', sha256='cfa863f342dd1c5fe8f1c7b6fd69589140370fc92742a19d82c8594e4e1e46ce',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11546/l_daal_2017.3.196.tgz')
    version('2017.2.174', sha256='5ee838b08d4cda7fc3e006e1deeed41671cbd7cfd11b64ec3b762c94dfc2b660',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11308/l_daal_2017.2.174.tgz')
    version('2017.1.132', sha256='6281105d3947fc2860e67401ea0218198cc4753fd2d4b513528a89143248e4f3',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/10983/l_daal_2017.1.132.tgz')
    version('2017.0.098', sha256='a7064425653b4f5f0fe51e25358d267d8ae023179eece61e08da891b67d79fe5',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9664/l_daal_2017.0.098.tgz')
    version('2016.3.210', sha256='367eaef21ea0143c11ae3fd56cd2a05315768c059e14caa15894bcf96853687c',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9099/l_daal_2016.3.210.tgz')
    version('2016.2.181', sha256='afdb65768957784d28ac537b4933a86eb4193c68a636157caed17b29ccdbfacb',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8687/l_daal_2016.2.181.tgz')

    provides('daal')
