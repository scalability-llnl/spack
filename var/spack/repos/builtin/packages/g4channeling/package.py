# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class G4channeling(Package):
    """Geant4 data for solid state crystal channeling"""

    homepage = "https://geant4.web.cern.ch"
    url = "https://geant4-data.web.cern.ch/geant4-data/datasets/G4CHANNELING.1.0.tar.gz"

    tags = ["hep"]

    maintainers("drbenmorgan")

    # Only versions relevant to Geant4 releases built by spack are added
    version("1.0", sha256="203e3c69984ca09acd181a1d31a9b0efafad4bc12e6c608f0b05e695120d67f2")

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, "data"))
        install_path = join_path(prefix.share, "data", self.g4datasetname)
        install_tree(self.stage.source_path, install_path)

    def setup_dependent_run_environment(self, env, dependent_spec):
        install_path = join_path(self.prefix.share, "data", self.g4datasetname)
        env.set("G4CHANNELINGDATA", install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return f"http://geant4-data.web.cern.ch/geant4-data/datasets/G4CHANNELING.{version}.tar.gz"

    @property
    def g4datasetname(self):
        return f"G4CHANNELING{self.spec.version}"
