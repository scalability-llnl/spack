# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nextflow(Package):
    """Data-driven computational pipelines"""

    homepage = "http://www.nextflow.io"
    url = "https://github.com/nextflow-io/nextflow/releases/download/v0.24.1/nextflow"

    version('20.07.1', sha256='de4db5747a801af645d9b021c7b36f4a25c3ce1a8fda7705a5f37e8f9357443a', expand=False)
    version('0.25.6', sha256='9498806596c96ba87396194fa6f1d7d1cdb739990f83e7e89d1d055366c5a943', expand=False)
    version('0.24.1', sha256='0bfde5335b385e3cff99bf4aab619e583de5dc0849767240f675037a2e7c1d83', expand=False)
    version('0.23.3', sha256='ffe1c314962ff97ebf47b0567883e152522acfbf6fd5800200b1a7a0ca2896d2', expand=False)
    version('0.21.0', sha256='076089079479da0d91fe1ad7aad06816164ecbcf17f73c55e795b1db8462b28d', expand=False)
    version('0.20.1', sha256='02635f3371f76a10e12f7366508c90bacf532ab7c23ae03c895317a150a39bd4', expand=False)
    version('0.17.3', sha256='05563ee1474fbef22f65fa3080792dcb08d218dd1b1561c517ebff4346559dbe', expand=False)

    depends_on('java')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("nextflow", join_path(prefix.bin, "nextflow"))
        set_executable(join_path(prefix.bin, "nextflow"))
