# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from sys import platform

from spack import *


class IntelOneapiCcl(IntelOneApiLibraryPackage):
    """Intel oneAPI CCL."""

    maintainers = ['rscohn2', 'danvev']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/oneccl.html'

    depends_on('intel-oneapi-mpi')

    if platform == 'linux':
        version('2021.2.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17731/l_oneapi_ccl_p_2021.2.0.269_offline.sh',
                sha256='18b7875030243295b75471e235e91e5f7b4fc15caf18c07d941a6d47fba378d7',
                expand=False)
        version('2021.1.1',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17391/l_oneapi_ccl_p_2021.1.1.54_offline.sh',
                sha256='de732df57a03763a286106c8b885fd60e83d17906936a8897a384b874e773f49',
                expand=False)

    @property
    def component_dir(self):
        return 'ccl'
