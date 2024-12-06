# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Emblmygff3(PythonPackage):
    """
    EMBLmyGFF3 converts an assembly in FASTA format along with associated
    annotation in GFF3 format into the EMBL flat file format which is the
    required format for submitting annotated assemblies to ENA.
    """

    homepage = "https://github.com/NBISweden/EMBLmyGFF3"
    url = "https://github.com/NBISweden/EMBLmyGFF3/archive/refs/tags/v2.2.tar.gz"

    maintainers("snehring")

    license("GPL-3.0-or-later")

    version("2.2", sha256="225b2b50da9064f779e164b2859506d7540d11fa78f7d41b5c0d94f02f7845c5")
    version("2.1", sha256="64aef403bc64088eca504b69acffb3fb16ec4448cd3d6c9692b7baf276b92fd2")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.8.0:", type=("build", "run"))
    depends_on("py-biopython@1.78:", type=("build", "run"))
    depends_on("py-bcbio-gff@0.6.4:", type=("build", "run"))
    depends_on("py-numpy@1.22:", type=("build", "run"))
