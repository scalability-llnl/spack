# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class G4realsurface(Package):
    """Geant4 data for measured optical surface reflectance"""

    homepage = "https://geant4.web.cern.ch"
    url = "https://geant4-data.web.cern.ch/geant4-data/datasets/RealSurface.1.0.tar.gz"

    tags = ["hep"]

    maintainers("drbenmorgan")

    # Only versions relevant to Geant4 releases built by spack are added
    version("2.2", sha256="9954dee0012f5331267f783690e912e72db5bf52ea9babecd12ea22282176820")
    version("2.1.1", sha256="90481ff97a7c3fa792b7a2a21c9ed80a40e6be386e581a39950c844b2dd06f50")
    version("2.1", sha256="2a287adbda1c0292571edeae2082a65b7f7bd6cf2bf088432d1d6f889426dcf3")
    version("1.0", sha256="3e2d2506600d2780ed903f1f2681962e208039329347c58ba1916740679020b1")

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, "data"))
        install_path = join_path(prefix.share, "data", self.g4datasetname)
        install_tree(self.stage.source_path, install_path)

    def setup_dependent_run_environment(self, env, dependent_spec):
        install_path = join_path(self.prefix.share, "data", self.g4datasetname)
        env.set("G4REALSURFACEDATA", install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return (
            "http://geant4-data.web.cern.ch/geant4-data/datasets/{0}RealSurface.{1}.tar.gz".format(
                "G4" if version > Version("1.0") else "", version
            )
        )

    @property
    def g4datasetname(self):
        spec = self.spec
        return "RealSurface{0}".format(spec.version)
