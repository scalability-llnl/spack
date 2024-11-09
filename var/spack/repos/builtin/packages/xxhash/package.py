# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xxhash(MakefilePackage):
    """xxHash is an Extremely fast Hash algorithm, running at RAM speed
    limits. It successfully completes the SMHasher test suite which
    evaluates collision, dispersion and randomness qualities of hash
    functions. Code is highly portable, and hashes are identical on all
    platforms (little / big endian).
    """

    homepage = "https://github.com/Cyan4973/xxHash"
    url = "https://github.com/Cyan4973/xxHash/archive/v0.6.5.tar.gz"

    license("BSD-2-Clause")

    version("0.8.2", sha256="baee0c6afd4f03165de7a4e67988d16f0f2b257b51d0e3cb91909302a26a79c4")
    version("0.8.1", sha256="3bb6b7d6f30c591dd65aaaff1c8b7a5b94d81687998ca9400082c739a690436c")
    version("0.8.0", sha256="7054c3ebd169c97b64a92d7b994ab63c70dd53a06974f1f630ab782c28db0f4f")
    version("0.7.4", sha256="4d9706c9da4fbdf901598f5e3b71db0eddd4ac962e827a73ebf75d66dfd820fe")
    version("0.6.5", sha256="19030315f4fc1b4b2cdb9d7a317069a109f90e39d1fe4c9159b7aaa39030eb95")
    version("0.6.4", sha256="4570ccd111df6b6386502791397906bf69b7371eb209af7d41debc2f074cdb22")
    version("0.6.3", sha256="d8c739ec666ac2af983a61dc932aaa2a8873df974d333a9922d472a121f2106e")
    version("0.6.2", sha256="e4da793acbe411e7572124f958fa53b280e5f1821a8bf78d79ace972950b8f82")
    version("0.6.1", sha256="a940123baa6c71b75b6c02836bae2155cd2f74f7682e1a1d6f7b889f7bc9e7f8")
    version("0.6.0", sha256="2adee77416e1bd53d1bf689d78947ff4e9a603aa319c84c9111ccf53f1a646e8")
    version("0.5.1", sha256="0171af39eefa06be1e616bc43b250d13bba417e4741135ec85c1fe8dc391997d")
    version("0.5.0", sha256="9605cd18d40d798eb1262bc0c2a154e1a3c138a6a9a0c4c792e855d0c08c23e1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    @property
    def build_targets(self):
        targets = []

        if "%nvhpc" in self.spec:
            if self.spec.satisfies("%nvhpc@:20.11"):
                targets.append("CFLAGS=-O1")

            if "avx512" in self.spec.target:
                # Workaround AVX512 compiler issue
                targets.append("CPPFLAGS=-DXXH_VECTOR=XXH_AVX2")

        return targets

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter("/usr/local", prefix)
