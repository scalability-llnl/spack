# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDoparallel(RPackage):
    """Foreach Parallel Adaptor for the 'parallel' Package.

    Provides a parallel backend for the %dopar% function using the parallel
    package."""

    cran = "doParallel"

    version("1.0.17", sha256="b96a25ad105a654d70c7b4ca27290dc9967bc47f4668b2763927a886b178abd7")
    version("1.0.16", sha256="f1bb26f964f30d47ae4d6cf2b0a2ca0c2122d376424875e82d9abe9e7b054eb2")
    version("1.0.15", sha256="71ad7ea69616468996aefdd8d02a4a234759a21ddde9ed1657e3c537145cd86e")
    version("1.0.11", sha256="4ccbd2eb46d3e4f5251b0c3de4d93d9168b02bb0be493656d6aea236667ff76a")
    version("1.0.10", sha256="70024b6950025cc027022ee409f382e5ad3680c0a25bcd404bfc16418be8add5")

    depends_on("r@2.14.0:", type=("build", "run"))
    depends_on("r-foreach@1.2.0:", type=("build", "run"))
    depends_on("r-iterators@1.0.0:", type=("build", "run"))
