# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class IntelIpp(IntelPackage):
    """Intel Integrated Performance Primitives."""

    homepage = "https://software.intel.com/en-us/intel-ipp"

    version('2020.2.254', sha256='18266ad1eec9b5b17e76da24f1aa9a9147300e5bd345e6bdad58d7187392fa77',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/16846/l_ipp_2020.2.254.tgz')
    version('2020.1.217', sha256='0bf8ac7e635e7e602cf201063a1a7dea3779b093104563fdb15e6b7ecf2f00a7',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/16534/l_ipp_2020.1.217.tgz')
    version('2020.0.166', sha256='6844007892ba524e828f245355cee44e8149f4c233abbbea16f7bb55a7d6ecff',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/16233/l_ipp_2020.0.166.tgz')
    version('2019.5.281', sha256='61d1e1da1a4a50f1cf02a3ed44e87eed05e94d58b64ef1e67a3bdec363bee713',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15817/l_ipp_2019.5.281.tgz')
    version('2019.4.243', sha256='d4f4232323e66b010d8440c75189aeb6a3249966e05035242b21982238a7a7f2',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15541/l_ipp_2019.4.243.tgz')
    version('2019.3.199', sha256='02545383206c1ae4dd66bfa6a38e2e14480ba11932eeed632df8ab798aa15ccd',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15276/l_ipp_2019.3.199.tgz')
    version('2019.2.187', sha256='280e9081278a0db3892fe82474c1201ec780a6f7c8d1f896494867f4b3bd8421',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15096/l_ipp_2019.2.187.tgz')
    version('2019.1.144', sha256='1eb7cd0fba74615aeafa4e314c645414497eb73f1705200c524fe78f00620db3',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/14887/l_ipp_2019.1.144.tgz')
    version('2019.0.117', sha256='d552ba49fba58f0e94da2048176f21c5dfd490dca7c5ce666dfc2d18db7fd551',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13576/l_ipp_2019.0.117.tgz')
    version('2018.4.274', sha256='bdc6082c65410c98ccf6daf239e0a6625d15ec5e0ddc1c0563aad42b6ba9063c',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13726/l_ipp_2018.4.274.tgz')
    version('2018.3.222', sha256='bb783c5e6220e240f19136ae598cd1c1d647496495139ce680de58d3d5496934',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13006/l_ipp_2018.3.222.tgz')
    version('2018.2.199', sha256='55cb5c910b2c1e2bd798163fb5019b992b1259a0692e328bb9054778cf01562b',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12726/l_ipp_2018.2.199.tgz')
    version('2018.0.128', sha256='da568ceec1b7acbcc8f666b73d4092788b037b1b03c0436974b82155056ed166',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12071/l_ipp_2018.0.128.tgz')
    version('2017.3.196', sha256='50d49a1000a88a8a58bd610466e90ae28d07a70993a78cbbf85d44d27c4232b6',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11545/l_ipp_2017.3.196.tgz')
    version('2017.2.174', sha256='92f866c9dce8503d7e04223ec35f281cfeb0b81cf94208c3becb11aacfda7b99',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11307/l_ipp_2017.2.174.tgz')
    version('2017.1.132', sha256='2908bdeab3057d4ebcaa0b8ff5b00eb47425d35961a96f14780be68554d95376',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11031/l_ipp_2017.1.132.tgz')
    version('2017.0.098', sha256='7633d16e2578be64533892336c8a15c905139147b0f74eaf9f281358ad7cdcba',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9663/l_ipp_2017.0.098.tgz')
    # built from parallel_studio_xe_2016.3.067
    version('9.0.3.210', sha256='8ce7bf17f4a0bbf8c441063de26be7f6e0f6179789e23f24eaa8b712632b3cdd',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9067/l_ipp_9.0.3.210.tgz')

    provides('ipp')
