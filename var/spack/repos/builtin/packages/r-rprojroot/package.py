# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRprojroot(RPackage):
    """Finding Files in Project Subdirectories.

    Robust, reliable and flexible paths to files below a project root.  The
    'root' of a project is defined as a directory that matches a certain
    criterion, e.g., it contains a certain regular file."""

    cran = "rprojroot"

    license("MIT")

    version("2.0.4", sha256="b5f463fb25a24dac7a4ca916be57dbe22b5262e1f41e53871ca83e57d4336e99")
    version("2.0.3", sha256="50604247470e910cecfe9b76df754bf96a0d701f81b732f7aa9c90a20d30f897")
    version("2.0.2", sha256="5fa161f0d4ac3b7a99dc6aa2d832251001dc92e93c828593a51fe90afd019e1f")
    version("1.3-2", sha256="df5665834941d8b0e377a8810a04f98552201678300f168de5f58a587b73238b")
    version("1.2", sha256="28b4d235ce67314528a0c1cc7e98faed42437b42e07fca18a59a80fdc3eefeb9")

    depends_on("r@3.0.0:", type=("build", "run"))

    depends_on("r-backports", type=("build", "run"), when="@:1.3-2")
