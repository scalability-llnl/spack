# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from sys import platform

from spack import *


class IntelOneapiIpp(IntelOneApiLibraryPackage):
    """Intel oneAPI IPP."""

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/ipp.html'

    if platform == 'linux':
        version('2021.1.1',
                sha256='2656a3a7f1f9f1438cbdf98fd472a213c452754ef9476dd65190a7d46618ba86',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17436/l_ipp_oneapi_p_2021.1.1.47_offline.sh',
                expand=False)

    depends_on('intel-oneapi-tbb')

    provides('ipp')

    @property
    def component_dir(self):
        return 'ipp'
