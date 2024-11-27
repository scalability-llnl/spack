# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyfastaq(PythonPackage):
    """Manipulate FASTA and FASTQ files."""

    homepage = "https://github.com/sanger-pathogens/Fastaq"

    pypi = "pyfastaq/pyfastaq-3.12.1.tar.gz"

    version("3.17.0", sha256="40c6dc0cea72c0ab91d10e5627a26dea1783b7e5e3edcfff8e1dc960bfd71cdc")
    version("3.16.0", sha256="368f3f1752668283f5d1aac4ea80e9595a57dc92a7d4925d723407f862af0e4e")
    version("3.15.0", sha256="30013f38956535fddddedda03dc072e808704f6e026231dd1539869a08afcbe8")
    version("3.14.0", sha256="54dc8cc8b3d24111f6939cf563833b8e9e78777b9cf7b82ca8ddec04aa1c05f2")
    version("3.13.0", sha256="79bfe342e053d51efbc7a901489c62e996566b4baf0f33cde1caff3a387756af")
    version("3.12.1", sha256="996dee7c5583b9c06c0a96a9e539d5f4218c084a3b2ee757fb245b4222b2a829")
    version("3.12.0", sha256="a3a03db385e6eaffa44b659594877bf95d78ac1b1c93d5498a7f0b9e4c4fe2aa")

    depends_on("py-setuptools", type="build")
    depends_on("samtools", type="run")
    depends_on("gzip", type="run")
