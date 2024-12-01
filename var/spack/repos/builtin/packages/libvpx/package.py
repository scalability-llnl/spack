# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libvpx(AutotoolsPackage):
    """libvpx is a free software video codec library from Google and the
    Alliance for Open Media.
    It serves as the reference software implementation for the VP8 and VP9
    video coding formats, and for AV1 a special fork named libaom that was
    stripped of backwards compatibility.
    """

    homepage = "https://chromium.googlesource.com/webm/libvpx"
    url = "https://github.com/webmproject/libvpx/archive/refs/tags/v1.10.0.tar.gz"

    license("BSD-3-Clause")

    version("1.14.1", sha256="901747254d80a7937c933d03bd7c5d41e8e6c883e0665fadcb172542167c7977")

    # Deprecated versions
    # https://nvd.nist.gov/vuln/detail/CVE-2023-44488
    version(
        "1.10.0",
        sha256="85803ccbdbdd7a3b03d930187cb055f1353596969c1f92ebec2db839fa4f834a",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("pic", default=True, description="Produce position-independent code (for shared libs)")

    depends_on("yasm")

    def configure_args(self):
        extra_args = []
        if self.spec.satisfies("+pic"):
            extra_args.append("--enable-pic")
        return extra_args
