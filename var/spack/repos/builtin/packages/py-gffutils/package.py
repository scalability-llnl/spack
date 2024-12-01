# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGffutils(PythonPackage):
    """GFF and GTF file manipulation and interconversion

    gffutils is a Python package for working with and manipulating the GFF and
    GTF format files typically used for genomic annotations. Files are loaded
    into a sqlite3 database, allowing much more complex manipulation of
    hierarchical features (e.g., genes, transcripts, and exons) than is
    possible with plain-text methods alone."""

    homepage = "https://github.com/daler/gffutils"
    pypi = "gffutils/gffutils-0.10.1.tar.gz"

    maintainers("dorton21")

    license("MIT")

    version("0.10.1", sha256="a8fc39006d7aa353147238160640e2210b168f7849cb99896be3fc9441e351cb")

    depends_on("py-setuptools", type="build")
    depends_on("py-pyfaidx@0.5.5.2:", type=("build", "run"))
    depends_on("py-six@1.12.0:", type=("build", "run"))
    depends_on("py-argh@0.26.2:", type=("build", "run"))
    depends_on("py-argcomplete@1.9.4:", type=("build", "run"))
    depends_on("py-simplejson", type=("build", "run"))
