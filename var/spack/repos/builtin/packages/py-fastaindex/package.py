# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFastaindex(PythonPackage):
    """FastA index (.fai) handler compatible with samtools faidx is extended
    with 4 columns storing counts for A, C, G & T for each sequence.."""

    homepage = "https://github.com/lpryszcz/FastaIndex"
    pypi = "FastaIndex/FastaIndex-0.11rc7.tar.gz"

    license("GPL-3.0-or-later")

    version("0.11rc7", sha256="c130a2146bb178ea4f9d228e0d360787046ab4cb0ab53b5b43711dd57e31aff7")

    depends_on("py-setuptools", type="build")
