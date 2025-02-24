# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class G4tendl(Package):
    """Geant4 data for incident particles [optional]"""

    homepage = "https://geant4.web.cern.ch"
    url = "https://geant4-data.web.cern.ch/geant4-data/datasets/G4TENDL.1.3.tar.gz"

    tags = ["hep"]

    maintainers("drbenmorgan")

    # Only versions relevant to Geant4 releases built by spack are added
    version("1.4", sha256="4b7274020cc8b4ed569b892ef18c2e088edcdb6b66f39d25585ccee25d9721e0")
    version("1.3.2", sha256="3b2987c6e3bee74197e3bd39e25e1cc756bb866c26d21a70f647959fc7afb849")
    version("1.3", sha256="52ad77515033a5d6f995c699809b464725a0e62099b5e55bf07c8bdd02cd3bce")

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, "data"))
        install_path = join_path(prefix.share, "data", self.g4datasetname)
        install_tree(self.stage.source_path, install_path)

    def setup_dependent_run_environment(self, env, dependent_spec):
        install_path = join_path(self.prefix.share, "data", self.g4datasetname)
        env.set("G4PARTICLEHPDATA", install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return "http://geant4-data.web.cern.ch/geant4-data/datasets/G4TENDL.%s.tar.gz" % version

    @property
    def g4datasetname(self):
        spec = self.spec
        return "G4TENDL{0}".format(spec.version)
