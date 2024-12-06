# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Madx(CMakePackage):
    """MAD-X (Methodical Accelerator Design) is an application
    for designing particle accelerators."""

    homepage = "https://github.com/MethodicalAcceleratorDesign/MAD-X"
    url = "https://github.com/MethodicalAcceleratorDesign/MAD-X/archive/refs/tags/5.07.00.tar.gz"
    git = "https://github.com/MethodicalAcceleratorDesign/MAD-X.git"

    maintainers("wdconinc")

    # Supported MAD-X versions
    version("5.09.03", sha256="cd57f9451e3541a820814ad9ef72b6e01d09c6f3be56802fa2e95b1742db7797")
    version("5.09.00", sha256="fc2823cdb90a53c1422cca93a48b003c97c1e72641d9e925cd8f59b08f795c7a")
    version("5.08.01", sha256="89c943fcb474344a4f7d28de98e8eae0aec40f779bf908daff79043bf3520555")
    version("5.08.00", sha256="0b3fe2aca8899289ef7bfb98d745f13b8c4082e239f54f2662c9cad8d1e63a53")
    version("5.07.00", sha256="77c0ec591dc3ea76cf57c60a5d7c73b6c0d66cca1fa7c4eb25a9071e8fc67e60")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("x11", default=True, description="Turn on plotting using X11")

    # patch for gcc-11 to avoid error due to variable shadowing
    patch(
        "https://github.com/MethodicalAcceleratorDesign/MAD-X/commit/e7a434290df675b894f70026ce0c7c217330cce5.patch?full_index=1",
        sha256="d09c26f10b6b69d2cb209fee317f90804d92b419026d5181007559119daf33f6",
        when="@:5.07.00",
    )

    depends_on("cmake@2.8:", type="build")

    depends_on("libx11")
    depends_on("zlib-api")

    def cmake_args(self):
        args = [
            self.define("MADX_STATIC", False),  # Turn on for static linking
            self.define("MADX_LAPACK", True),  # Use system blas/lapack installation
            self.define("MADX_NTPSA", True),  # Build with NTPSA
            self.define("MADX_ONLINE", False),  # Build with Online model
            self.define_from_variant("MADX_X11", "x11"),  # Turn on plotting using X11
        ]
        return args
