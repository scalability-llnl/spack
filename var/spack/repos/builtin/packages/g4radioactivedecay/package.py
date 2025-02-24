# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class G4radioactivedecay(Package):
    """Geant4 data files for radio-active decay hadronic processes"""

    homepage = "https://geant4.web.cern.ch"
    url = "https://geant4-data.web.cern.ch/geant4-data/datasets/G4RadioactiveDecay.5.1.1.tar.gz"

    tags = ["hep"]

    maintainers("drbenmorgan")

    # Only versions relevant to Geant4 releases built by spack are added
    version("6.1.2", sha256="a40d7e3ebc64d35555c4a49d0ff1e0945cd605d84354d053121293914caea13a")
    version("5.6", sha256="3886077c9c8e5a98783e6718e1c32567899eeb2dbb33e402d4476bc2fe4f0df1")
    version("5.4", sha256="240779da7d13f5bf0db250f472298c3804513e8aca6cae301db97f5ccdcc4a61")
    version("5.3", sha256="5c8992ac57ae56e66b064d3f5cdfe7c2fee76567520ad34a625bfb187119f8c1")
    version("5.2", sha256="99c038d89d70281316be15c3c98a66c5d0ca01ef575127b6a094063003e2af5d")
    version("5.1.1", sha256="f7a9a0cc998f0d946359f2cb18d30dff1eabb7f3c578891111fc3641833870ae")
    version("4.0", sha256="ed2053bddee507920a29a27db4364fbef255b951597686b0410d5458e9b38cb5")

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, "data"))
        install_path = join_path(prefix.share, "data", self.g4datasetname)
        install_tree(self.stage.source_path, install_path)

    def setup_dependent_run_environment(self, env, dependent_spec):
        install_path = join_path(self.prefix.share, "data", self.g4datasetname)
        env.set("G4RADIOACTIVEDATA", install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return (
            "http://geant4-data.web.cern.ch/geant4-data/datasets/G4RadioactiveDecay.%s.tar.gz"
            % version
        )

    @property
    def g4datasetname(self):
        spec = self.spec
        return "RadioactiveDecay{0}".format(spec.version)
