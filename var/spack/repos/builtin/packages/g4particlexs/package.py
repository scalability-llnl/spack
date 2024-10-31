# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class G4particlexs(Package):
    """Geant4 data for evaluated particle cross-sections on
    natural composition of elements"""

    homepage = "https://geant4.web.cern.ch"
    url = "https://geant4-data.web.cern.ch/geant4-data/datasets/G4PARTICLEXS.2.1.tar.gz"

    tags = ["hep"]

    maintainers("drbenmorgan")

    # Only versions relevant to Geant4 releases built by spack are added
    version("4.1", sha256="07ae1e048e9ac8e7f91f6696497dd55bd50ccc822d97af1a0b9e923212a6d7d1")
    version("4.0", sha256="9381039703c3f2b0fd36ab4999362a2c8b4ff9080c322f90b4e319281133ca95")
    version("3.1.1", sha256="66c17edd6cb6967375d0497add84c2201907a25e33db782ebc26051d38f2afda")
    version("3.1", sha256="404da84ead165e5cccc0bb795222f6270c9bf491ef4a0fd65195128b27f0e9cd")
    version("2.1", sha256="094d103372bbf8780d63a11632397e72d1191dc5027f9adabaf6a43025520b41")
    version("1.1", sha256="100a11c9ed961152acfadcc9b583a9f649dda4e48ab314fcd4f333412ade9d62")

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, "data"))
        install_path = join_path(prefix.share, "data", "G4PARTICLEXS{0}".format(self.version))
        install_tree(self.stage.source_path, install_path)

    def setup_dependent_run_environment(self, env, dependent_spec):
        install_path = join_path(self.prefix.share, "data", "G4PARTICLEXS{0}".format(self.version))
        env.set("G4PARTICLEXSDATA", install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return (
            "http://geant4-data.web.cern.ch/geant4-data/datasets/G4PARTICLEXS.%s.tar.gz" % version
        )
