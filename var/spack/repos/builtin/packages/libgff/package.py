# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libgff(CMakePackage):
    """Lightweight GTF/GFF Parser, exposes a C++ interface without drawing in
    a heavyweight dependency."""

    homepage = "https://github.com/COMBINE-lab/libgff/"
    url = "https://github.com/COMBINE-lab/libgff/archive/v2.0.0.tar.gz"

    # notify when the package is updated.
    maintainers("ajxander12")

    version("2.0.0", sha256="7656b19459a7ca7d2fd0fcec4f2e0fd0deec1b4f39c703a114e8f4c22d82a99c")

    depends_on("cxx", type="build")  # generated
