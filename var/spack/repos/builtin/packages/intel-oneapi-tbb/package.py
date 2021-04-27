# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from sys import platform

from spack import *


class IntelOneapiTbb(IntelOneApiLibraryPackage):
    """Intel oneAPI TBB."""

    maintainers = ['rscohn2', 'danvev']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onetbb.html'

    if platform == 'linux':
        version('2021.2.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17759/l_tbb_oneapi_p_2021.2.0.357_offline.sh',
                sha256='c1c3623c5bef547b30eac009e7a444611bf714c758d7472c114e9be9d5700eba',
                expand=False)
        version('2021.1.1',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17378/l_tbb_oneapi_p_2021.1.1.119_offline.sh',
                sha256='535290e3910a9d906a730b24af212afa231523cf13a668d480bade5f2a01b53b',
                expand=False)

    provides('tbb')

    @property
    def component_dir(self):
        return 'tbb'
