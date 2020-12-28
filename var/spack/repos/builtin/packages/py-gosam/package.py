# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGosam(PythonPackage):
    """The package GoSam allows for the automated calculation of
       one-loop amplitudes for multi-particle processes in renormalizable
       quantum field theories."""

    homepage = "https://gosam.hepforge.org"
    url      = "https://gosam.hepforge.org/downloads/?f=gosam-2.0.4-6d9f1cba.tar.gz"

    tags = ['hep']

    version('2.0.4', sha256='faf621c70f66d9dffc16ac5cce66258067f39f686d722a4867eeb759fcde4f44')

    depends_on('form', type='run')
    depends_on('qgraf', type='run')
    depends_on('gosam-contrib', type='link')
    depends_on('python@2.7:2.7.99', type=('build', 'run'))

    def setup_run_environment(self, env):
        gosam_contrib_lib_dir = self.spec['gosam-contrib'].prefix.lib
        env.prepend_path('LD_LIBRARY_PATH', gosam_contrib_lib_dir)
