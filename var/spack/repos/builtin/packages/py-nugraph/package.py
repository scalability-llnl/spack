# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNugraph(PythonPackage):
    """Graph Neural Network for neutrino physics event reconstruction"""

    pypi = "nugraph/nugraph-24.7.1.tar.gz"

    maintainers("vhewes")

    license("MIT", checked_by="vhewes")

    version("24.7.1", sha256="e1449e4a37049cc774ad026d4f2db339eb60bb59109a11920bb65a4061915de8")
    version("24.7.0", sha256="b95d93a1cbcd280a3529ce4782ef778b982d9d4edcc19f522442c38144895f65")
    version("24.4.0", sha256="5f888d065819b1ec7c33e7f829ad65eb963db2cf109a5d31b4caef49c004f86f")
    version("24.2.0", sha256="4765ea73b384e95a38a598499e77d805541e415049da9f6f46193f8bc281208a")
    version("23.11.1", sha256="b160996fca9615b2c7e6ed02fb780af5edaa97f6cdafd45abdf65ea0c7a6f2ca")
    version("23.11.0", sha256="a1e01a8c3143fc8db2cf8a3584d192a738d89eb865b1d52cd2994b24bd4175ec")
    version("23.10.0", sha256="8a0219318c6bd6d0d240e419ef88cdedd7e944276f0cce430d9ece423e06f1b8")

    depends_on("py-flit-core", type="build")

    depends_on("py-matplotlib")
    depends_on("py-numl")
    depends_on("py-pynvml")
    depends_on("py-seaborn")
    depends_on("py-pytorch-lightning")

    extends("python")
