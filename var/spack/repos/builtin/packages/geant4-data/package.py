# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Geant4Data(BundlePackage):
    """A bundle package to hold Geant4 data packages"""

    homepage = "http://geant4.cern.ch"

    maintainers("drbenmorgan")

    tags = ["hep"]

    version("11.3.0")
    version("11.2.2")
    version("11.2.0")
    version("11.1.0")
    version("11.0.0")
    version("10.7.4")
    version("10.7.3")
    version("10.7.2")
    version("10.7.1")
    version("10.7.0")
    version("10.6.3")
    version("10.6.2")
    version("10.6.1")
    version("10.6.0")
    version("10.5.1")
    version("10.4.3")
    version("10.4.0")
    version("10.3.3")
    version("10.0.4")

    # Add install phase so we can create the data "view"
    phases = ["install"]

    # For clarity, declare deps on a Major-Minor version basis as
    # they generally don't change on the patch level
    # Can move to declaring on a dataset basis if needed
    _datasets = {
        "11.3.0:11.3": [
            "g4ndl@4.7.1",
            "g4emlow@8.6.1",
            "g4photonevaporation@6.1",
            "g4radioactivedecay@6.1.2",
            "g4particlexs@4.1",
            "g4pii@1.3",
            "g4realsurface@2.2",
            "g4saiddata@2.0",
            "g4abla@3.3",
            "g4incl@1.2",
            "g4ensdfstate@3.0",
            "g4channeling@1.0",
        ],
        "11.2.2:11.2": [
            "g4ndl@4.7.1",
            "g4emlow@8.5",
            "g4photonevaporation@5.7",
            "g4radioactivedecay@5.6",
            "g4particlexs@4.0",
            "g4pii@1.3",
            "g4realsurface@2.2",
            "g4saiddata@2.0",
            "g4abla@3.3",
            "g4incl@1.2",
            "g4ensdfstate@2.3",
        ],
        "11.2.0:11.2.1": [
            "g4ndl@=4.7",
            "g4emlow@8.5",
            "g4photonevaporation@5.7",
            "g4radioactivedecay@5.6",
            "g4particlexs@4.0",
            "g4pii@1.3",
            "g4realsurface@2.2",
            "g4saiddata@2.0",
            "g4abla@3.3",
            "g4incl@1.2",
            "g4ensdfstate@2.3",
        ],
        "11.1.0:11.1": [
            "g4ndl@4.7",
            "g4emlow@8.2",
            "g4photonevaporation@5.7",
            "g4radioactivedecay@5.6",
            "g4particlexs@4.0",
            "g4pii@1.3",
            "g4realsurface@2.2",
            "g4saiddata@2.0",
            "g4abla@3.1",
            "g4incl@1.0",
            "g4ensdfstate@2.3",
        ],
        "11.0.0:11.0": [
            "g4ndl@4.6",
            "g4emlow@8.0",
            "g4photonevaporation@5.7",
            "g4radioactivedecay@5.6",
            "g4particlexs@4.0",
            "g4pii@1.3",
            "g4realsurface@2.2",
            "g4saiddata@2.0",
            "g4abla@3.1",
            "g4incl@1.0",
            "g4ensdfstate@2.3",
        ],
        "10.7.0:10.7": [
            "g4ndl@4.6",
            "g4emlow@7.13",
            "g4photonevaporation@5.7",
            "g4radioactivedecay@5.6",
            "g4pii@1.3",
            "g4realsurface@2.2",
            "g4saiddata@2.0",
            "g4abla@3.1",
            "g4incl@1.0",
            "g4ensdfstate@2.3",
        ],
        "10.7.1:10.7": ["g4particlexs@3.1.1"],
        "10.7.0": ["g4particlexs@3.1"],
        "10.6.0:10.6": [
            "g4ndl@4.6",
            "g4emlow@7.9.1",
            "g4photonevaporation@5.5",
            "g4radioactivedecay@5.4",
            "g4particlexs@2.1",
            "g4pii@1.3",
            "g4realsurface@2.1.1",
            "g4saiddata@2.0",
            "g4abla@3.1",
            "g4incl@1.0",
            "g4ensdfstate@2.2",
        ],
        "10.5.0:10.5": [
            "g4ndl@4.5",
            "g4emlow@7.7",
            "g4photonevaporation@5.3",
            "g4radioactivedecay@5.3",
            "g4particlexs@1.1",
            "g4pii@1.3",
            "g4realsurface@2.1.1",
            "g4saiddata@2.0",
            "g4abla@3.1",
            "g4incl@1.0",
            "g4ensdfstate@2.2",
        ],
        "10.4.0:10.4": [
            "g4ndl@4.5",
            "g4emlow@7.3",
            "g4photonevaporation@5.2",
            "g4radioactivedecay@5.2",
            "g4neutronxs@1.4",
            "g4pii@1.3",
            "g4saiddata@1.1",
            "g4abla@3.1",
            "g4ensdfstate@2.2",
        ],
        "10.4.2:10.4": ["g4realsurface@2.1.1"],
        "10.4.0:10.4.1": ["g4realsurface@2.1"],
        "10.3.0:10.3": [
            "g4ndl@4.5",
            "g4emlow@6.50",
            "g4neutronxs@1.4",
            "g4pii@1.3",
            "g4realsurface@1.0",
            "g4saiddata@1.1",
            "g4abla@3.0",
            "g4ensdfstate@2.1",
        ],
        "10.3.1:10.3": ["g4photonevaporation@4.3.2", "g4radioactivedecay@5.1.1"],
        "10.3.0": ["g4photonevaporation@4.3", "g4radioactivedecay@5.1"],
        "10.0.4": [
            "g4ndl@4.4",
            "g4emlow@6.35",
            "g4photonevaporation@3.0",
            "g4radioactivedecay@4.0",
            "g4neutronxs@1.4",
            "g4pii@1.3",
            "g4realsurface@1.0",
            "g4saiddata@1.1",
            "g4abla@3.0",
            "g4ensdfstate@1.0",
        ],
    }

    for _vers, _dsets in _datasets.items():
        _vers = "@" + _vers
        for _d in _dsets:
            depends_on(_d, type=("build", "run"), when=_vers)

    _datasets_tendl = {
        "11.0:11.3": "g4tendl@1.4",
        "10.4:10.7": "g4tendl@1.3.2",
        "10.3:10.3": "g4tendl@1.3",
    }

    variant("tendl", default=True, when="@10.3:", description="Enable G4TENDL")
    with when("+tendl"):
        for _vers, _d in _datasets_tendl.items():
            depends_on(_d, type=("build", "run"), when="@" + _vers)
    variant("nudexlib", default=True, when="@11.3.0:11.3", description="Enable G4NUDEXLIB")
    with when("+nudexlib"):
        depends_on("g4nudexlib@1.0", type=("build", "run"))
    variant("urrpt", default=True, when="@11.3.0:11.3", description="Enable G4URRPT")
    with when("+urrpt"):
        depends_on("g4urrpt@1.1", type=("build", "run"))

    @property
    def datadir(self):
        spec = self.spec
        return join_path(spec.prefix.share, "{0}-{1}".format(self.name, self.version.dotted))

    def install(self, spec, prefix):
        with working_dir(self.datadir, create=True):
            for s in spec.dependencies():
                if not s.name.startswith("g4"):
                    continue

                if not hasattr(s.package, "g4datasetname"):
                    raise InstallError(f"Dependency `{s.name}` does not expose `g4datasetname`")

                d = "{0}/data/{1}".format(s.prefix.share, s.package.g4datasetname)
                os.symlink(d, os.path.basename(d))
