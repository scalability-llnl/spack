# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class G4saiddata(Package):
    """Geant4 data from evaluated cross-sections in SAID data-base"""

    homepage = "https://geant4.web.cern.ch"
    url = "https://geant4-data.web.cern.ch/geant4-data/datasets/G4SAIDDATA.1.1.tar.gz"

    tags = ["hep"]

    maintainers("drbenmorgan")

    # Only versions relevant to Geant4 releases built by spack are added
    version("2.0", sha256="1d26a8e79baa71e44d5759b9f55a67e8b7ede31751316a9e9037d80090c72e91")
    version("1.1", sha256="a38cd9a83db62311922850fe609ecd250d36adf264a88e88c82ba82b7da0ed7f")

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, "data"))
        install_path = join_path(prefix.share, "data", self.g4datasetname)
        install_tree(self.stage.source_path, install_path)

    def setup_dependent_run_environment(self, env, dependent_spec):
        install_path = join_path(self.prefix.share, "data", self.g4datasetname)
        env.set("G4SAIDXSDATA", install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return "http://geant4-data.web.cern.ch/geant4-data/datasets/G4SAIDDATA.%s.tar.gz" % version

    @property
    def g4datasetname(self):
        spec = self.spec
        return "G4SAIDDATA{0}".format(spec.version)
