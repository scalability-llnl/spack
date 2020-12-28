# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class G4ndl(Package):
    """Geant4 Neutron data files with thermal cross sections """
    homepage = "http://geant4.web.cern.ch"
    url = "http://geant4-data.web.cern.ch/geant4-data/datasets/G4NDL.4.5.tar.gz"

    tags = ['hep']

    maintainers = ['drbenmorgan']

    version('4.6', sha256='9d287cf2ae0fb887a2adce801ee74fb9be21b0d166dab49bcbee9408a5145408')
    version('4.5', sha256='cba928a520a788f2bc8229c7ef57f83d0934bb0c6a18c31ef05ef4865edcdf8e')

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data', 'G4NDL{0}'
                                 .format(self.version))
        install_tree(self.stage.source_path, install_path)

    def setup_dependent_run_environment(self, env, dependent_spec):
        install_path = join_path(self.prefix.share, 'data', 'G4NDL{0}'
                                 .format(self.version))
        env.set('G4NEUTRONHPDATA', install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://geant4-data.web.cern.ch/geant4-data/datasets/G4NDL.%s.tar.gz" % version)
