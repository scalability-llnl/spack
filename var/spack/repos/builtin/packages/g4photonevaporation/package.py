# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class G4photonevaporation(Package):
    """Geant4 data for photon evaporation"""
    homepage = "http://geant4.web.cern.ch"
    url = "http://geant4-data.web.cern.ch/geant4-data/datasets/G4PhotonEvaporation.4.3.2.tar.gz"

    tags = ['hep']

    maintainers = ['drbenmorgan']

    # Only versions relevant to Geant4 releases built by spack are added
    version('5.7', sha256='761e42e56ffdde3d9839f9f9d8102607c6b4c0329151ee518206f4ee9e77e7e5')
    version('5.5', sha256='5995dda126c18bd7f68861efde87b4af438c329ecbe849572031ceed8f5e76d7')
    version('5.3', sha256='d47ababc8cbe548065ef644e9bd88266869e75e2f9e577ebc36bc55bf7a92ec8')
    version('5.2', sha256='83607f8d36827b2a7fca19c9c336caffbebf61a359d0ef7cee44a8bcf3fc2d1f')
    version('4.3.2', sha256='d4641a6fe1c645ab2a7ecee09c34e5ea584fb10d63d2838248bfc487d34207c7')

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data',
                                 'PhotonEvaporation{0}'
                                 .format(self.version))
        install_tree(self.stage.source_path, install_path)

    def setup_dependent_run_environment(self, env, dependent_spec):
        install_path = join_path(self.prefix.share, 'data',
                                 'PhotonEvaporation{0}'
                                 .format(self.version))
        env.set('G4LEVELGAMMADATA', install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://geant4-data.web.cern.ch/geant4-data/datasets/G4PhotonEvaporation.%s.tar.gz" % version)
