# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gperf(AutotoolsPackage, GNUMirrorPackage):
    """GNU gperf is a perfect hash function generator. For a given
    list of strings, it produces a hash function and hash table, in
    form of C or C++ code, for looking up a value depending on the
    input string. The hash function is perfect, which means that the
    hash table has no collisions, and the hash table lookup needs a
    single string comparison only."""

    homepage = "https://www.gnu.org/software/gperf/"
    gnu_mirror_path = "gperf/gperf-3.0.4.tar.gz"

    version('3.1',   sha256='588546b945bba4b70b6a3a616e80b4ab466e3f33024a352fc2198112cdbb3ae2')
    version('3.0.4', sha256='767112a204407e62dbc3106647cf839ed544f3cf5d0f0523aaa2508623aad63e')

    # NOTE: `make check` is known to fail tests
