# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Khmer(PythonPackage):
    """khmer is a software library and toolkit for k-mer based analysis and transformation
    of nucleotide sequence data"""

    homepage = "https://khmer.readthedocs.io/en/latest/"
    pypi = "khmer/khmer-2.1.1.tar.gz"

    license("BSD-3-Clause", checked_by="A-N-Other")

    version("2.1.1", sha256="a709606910bb8679bd8525e9d2bf6d1421996272e343b54cc18090feb2fdbe24")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # https://github.com/dib-lab/khmer/pull/1922 ...
    conflicts("^python@3.12:")

    depends_on("py-setuptools@3.4.1:", type="build")
    depends_on("py-pytest-runner@2", type="build")
    depends_on("py-screed@1:", type=("build", "run"))
    # abandoned `bz2file` dependency dropped in favour of the patch below

    depends_on("openmpi")

    def patch(self):
        filter_file("bz2file", "bz2", join_path("khmer", "kfile.py"))
        filter_file("'bz2file', ", "", "setup.py")
