# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyImmutabledict(PythonPackage):
    """A fork of frozendict, an immutable wrapper around
    dictionaries. It implements the complete mapping interface and can be used as a
    drop-in replacement for dictionaries where immutability is
    desired. The immutabledict constructor mimics dict, and all of the
    expected interfaces (iter, len, repr, hash, getitem) are
    provided. Note that an immutabledict does not guarantee the
    immutability of its values, so the utility of hash method is
    restricted by usage. The only difference is that the copy() method
    of immutable takes variable keyword arguments, which will be
    present as key/value pairs in the new, immutable copy."""

    homepage = "https://github.com/corenting/immutabledict"
    pypi = "immutabledict/immutabledict-2.2.1.tar.gz"

    license("MIT")

    version("2.2.1", sha256="1ddb0edf1bb6c70d0197eb90ce1fe2b2d58502334f5fdfde72d7c633d723ec3a")

    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
