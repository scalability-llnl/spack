# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libgssglue(AutotoolsPackage):
    """GSSAPI interface using mechanisms from other GSSAPI implementations."""

    homepage = "http://www.citi.umich.edu/projects/nfsv4/linux/"
    url = "http://www.citi.umich.edu/projects/nfsv4/linux/libgssglue/libgssglue-0.4.tar.gz"

    license("BSD-3-Clause")

    version("0.4", sha256="3f791a75502ba723e5e85e41e5e0c711bb89e2716b7c0ec6e74bd1df6739043a")
    version("0.3", sha256="d98a022af432b61fe2a1eb811b5916743ccb781e383da680f1a00fd1005a5174")
    version("0.2", sha256="3de4974e19e54048acdc465d3b3c6c006cb66d2952d36e6b0afc10012184dc91")

    depends_on("c", type="build")  # generated
