# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import glob
import os
import re

import spack.util.windows_registry as winreg
from spack.package import *


class WinWdk(Package):
    """
    Windows Driver Kit development package
    """

    homepage = "https://learn.microsoft.com/en-us/windows-hardware/drivers/"
    tags = ["windows", "windows-system"]

    # The wdk has many libraries and executables. Record one for detection purposes
    libraries = ["mmos.lib"]

    version(
        "10.0.19041",
        sha256="5f4ea0c55af099f97cb569a927c3a290c211f17edcfc65009f5b9253b9827925",
        url="https://go.microsoft.com/fwlink/?linkid=2128854",
        expand=False,
    )
    version(
        "10.0.18362",
        sha256="c35057cb294096c63bbea093e5024a5fb4120103b20c13fa755c92f227b644e5",
        url="https://go.microsoft.com/fwlink/?linkid=2085767",
        expand=False,
    )
    version(
        "10.0.17763",
        sha256="e6e5a57bf0a58242363cd6ca4762f44739f19351efc06cad382cca944b097235",
        url="https://go.microsoft.com/fwlink/?linkid=2026156",
        expand=False,
    )
    version(
        "10.0.17134",
        sha256="48e636117bb7bfe66b1ade793cc8e885c42c880fadaee471782d31b5c4d13e9b",
        url="https://go.microsoft.com/fwlink/?linkid=873060",
        expand=False,
    )
    version(
        "10.0.16299",
        sha256="14efbcc849e5977417e962f1cd68357d21abf27393110b9d95983ad03fc22ef4",
        url="https://go.microsoft.com/fwlink/p/?linkid=859232",
        expand=False,
    )
    version(
        "10.0.15063",
        sha256="489b497111bc791d9021b3573bfd93086a28b598c7325ab255e81c6f5d80a820",
        url="https://go.microsoft.com/fwlink/p/?LinkID=845980",
        expand=False,
    )
    version(
        "10.0.14393",
        sha256="0bfb2ac9db446e0d98c29ef7341a8c8e8e7aa24bc72b00c5704a88b13f48b3cb",
        url="https://go.microsoft.com/fwlink/p/?LinkId=526733",
        expand=False,
    )

    variant(
        "plat", values=("x64", "x86", "arm", "arm64"), default="x64", description="Toolchain arch"
    )

    # need one to one dep on SDK per https://github.com/MicrosoftDocs/windows-driver-docs/issues/1550
    # additionally, the WDK needs to be paired with a version of the Windows SDK
    # as per https://learn.microsoft.com/en-us/windows-hardware/drivers/download-the-wdk#download-icon-step-2-install-windows-11-version-22h2-sdk
    depends_on("win-sdk@10.0.19041", when="@10.0.19041")
    depends_on("win-sdk@10.0.18362", when="@10.0.18362")
    depends_on("win-sdk@10.0.17763", when="@10.0.17763")
    depends_on("win-sdk@10.0.17134", when="@10.0.17134")
    depends_on("win-sdk@10.0.16299", when="@10.0.16299")
    depends_on("win-sdk@10.0.15063", when="@10.0.15063")
    depends_on("win-sdk@10.0.14393", when="@10.0.14393")

    for plat in ["linux", "darwin"]:
        conflicts("platform=%s" % plat)

    @classmethod
    def determine_version(cls, lib):
        """
        WDK is a set of drivers that we would like to
        be discoverable externally by Spack.
        The lib does not provide the WDK
        version so we derive from the lib path
        """
        version_match_pat = re.compile(r"[0-9][0-9].[0-9]+.[0-9][0-9][0-9][0-9][0-9]")
        ver_str = re.search(version_match_pat, lib)
        return ver_str if not ver_str else Version(ver_str.group())

    @classmethod
    def determine_variants(cls, libs, ver_str):
        """Allow for determination of toolchain arch for detected WGL"""
        variants = []
        for lib in libs:
            base, lib_name = os.path.split(lib)
            _, arch = os.path.split(base)
            variants.append("plat=%s" % arch)
        return variants

    def setup_dependent_environment(self):
        # This points to all core build extensions needed to build
        # drivers on Windows
        os.environ["WDKContentRoot"] = self.prefix

    @run_before("install")
    def rename_downloaded_executable(self):
        """WGL download is named by fetch based on name derived from Link redirection
        This name is not properly formated so that Windows understands it as an executable
        We rename so as to allow Windows to run the WGL installer"""
        installer = glob.glob(os.path.join(self.stage.source_path, "linkid=**"))
        if len(installer) > 1:
            raise RuntimeError(
                "Fetch has failed, unable to determine installer path from:\n%s"
                % "\n".join(installer)
            )
        installer = installer[0]
        os.rename(installer, os.path.join(self.stage.source_path, "wdksetup.exe"))

    def install(self, spec, prefix):
        install_args = ["/features", "+", "/quiet", "/installpath", self.prefix]
        with working_dir(self.stage.source_path):
            try:
                Executable("wdksetup.exe")(*install_args)
            except ProcessError as pe:
                reg = winreg.WindowsRegistryView(
                    "SOFTWARE\\Microsoft\\Windows Kits\\Installed Roots",
                    root_key=spack.util.windows_registry.HKEY.HKEY_LOCAL_MACHINE,
                )
                if not reg:
                    # No Kits are available, failure was genuine
                    raise pe
                else:
                    versions = [str(subkey) for subkey in reg.get_subkeys()]
                    versions = ",".join(versions) if len(versions) > 1 else versions[0]
                    plural = "s" if len(versions) > 1 else ""
                    raise InstallError(
                        "Cannot install WDK version %s. "
                        "Version%s %s already present on system."
                        "Please run `spack external find win-wdk` to use the WDK"
                        % (self.version, plural, versions)
                    )
