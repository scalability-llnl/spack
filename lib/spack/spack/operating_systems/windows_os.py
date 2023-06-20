# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import pathlib
import platform
import subprocess

from spack.error import SpackError
from spack.version import Version
from spack.util import windows_registry as winreg
from ._operating_system import OperatingSystem


def windows_version():
    """Windows version as a Version object"""
    # include the build number as this provides important information
    # for low lever packages and components like the SDK and WDK
    # The build number is the version component that would otherwise
    # be the patch version in sematic versioning, i.e. z of x.y.z
    return Version(platform.version())


class WindowsOs(OperatingSystem):
    """This class represents the Windows operating system.  This will be
    auto detected using the python platform.win32_ver() once we have a
    python setup that runs natively.  The Windows platform will be
    represented using the major version operating system number, e.g.
    10.
    """

    # First Strategy: Find MSVC directories using vswhere
    _compiler_search_paths = []
    comp_search_paths = []
    vs_install_paths = []
    root = os.environ.get("ProgramFiles(x86)") or os.environ.get("ProgramFiles")
    if root:
        try:
            extra_args = {"encoding": "mbcs", "errors": "strict"}
            paths = subprocess.check_output(  # type: ignore[call-overload] # novermin
                [
                    os.path.join(root, "Microsoft Visual Studio", "Installer", "vswhere.exe"),
                    "-prerelease",
                    "-requires",
                    "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
                    "-property",
                    "installationPath",
                    "-products",
                    "*",
                ],
                **extra_args,
            ).strip()
            vs_install_paths = paths.split("\n")
            msvc_paths = [os.path.join(path, "VC", "Tools", "MSVC") for path in vs_install_paths]
            for p in msvc_paths:
                comp_search_paths.extend(glob.glob(os.path.join(p, "*", "bin", "Hostx64", "x64")))
            if os.getenv("ONEAPI_ROOT"):
                comp_search_paths.extend(
                    glob.glob(
                        os.path.join(
                            str(os.getenv("ONEAPI_ROOT")), "compiler", "*", "windows", "bin"
                        )
                    )
                )
        except (subprocess.CalledProcessError, OSError, UnicodeDecodeError):
            pass
    _compiler_search_paths.extend(comp_search_paths)
    # Second strategy: Find MSVC via the registry
    msft = winreg.WindowsRegistryView("SOFTWARE\\WOW6432Node\\Microsoft", winreg.HKEY.HKEY_LOCAL_MACHINE)
    vs_entries = msft.find_subkeys(r"VisualStudio_.*")
    vs_paths = []
    def clean_vs_path(path):
        path = path.split(",")[0].lstrip("@")
        return str(pathlib.Path(path).parent / "..\\..")
    for entry in vs_entries:
        try:
            val = entry.get_subkey("Capabilities").get_value("ApplicationDescription").value
            vs_paths.append(clean_vs_path(val))
        except FileNotFoundError as e:
            if hasattr(e, "winerror"):
                if e.winerror == 2:
                    pass
                else:
                    raise
            else:
                raise

    _compiler_search_paths.extend(vs_paths)
    if _compiler_search_paths:
        compiler_search_paths = _compiler_search_paths

    def __init__(self):
        plat_ver = windows_version()
        if plat_ver < Version("10"):
            raise SpackError("Spack is not supported on Windows versions older than 10")
        super().__init__("windows{}".format(plat_ver), plat_ver)

    def __str__(self):
        return self.name
