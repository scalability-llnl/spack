# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class G4urrpt(Package):
    """Geant4 data for evaluated particle cross-sections on
    natural composition of elements"""

    homepage = "https://geant4.web.cern.ch"
    url = "https://geant4-data.web.cern.ch/geant4-data/datasets/G4URRPT.1.0.tar.gz"

    tags = ["hep"]

    maintainers("drbenmorgan")

    # Only versions relevant to Geant4 releases built by spack are added
    version("1.1", sha256="6a3432db80bc088aee19c504b9c0124913005d6357ea14870451400ab20d9c11")
    version("1.0", sha256="278eb6c4086e919d2c2a718eb44d4897b7e06d2a32909f6ed48eb8590b3f9977")

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, "data"))
        install_path = join_path(prefix.share, "data", self.g4datasetname)
        install_tree(self.stage.source_path, install_path)

    def setup_dependent_run_environment(self, env, dependent_spec):
        install_path = join_path(self.prefix.share, "data", self.g4datasetname)
        env.set("G4URRPTDATA", install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return "http://geant4-data.web.cern.ch/geant4-data/datasets/G4URRPT.%s.tar.gz" % version

    @property
    def g4datasetname(self):
        spec = self.spec
        return "G4URRPT{0}".format(spec.version)
