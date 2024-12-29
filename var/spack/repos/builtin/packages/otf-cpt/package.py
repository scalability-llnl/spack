# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OtfCpt(CMakePackage):
    """Tool to collect and report model factors (aka. fundamental performance factors)
    for hybrid MPI + OpenMP applications on-the-fly."""

    # Add a proper url for your package's homepage here.
    homepage = (
        "https://github.com/RWTH-HPC/OTF-CPT?tab=readme-ov-file#on-the-fly-critical-path-tool"
    )
    git = "https://github.com/RWTH-HPC/OTF-CPT.git"

    maintainers("jgraciahlrs", "jprotze")

    license("Apache-2.0", checked_by="jgraciahlrs")

    version("0.9", tag="v0.9")

    depends_on("cxx", type="build")
    depends_on("mpi")
    conflicts(
        "%gcc",
        # Use a clang compiler with a matching libomp, e.g. 'sudo apt install libomp-14-dev':
        msg="gcc currently does not support OMPT, please use a clang-like compiler with libomp",
    )

    patch(
        "https://github.com/RWTH-HPC/OTF-CPT/commit/b58f83588a4c231b71ca48dcddd909e1ab318cc6.diff?full_index=1",
        sha256="35fadc3e61e5b7aa3a68272f701af3a242e30a435f1ddd679577ba35c7496565",
        when="@0.9",
    )
