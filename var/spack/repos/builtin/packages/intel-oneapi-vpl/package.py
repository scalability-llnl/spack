# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from sys import platform

from spack import *


class IntelOneapiVpl(IntelOneApiLibraryPackage):
    """Intel oneAPI VPL."""

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onevpl.html'

    if platform == 'linux':
        version('2021.1.1',
                sha256='0fec42545b30b7bb2e4e33deb12ab27a02900f5703153d9601673a8ce43082ed',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17418/l_oneVPL_p_2021.1.1.66_offline.sh',
                expand=False)

    @property
    def component_dir(self):
        return 'vpl'
