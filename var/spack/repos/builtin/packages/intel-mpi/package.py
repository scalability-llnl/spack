# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class IntelMpi(IntelPackage):
    """Intel MPI"""

    homepage = "https://software.intel.com/en-us/intel-mpi-library"

    version('2019.10.317', sha256='28e1b615e63d2170a99feedc75e3b0c5a7e1a07dcdaf0a4181831b07817a5346',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/17534/l_mpi_2019.10.317.tgz')
    version('2019.9.304', sha256='618a5dc2de54306645e6428c5eb7d267b54b11b5a83dfbcad7d0f9e0d90bb2e7',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/17263/l_mpi_2019.9.304.tgz')
    version('2019.8.254', sha256='fa163b4b79bd1b7509980c3e7ad81b354fc281a92f9cf2469bf4d323899567c0',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/16814/l_mpi_2019.8.254.tgz')
    version('2019.7.217', sha256='90383b0023f84ac003a55d8bb29dbcf0c639f43a25a2d8d8698a16e770ac9c07',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/16546/l_mpi_2019.7.217.tgz')
    version('2019.6.166', sha256='119be69f1117c93a9e5e9b8b4643918e55d2a55a78ad9567f77d16cdaf18cd6e',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/16120/l_mpi_2019.6.166.tgz')
    version('2019.5.281', sha256='9c59da051f1325b221e5bc4d8b689152e85d019f143069fa39e17989306811f4',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15838/l_mpi_2019.5.281.tgz')
    version('2019.4.243', sha256='233a8660b92ecffd89fedd09f408da6ee140f97338c293146c9c080a154c5fcd',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15553/l_mpi_2019.4.243.tgz')
    version('2019.3.199', sha256='5304346c863f64de797250eeb14f51c5cfc8212ff20813b124f20e7666286990',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15260/l_mpi_2019.3.199.tgz')
    version('2019.2.187', sha256='6a3305933b5ef9e3f7de969e394c91620f3fa4bb815a4f439577739d04778b20',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15040/l_mpi_2019.2.187.tgz')
    version('2019.1.144', sha256='dac86a5db6b86503313742b17535856a432955604f7103cb4549a9bfc256c3cd',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/14879/l_mpi_2019.1.144.tgz')
    version('2019.0.117', sha256='dfb403f49c1af61b337aa952b71289c7548c3a79c32c57865eab0ea0f0e1bc08',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13584/l_mpi_2019.0.117.tgz')
    version('2018.4.274', sha256='a1114b3eb4149c2f108964b83cad02150d619e50032059d119ac4ffc9d5dd8e0',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13741/l_mpi_2018.4.274.tgz')
    version('2018.3.222', sha256='5021d14b344fc794e89f146e4d53d70184d7048610895d7a6a1e8ac0cf258999',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13112/l_mpi_2018.3.222.tgz')
    version('2018.2.199', sha256='0927f1bff90d10974433ba2892e3fd38e6fee5232ab056a9f9decf565e814460',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12748/l_mpi_2018.2.199.tgz')
    version('2018.1.163', sha256='130b11571c3f71af00a722fa8641db5a1552ac343d770a8304216d8f5d00e75c',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12414/l_mpi_2018.1.163.tgz')
    version('2018.0.128', sha256='debaf2cf80df06db9633dfab6aa82213b84a665a55ee2b0178403906b5090209',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12120/l_mpi_2018.0.128.tgz')
    version('2017.4.239', sha256='5a1048d284dce8bc75b45789471c83c94b3c59f8f159cab43d783fc44302510b',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12209/l_mpi_2017.4.239.tgz')
    version('2017.3.196', sha256='dad9efbc5bbd3fd27cce7e1e2507ad77f342d5ecc929747ae141c890e7fb87f0',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11595/l_mpi_2017.3.196.tgz')
    version('2017.2.174', sha256='106a4b362c13ddc6978715e50f5f81c58c1a4c70cd2d20a99e94947b7e733b88',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11334/l_mpi_2017.2.174.tgz')
    version('2017.1.132', sha256='8d30a63674fe05f17b0a908a9f7d54403018bfed2de03c208380b171ab99be82',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11014/l_mpi_2017.1.132.tgz')
    # built from parallel_studio_xe_2016.3.068
    version('5.1.3.223',  sha256='544f4173b09609beba711fa3ba35567397ff3b8390e4f870a3307f819117dd9b',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9278/l_mpi_p_5.1.3.223.tgz')

    provides('mpi')

    def setup_dependent_build_environment(self, *args):
        # Handle in callback, conveying client's compilers in additional arg.
        # CAUTION - DUP code in:
        #   ../intel-mpi/package.py
        #   ../intel-parallel-studio/package.py
        self._setup_dependent_env_callback(*args, compilers_of_client={
            'CC':   spack_cc,
            'CXX':  spack_cxx,
            'F77':  spack_f77,
            'F90':  spack_fc,
            'FC':   spack_fc,
        })

    def setup_run_environment(self, env):
        super(IntelMpi, self).setup_run_environment(env)

        for name, value in self.mpi_compiler_wrappers.items():
            env.set(name, value)
