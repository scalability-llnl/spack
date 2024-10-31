# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWatchdog(PythonPackage):
    """Python library and shell utilities to monitor filesystem events."""

    homepage = "https://github.com/gorakhargosh/watchdog"
    pypi = "watchdog/watchdog-0.10.3.tar.gz"

    license("Apache-2.0")

    version("2.1.6", sha256="a36e75df6c767cbf46f61a91c70b3ba71811dfa0aca4a324d9407a06a8b7a2e7")
    version("0.10.3", sha256="4214e1379d128b0588021880ccaf40317ee156d4603ac388b9adcf29165e0c04")
    version("0.10.2", sha256="c560efb643faed5ef28784b2245cf8874f939569717a4a12826a173ac644456b")
    version("0.10.1", sha256="d64786787b14c8c6a71a8cc014056776ba6b52e85d1164ef2ab50aec02723a3d")
    version("0.10.0", sha256="8e800496cdfb921cfdc62b58a11966d0d2203a35dc005b4b5b8e1ab3097b2eb5")
    version("0.9.0", sha256="965f658d0732de3188211932aeb0bb457587f04f63ab4c1e33eab878e9de961d")
    version("0.8.3", sha256="7e65882adb7746039b6f3876ee174952f8eaaa34491ba34333ddf1fe35de4162")
    version("0.8.2", sha256="33a9ab3ce2e6b1aca4d2a50752231668d69bdba4ab096d9742195ccfbef1e023")
    version("0.8.1", sha256="d6ec6be582b244834a888c8ccc2d451816184ab104b5454b5e5cd7649e8f671c")
    version("0.8.0", sha256="a86bb2d8b94bb4bf76fcc2ff36f741c0e511ec24c4d3a1059b47d49e377d64f5")
    version("0.7.1", sha256="54ca64fdf0a2fb23cecba6349f9587e62fd31840ae22a71898a65adb8c6b52f9")

    depends_on("c", type="build")  # generated

    variant(
        "watchmedo",
        default=False,
        when="@0.10:",
        description="Build optional watchmedo utility script",
    )

    depends_on("python@2.6:2,3.2:", type=("build", "run"), when="@0.9.0:")
    depends_on("python@2.7:2,3.4:", type=("build", "run"), when="@0.10.0:")
    depends_on("python@3.6:", type=("build", "run"), when="@2.1.6:")

    depends_on("py-setuptools", type="build")

    depends_on("py-pyyaml@3.9:", type=("build", "run"), when="@0.7.1")
    depends_on("py-pyyaml@3.10:", type=("build", "run"), when="@0.8.0:0.8.3")
    depends_on("py-pyyaml@3.10:", type=("build", "run"), when="@0.9.0")
    depends_on("py-pyyaml@3.10:", type=("build", "run"), when="@0.10.0: +watchmedo")
    depends_on("py-pyyaml@3.10:", type=("build", "run"), when="@2.1.6: +watchmedo")

    depends_on("py-argh@0.8.1:", type=("build", "run"), when="@0.7.1")
    depends_on("py-argh@0.24.1:", type=("build", "run"), when="@0.8.0:0.9.0")
    depends_on("py-argh@0.24.1:", type=("build", "run"), when="@0.10.0:0.10.3 +watchmedo")

    depends_on("py-pathtools@0.1.1:", type=("build", "run"), when="@0:0.10.3")

    # Missing dependencies
    conflicts("platform=darwin", when="@0.10.0:0.10.1")
    # depends_on('py-pyobjc-framework-cocoa@4.2.2:',
    #            when='@0.10.0:0.10.1 platform=darwin')
    # depends_on('py-pyobjc-framework-fsevents@4.2.2:',
    #            when='@0.10.0:0.10.1 platform=darwin')
