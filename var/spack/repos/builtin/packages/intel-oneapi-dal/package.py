# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from sys import platform

from spack import *


class IntelOneapiDal(IntelOneApiLibraryPackage):
    """Intel oneAPI DAL."""

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onedal.html'

    if platform == 'linux':
        version('2021.1.1',
                sha256='6e0e24bba462e80f0fba5a46e95cf0cca6cf17948a7753f8e396ddedd637544e',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17443/l_daal_oneapi_p_2021.1.1.79_offline.sh',
                expand=False)

    depends_on('intel-oneapi-tbb')

    provides('daal')

    @property
    def component_dir(self):
        return 'dal'
