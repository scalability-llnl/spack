# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import glob


class Geant4Data(BundlePackage):
    """A bundle package to hold Geant4 data packages"""

    homepage = "http://geant4.cern.ch"

    maintainers = ['drbenmorgan']

    tags = ['hep']

    version('10.7.1')
    version('10.7.0')
    version('10.6.3')
    version('10.6.2')
    version('10.6.1')
    version('10.6.0')
    version('10.5.1')
    version('10.4.3')
    version('10.4.0')
    version('10.3.3')

    # Add install phase so we can create the data "view"
    phases = ['install']

    # For clarity, declare deps on a Major-Minor version basis as
    # they generally don't change on the patch level
    # Can move to declaring on a dataset basis if needed
    # geant4@10.7.X
    depends_on("g4ndl@4.6", when='@10.7.0:10.7.9999')
    depends_on("g4emlow@7.13", when='@10.7.0:10.7.9999')
    depends_on("g4photonevaporation@5.7", when='@10.7.0:10.7.9999')
    depends_on("g4radioactivedecay@5.6", when='@10.7.0:10.7.9999')
    depends_on("g4particlexs@3.1.1", when='@10.7.1:10.7.9999')
    depends_on("g4particlexs@3.1", when='@10.7.0')
    depends_on("g4pii@1.3", when='@10.7.0:10.7.9999')
    depends_on("g4realsurface@2.2", when='@10.7.0:10.7.9999')
    depends_on("g4saiddata@2.0", when='@10.7.0:10.7.9999')
    depends_on("g4abla@3.1", when='@10.7.0:10.7.9999')
    depends_on("g4incl@1.0", when='@10.7.0:10.7.9999')
    depends_on("g4ensdfstate@2.3", when='@10.7.0:10.7.9999')

    # geant4@10.6.X
    depends_on("g4ndl@4.6", when='@10.6.0:10.6.9999')
    depends_on("g4emlow@7.9", when='@10.6.0')
    depends_on("g4emlow@7.9.1", when='@10.6.1:10.6.9999')
    depends_on("g4photonevaporation@5.5", when='@10.6.0:10.6.9999')
    depends_on("g4radioactivedecay@5.4", when='@10.6.0:10.6.9999')
    depends_on("g4particlexs@2.1", when='@10.6.0:10.6.9999')
    depends_on("g4pii@1.3", when='@10.6.0:10.6.9999')
    depends_on("g4realsurface@2.1.1", when='@10.6.0:10.6.9999')
    depends_on("g4saiddata@2.0", when='@10.6.0:10.6.9999')
    depends_on("g4abla@3.1", when='@10.6.0:10.6.9999')
    depends_on("g4incl@1.0", when='@10.6.0:10.6.9999')
    depends_on("g4ensdfstate@2.2", when='@10.6.0:10.6.9999')

    # geant4@10.5.X
    depends_on("g4ndl@4.5", when='@10.5.0:10.5.9999')
    depends_on("g4emlow@7.7", when='@10.5.0:10.5.9999')
    depends_on("g4photonevaporation@5.3", when='@10.5.0:10.5.9999')
    depends_on("g4radioactivedecay@5.3", when='@10.5.0:10.5.9999')
    depends_on("g4particlexs@1.1", when='@10.5.0:10.5.9999')
    depends_on("g4pii@1.3", when='@10.5.0:10.5.9999')
    depends_on("g4realsurface@2.1.1", when='@10.5.0:10.5.9999')
    depends_on("g4saiddata@2.0", when='@10.5.0:10.5.9999')
    depends_on("g4abla@3.1", when='@10.5.0:10.5.9999')
    depends_on("g4incl@1.0", when='@10.5.0:10.5.9999')
    depends_on("g4ensdfstate@2.2", when='@10.5.0:10.5.9999')

    # geant4@10.4.X
    depends_on("g4ndl@4.5", when='@10.4.0:10.4.9999')
    depends_on("g4emlow@7.3", when='@10.4.0:10.4.9999')
    depends_on("g4photonevaporation@5.2", when='@10.4.0:10.4.9999')
    depends_on("g4radioactivedecay@5.2", when='@10.4.0:10.4.9999')
    depends_on("g4neutronxs@1.4", when='@10.4.0:10.4.9999')
    depends_on("g4pii@1.3", when='@10.4.0:10.4.9999')

    depends_on("g4realsurface@2.1.1", when='@10.4.2:10.4.9999')
    depends_on("g4realsurface@2.1", when='@10.4.0:10.4.1')

    depends_on("g4saiddata@1.1", when='@10.4.0:10.4.9999')
    depends_on("g4abla@3.1", when='@10.4.0:10.4.9999')
    depends_on("g4ensdfstate@2.2", when='@10.4.0:10.4.9999')

    # geant4@10.3.X
    depends_on("g4ndl@4.5", when='@10.3.0:10.3.9999')
    depends_on("g4emlow@6.50", when='@10.3.0:10.3.9999')

    depends_on("g4photonevaporation@4.3.2", when='@10.3.1:10.3.9999')
    depends_on("g4photonevaporation@4.3", when='@10.3.0')

    depends_on("g4radioactivedecay@5.1.1", when='@10.3.1:10.3.9999')
    depends_on("g4radioactivedecay@5.1", when='@10.3.0')

    depends_on("g4neutronxs@1.4", when='@10.3.0:10.3.9999')
    depends_on("g4pii@1.3", when='@10.3.0:10.3.9999')
    depends_on("g4realsurface@1.0", when='@10.3.0:10.3.9999')
    depends_on("g4saiddata@1.1", when='@10.3.0:10.3.9999')
    depends_on("g4abla@3.0", when='@10.3.0:10.3.9999')
    depends_on("g4ensdfstate@2.1", when='@10.3.0:10.3.9999')

    def install(self, spec, prefix):
        spec = self.spec
        data = '{0}-{1}'.format(self.name, self.version.dotted)
        datadir = join_path(spec.prefix.share, data)

        with working_dir(datadir, create=True):
            for s in spec.dependencies():
                for d in glob.glob('{0}/data/*'.format(s.prefix.share)):
                    os.symlink(d, os.path.basename(d))
