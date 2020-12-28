# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class G4emlow(Package):
    """Geant4 data files for low energy electromagnetic processes."""
    homepage = "http://geant4.web.cern.ch"
    url = "http://geant4-data.web.cern.ch/geant4-data/datasets/G4EMLOW.6.50.tar.gz"

    tags = ['hep']

    maintainers = ['drbenmorgan']

    # Only versions relevant to Geant4 releases built by spack are added
    version('7.13', sha256='374896b649be776c6c10fea80abe6cf32f9136df0b6ab7c7236d571d49fb8c69')
    version('7.9.1', sha256='820c106e501c64c617df6c9e33a0f0a3822ffad059871930f74b8cc37f043ccb')
    version('7.9', sha256='4abf9aa6cda91e4612676ce4d2d8a73b91184533aa66f9aad19a53a8c4dc3aff')
    version('7.7', sha256='16dec6adda6477a97424d749688d73e9bd7d0b84d0137a67cf341f1960984663')
    version('7.3', sha256='583aa7f34f67b09db7d566f904c54b21e95a9ac05b60e2bfb794efb569dba14e')
    version('6.50', sha256='c97be73fece5fb4f73c43e11c146b43f651c6991edd0edf8619c9452f8ab1236')

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data', 'G4EMLOW{0}'
                                 .format(self.version))
        install_tree(self.stage.source_path, install_path)

    def setup_dependent_run_environment(self, env, dependent_spec):
        install_path = join_path(self.prefix.share, 'data', 'G4EMLOW{0}'
                                 .format(self.version))
        env.set('G4LEDATA', install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://geant4-data.web.cern.ch/geant4-data/datasets/G4EMLOW.%s.tar.gz" % version)
