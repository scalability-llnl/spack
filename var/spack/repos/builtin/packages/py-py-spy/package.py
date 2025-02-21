# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPySpy(CargoPackage):
    """A Sampling Profiler for Python."""

    homepage = "https://github.com/benfred/py-spy"
    url = "https://github.com/benfred/py-spy/archive/v0.3.8.tar.gz"

    license("MIT", checked_by="lgarrison")

    version("0.4.0", sha256="13a5c4b949947425670eedac05b6dd27edbc736b75f1587899efca1a7ef79ac3")
    version("0.3.8", sha256="9dbfd0ea79ef31a2966891e86cf6238ed3831938cf562e71848e07b7009cf57d")
    version("0.3.3", sha256="41454d3d9132da45c72f7574faaff65f40c757720293a277ffa5ec5a4b44f902")

    # TODO: uses cargo to download and build dozens of dependencies.
    # Need to figure out how to manage these with Spack once we have a
    # CargoPackage base class.
    depends_on("unwind")
    depends_on("libunwind components=ptrace", when="^[virtuals=unwind] libunwind")
