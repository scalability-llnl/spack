# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RXlconnect(RPackage):
    """Excel Connector for R.

    Provides comprehensive functionality to read, write and format Excel
    data."""

    cran = "XLConnect"

    version("1.0.10", sha256="e3c267cb1e6a6fb3a9fb132e60649182ee7a28e4e9188c72786fb843aad6e2b4")
    version("1.0.7", sha256="821dba231c3c3147455e7525119b51e5dc001984c638b7ce519d0974b32de677")
    version("1.0.6", sha256="b233b9f74d1464b78d5dd28bd8a1fa46ca6254518da2d3bda3c978a3f4aaa4f9")
    version("1.0.5", sha256="975c2ef57f28ccfac79ae5d285b7e82e60791fb121052616c10bc52e2bca16ad")
    version("1.0.1", sha256="927aa34a3c81c12bf156e55edca9e2f5186c31435cce23feda4b906d049d6e39")
    version("0.2-15", sha256="26e1d8db65974719adbc25f1327c584003eb562dc1bb2121bffc2550cf3178b3")
    version("0.2-14", sha256="d1013ed26947572bad97d62a3d66346f74993cf96c6408d21d5b6ee567468819")
    version("0.2-12", sha256="500624f078fb27338aa91d8710daaf38633659a9b17f7cb713232a3d66f9f62c")
    version("0.2-11", sha256="17c5eddd00b933fd7a2ab9d942c813046d45f0af487f8d5b11011a004db69d0b")

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r@3.6.0:", type=("build", "run"), when="@1.0.6:")
    depends_on("r-rjava", type=("build", "run"))
    depends_on("r-rjava@1.0-1:", type=("build", "run"), when="@1.0.6:")
    depends_on("java@6:")
    depends_on("java@8:11", when="@1.0.1:")
    depends_on("java@8:17", when="@1.0.5:")

    depends_on("r-xlconnectjars@0.2-9", type=("build", "run"), when="@0.2-11")
    depends_on("r-xlconnectjars@0.2-12", type=("build", "run"), when="@0.2-12")
    depends_on("r-xlconnectjars@0.2-14", type=("build", "run"), when="@0.2-14")
    depends_on("r-xlconnectjars@0.2-15", type=("build", "run"), when="@0.2-15")
