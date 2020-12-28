# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sratoolkit(Package):
    """The NCBI SRA Toolkit enables reading ("dumping") of sequencing files
       from the SRA database and writing ("loading") files into the .sra
       format."""

    homepage = "https://trace.ncbi.nlm.nih.gov/Traces/sra"
    url      = "https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.8.2-1/sratoolkit.2.8.2-1-centos_linux64.tar.gz"

    maintainers = ['robqiao']

    version('2.10.7', sha256='b3f319974f0c7a318554d6383a13dd30f7d447533d92b6fd3bd057d3524e0140')
    version('2.9.6', sha256='faab687c822d0c02956f73f35e04875dde420ce9f602b88bbf3f2e8d79a17155')
    version('2.9.2', sha256='17dbe13aa1ed7955d31e1e76e8b62786e80a77e9ed9d396631162dc3ad8b716d')
    version('2.8.2-1', sha256='b053061aae7c6d00162fe0f514be4128a60365b4b2b5b36e7f4798b348b55cf5')

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin, symlinks=True)
        install_tree('example', prefix.example)
        install_tree('schema', prefix.schema)
