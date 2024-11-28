# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLog4r(RPackage):
    """A Fast and Lightweight Logging System for R, Based on 'log4j'.

    logr4 provides an object-oriented logging system that uses an API roughly
    equivalent to log4j and its related variants."""

    cran = "log4r"

    license("Artistic-2.0")

    version("0.4.3", sha256="dfe3d49d35a8d8f3ad63f156d18e860540a01bd0af0e343cbab3e31a2cf5904c")
    version("0.4.2", sha256="924a020565dcd05a2bc8283285fcae60f6b58b35e1be7c55acc0c703c7edfe34")
    version("0.3.2", sha256="14ba6b096283279f0accbde26a600771ab2df271db6c8eeb04d6f113107825a3")
    version("0.3.0", sha256="8e5d0221298410e48bee9d9a983a23e1834ce88592f9d931471bfdb05f37a691")
    version("0.2", sha256="321bee6babb92376b538624027a36e7d2a6c8edb360aa38ab0a6762dfea9081f")

    depends_on("c", type="build")  # generated
