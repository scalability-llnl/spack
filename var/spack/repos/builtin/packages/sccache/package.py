# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

import spack.build_systems
import spack.build_systems.cargo
from spack.package import *


class Sccache(CargoPackage):
    """Sccache is a ccache-like tool. It is used as a compiler wrapper and avoids
    compilation when possible. Sccache has the capability to utilize caching in
    remote storage environments, including various cloud storage options, or
    alternatively, in local storage."""

    homepage = "https://github.com/mozilla/sccache"
    url = "https://github.com/mozilla/sccache/archive/refs/tags/v0.8.2.tar.gz"

    tags = ["build-tools"]

    executables = [r"^sccache$", r"^sscache-dist$"]

    license("Apache-2.0", checked_by="pranav-sivaraman")

    version("0.8.2", sha256="2b3e0ef8902fe7bcdcfccf393e29f4ccaafc0194cbb93681eaac238cdc9b94f8")

    depends_on("rust@1.75:", when="@0.8.2:")
    depends_on("rust@1.70:", when="@0.7.7:")
    depends_on("rust@1.67.1:")  # for 0.6/0.7.1 and newer, but may work for even older versions.
    depends_on("pkgconfig", type="build", when="platform=linux")

    depends_on("openssl", when="platform=linux")

    variant(
        "dist-server",
        default=False,
        description="Enables the sccache-dist binary",
        when="platform=linux",
    )

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.match(r"sccache (\S+)", output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version_str):
        if any(os.path.basename(path) == "sccache-dist" for path in exes):
            return "+dist-server"
        else:
            return "~dist-server"


class CargoBuilder(spack.build_systems.cargo.CargoBuilder):

    @property
    def build_args(self):
        if self.spec.satisfies("+dist-server"):
            return ["--features=dist-server"]

        return []
