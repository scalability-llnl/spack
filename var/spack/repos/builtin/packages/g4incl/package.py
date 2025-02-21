# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class G4incl(Package):
    """Geant4 data for evaluated particle cross-sections on natural
    composition of elements"""

    homepage = "https://geant4.web.cern.ch"
    url = "https://geant4-data.web.cern.ch/geant4-data/datasets/G4INCL.1.0.tar.gz"

    tags = ["hep"]

    maintainers("drbenmorgan")

    # Only versions relevant to Geant4 releases built by spack are added
    version("1.2", sha256="f880b16073ee0a92d7494f3276a6d52d4de1d3677a0d4c7c58700396ed0e1a7e")
    version("1.1", sha256="5d82e71db5f5a1b659937506576be58db7de7753ec5913128141ae7fce673b44")
    version("1.0", sha256="716161821ae9f3d0565fbf3c2cf34f4e02e3e519eb419a82236eef22c2c4367d")

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, "data"))
        install_path = join_path(prefix.share, "data", self.g4datasetname)
        install_tree(self.stage.source_path, install_path)

    def setup_dependent_run_environment(self, env, dependent_spec):
        install_path = join_path(self.prefix.share, "data", self.g4datasetname)
        env.set("G4INCLDATA", install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return "http://geant4-data.web.cern.ch/geant4-data/datasets/G4INCL.%s.tar.gz" % version

    @property
    def g4datasetname(self):
        spec = self.spec
        return "G4INCL{0}".format(spec.version)
