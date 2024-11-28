# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Utilities for interacting with files,
like those in llnl.util.filesystem, but which require logic from spack.util
"""

import glob
import os
import re
import sys
from typing import List, Optional, Union

from llnl.util import tty
from llnl.util.filesystem import join_path, windows_drive
from llnl.util.lang import memoized

import spack.config
import spack.operating_systems.windows_os as winOs
import spack.util.environment
import spack.util.windows_registry
from spack.util.executable import Executable, which


class WindowsCompilerExternalPaths:
    @staticmethod
    def find_windows_compiler_root_paths() -> List[str]:
        """Helper for Windows compiler installation root discovery

        At the moment simply returns location of VS install paths from VSWhere
        But should be extended to include more information as relevant"""
        return list(winOs.WindowsOs().vs_install_paths)

    @staticmethod
    def find_windows_compiler_cmake_paths() -> List[str]:
        """Semi hard-coded search path for cmake bundled with MSVC"""
        return [
            os.path.join(
                path, "Common7", "IDE", "CommonExtensions", "Microsoft", "CMake", "CMake", "bin"
            )
            for path in WindowsCompilerExternalPaths.find_windows_compiler_root_paths()
        ]

    @staticmethod
    def find_windows_compiler_ninja_paths() -> List[str]:
        """Semi hard-coded search heuristic for locating ninja bundled with MSVC"""
        return [
            os.path.join(path, "Common7", "IDE", "CommonExtensions", "Microsoft", "CMake", "Ninja")
            for path in WindowsCompilerExternalPaths.find_windows_compiler_root_paths()
        ]

    @staticmethod
    def find_windows_compiler_bundled_packages() -> List[str]:
        """Return all MSVC compiler bundled packages"""
        return (
            WindowsCompilerExternalPaths.find_windows_compiler_cmake_paths()
            + WindowsCompilerExternalPaths.find_windows_compiler_ninja_paths()
        )


class WindowsKitExternalPaths:
    @staticmethod
    def find_windows_kit_roots() -> List[str]:
        """Return Windows kit root, typically %programfiles%\\Windows Kits\\10|11\\"""
        if sys.platform != "win32":
            return []
        program_files = os.environ["PROGRAMFILES(x86)"]
        kit_base = os.path.join(program_files, "Windows Kits", "**")
        return glob.glob(kit_base)

    @staticmethod
    def find_windows_kit_bin_paths(
        kit_base: Union[Optional[str], Optional[list]] = None
    ) -> List[str]:
        """Returns Windows kit bin directory per version"""
        kit_base = WindowsKitExternalPaths.find_windows_kit_roots() if not kit_base else kit_base
        assert kit_base, "Unexpectedly empty value for Windows kit base path"
        if isinstance(kit_base, str):
            kit_base = kit_base.split(";")
        kit_paths = []
        for kit in kit_base:
            kit_bin = os.path.join(kit, "bin")
            kit_paths.extend(glob.glob(os.path.join(kit_bin, "[0-9]*", "*\\")))
        return kit_paths

    @staticmethod
    def find_windows_kit_lib_paths(
        kit_base: Union[Optional[str], Optional[list]] = None
    ) -> List[str]:
        """Returns Windows kit lib directory per version"""
        kit_base = WindowsKitExternalPaths.find_windows_kit_roots() if not kit_base else kit_base
        assert kit_base, "Unexpectedly empty value for Windows kit base path"
        if isinstance(kit_base, str):
            kit_base = kit_base.split(";")
        kit_paths = []
        for kit in kit_base:
            kit_lib = os.path.join(kit, "Lib")
            kit_paths.extend(glob.glob(os.path.join(kit_lib, "[0-9]*", "*", "*\\")))
        return kit_paths

    @staticmethod
    def find_windows_driver_development_kit_paths() -> List[str]:
        """Provides a list of all installation paths
        for the WDK by version and architecture
        """
        wdk_content_root = os.getenv("WDKContentRoot")
        return WindowsKitExternalPaths.find_windows_kit_lib_paths(wdk_content_root)

    @staticmethod
    def find_windows_kit_reg_installed_roots_paths() -> List[str]:
        reg = spack.util.windows_registry.WindowsRegistryView(
            "SOFTWARE\\Microsoft\\Windows Kits\\Installed Roots",
            root_key=spack.util.windows_registry.HKEY.HKEY_LOCAL_MACHINE,
        )
        if not reg:
            # couldn't find key, return empty list
            return []
        kit_root_reg = re.compile(r"KitsRoot[0-9]+")
        root_paths = []
        for kit_root in filter(kit_root_reg.match, reg.get_values().keys()):
            root_paths.extend(
                WindowsKitExternalPaths.find_windows_kit_lib_paths(reg.get_value(kit_root).value)
            )
        return root_paths

    @staticmethod
    def find_windows_kit_reg_sdk_paths() -> List[str]:
        sdk_paths = []
        sdk_regex = re.compile(r"v[0-9]+.[0-9]+")
        windows_reg = spack.util.windows_registry.WindowsRegistryView(
            "SOFTWARE\\WOW6432Node\\Microsoft\\Microsoft SDKs\\Windows",
            root_key=spack.util.windows_registry.HKEY.HKEY_LOCAL_MACHINE,
        )
        for key in filter(sdk_regex.match, [x.name for x in windows_reg.get_subkeys()]):
            reg = windows_reg.get_subkey(key)
            sdk_paths.extend(
                WindowsKitExternalPaths.find_windows_kit_lib_paths(
                    reg.get_value("InstallationFolder").value
                )
            )
        return sdk_paths


def find_win32_additional_install_paths() -> List[str]:
    """Not all programs on Windows live on the PATH
    Return a list of other potential install locations.
    """
    drive_letter = windows_drive()
    windows_search_ext = []
    cuda_re = r"CUDA_PATH[a-zA-Z1-9_]*"
    # The list below should be expanded with other
    # common Windows install locations as neccesary
    path_ext_keys = ["I_MPI_ONEAPI_ROOT", "MSMPI_BIN", "MLAB_ROOT", "NUGET_PACKAGES"]
    user = os.environ["USERPROFILE"]
    add_path = lambda key: re.search(cuda_re, key) or key in path_ext_keys
    windows_search_ext.extend([os.environ[key] for key in os.environ.keys() if add_path(key)])
    # note windows paths are fine here as this method should only ever be invoked
    # to interact with Windows
    # Add search path for default Chocolatey (https://github.com/chocolatey/choco)
    # install directory
    windows_search_ext.append("%s\\ProgramData\\chocolatey\\bin" % drive_letter)
    # Add search path for NuGet package manager default install location
    windows_search_ext.append(os.path.join(user, ".nuget", "packages"))
    windows_search_ext.extend(
        spack.config.get("config:additional_external_search_paths", default=[])
    )
    windows_search_ext.extend(spack.util.environment.get_path("PATH"))
    return windows_search_ext


def _ensure_file_on_win():
    """Ensures the file command is available on Windows
    If not, it is bootstrapped.
    No-op on all other platforms"""
    if sys.platform != "win32":
        return
    import spack.bootstrap

    with spack.bootstrap.ensure_bootstrap_configuration():
        spack.bootstrap.ensure_file_in_path_or_raise()


@memoized
def file_command(*args):
    """Creates entry point to `file` system command with provided arguments"""
    _ensure_file_on_win()
    file_cmd = which("file", required=True)
    for arg in args:
        file_cmd.add_default_arg(arg)
    return file_cmd


@memoized
def _get_mime_type():
    """Generate method to call `file` system command to aquire mime type
    for a specified path
    """
    if sys.platform == "win32":
        # -h option (no-dereference) does not exist in Windows
        return file_command("-b", "--mime-type")
    else:
        return file_command("-b", "-h", "--mime-type")


def mime_type(filename):
    """Returns the mime type and subtype of a file.

    Args:
        filename: file to be analyzed

    Returns:
        Tuple containing the MIME type and subtype
    """
    output = _get_mime_type()(filename, output=str, error=str).strip()
    tty.debug("==> " + output)
    type, _, subtype = output.partition("/")
    return type, subtype


def fix_darwin_install_name(path):
    """Fix install name of dynamic libraries on Darwin to have full path.

    There are two parts of this task:

    1. Use ``install_name('-id', ...)`` to change install name of a single lib
    2. Use ``install_name('-change', ...)`` to change the cross linking between
       libs. The function assumes that all libraries are in one folder and
       currently won't follow subfolders.

    Parameters:
        path (str): directory in which .dylib files are located
    """
    libs = glob.glob(join_path(path, "*.dylib"))
    for lib in libs:
        # fix install name first:
        install_name_tool = Executable("install_name_tool")
        install_name_tool("-id", lib, lib)
        otool = Executable("otool")
        long_deps = otool("-L", lib, output=str).split("\n")
        deps = [dep.partition(" ")[0][1::] for dep in long_deps[2:-1]]
        # fix all dependencies:
        for dep in deps:
            for loc in libs:
                # We really want to check for either
                #     dep == os.path.basename(loc)   or
                #     dep == join_path(builddir, os.path.basename(loc)),
                # but we don't know builddir (nor how symbolic links look
                # in builddir). We thus only compare the basenames.
                if os.path.basename(dep) == os.path.basename(loc):
                    install_name_tool("-change", dep, loc, lib)
                    break
