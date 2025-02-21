# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScreed(PythonPackage):
    """screed: a Python library for loading FASTA and FASTQ sequences."""

    homepage = "https://screed.readthedocs.io/"
    pypi = "screed/screed-1.1.2.tar.gz"

    version("1.1.2", sha256="734ffa7a8a645286496d895b736f91d6b2988956e2fd42358123d93ec8519b6a")

    depends_on("py-setuptools@48:", type="build")
    depends_on("py-setuptools-scm@4:5", type="build")
    depends_on("py-setuptools-scm-git-archive", type="build")
    depends_on("py-wheel@0.29.0:", type="build")
