# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class ConditionalVirtualDependency(Package):
    """Brings in a virtual dependency if certain conditions are met."""

    homepage = "https://dev.null"

    version("1.0")

    variant("stuff", default=True, description="nope")
    variant("mpi", default=False, description="nope")

    depends_on("stuff", when="+stuff")
    depends_on("mpi", when="+mpi")
