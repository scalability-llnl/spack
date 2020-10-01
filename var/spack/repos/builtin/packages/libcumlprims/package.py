# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class Libcumlprims(Package):
    """libcuMLPrims library"""

    homepage = "https://rapids.ai"
    url      = "https://anaconda.org/nvidia/libcumlprims/0.15.0/download/linux-64/libcumlprims-0.15.0-cuda11.0_gdbd0d39_0.tar.bz2"

    version('0.15.0-cuda11.0_gdbd0d39_0', sha256='0edc55767f06f533fbff7a0fecaf6e6d4f82eec39604b3874a07b5609f79ece8')
    version('0.15.0-cuda10.2_gdbd0d39_0', sha256='b7a8740de0d15380829f42fcb078567e73ab7d29b14be073376153bf2d8ec945')
    version('0.15.0-cuda10.1_gdbd0d39_0', sha256='f055f904b5ef67995869b0bc648d9fe30839b08e77cb335573bf9f1c816d4d9b')

    depends_on('cuda@11.0.0:11.0.999', when='@0.15.0-cuda11.0_gdbd0d39_0')
    depends_on('cuda@10.2.0:10.2.999', when='@0.15.0-cuda10.2_gdbd0d39_0')
    depends_on('cuda@10.1.0:10.1.999', when='@0.15.0-cuda10.1_gdbd0d39_0')

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path('SPACK_INCLUDE_DIRS', self.prefix.include.cumlprims)

    def url_for_version(self, version):
        url = "https://anaconda.org/nvidia/libcumlprims/{0}/download/linux-64/libcumlprims-{1}.tar.bz2"
        return url.format(version.up_to(3), version)

    def install(self, spec, prefix):
        cp = which('cp')

        cp('-r', os.path.join(self.stage.source_path, '.'), prefix)
