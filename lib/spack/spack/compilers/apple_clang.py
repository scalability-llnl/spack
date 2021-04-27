# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path
import re
import shutil

import llnl.util.tty as tty
import llnl.util.lang
import spack.compiler
import spack.util.executable
import spack.version

from .clang import Clang


class AppleClang(Clang):
    openmp_flag = "-Xpreprocessor -fopenmp"

    @classmethod
    @llnl.util.lang.memoized
    def extract_version_from_output(cls, output):
        ver = 'unknown'
        match = re.search(
            # Apple's LLVM compiler has its own versions, so suffix them.
            r'^Apple (?:LLVM|clang) version ([^ )]+)',
            output,
            # Multi-line, since 'Apple clang' may not be on the first line
            # in particular, when run as gcc, it seems to output
            # "Configured with: --prefix=..." as the first line
            re.M,
        )
        if match:
            ver = match.group(match.lastindex)
        return ver

    @property
    def cxx11_flag(self):
        # Adapted from CMake's AppleClang-CXX rules
        # Spack's AppleClang detection only valid from Xcode >= 4.6
        if self.real_version < spack.version.ver('4.0.0'):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C++11 standard", "cxx11_flag", "Xcode < 4.0.0"
            )
        return "-std=c++11"

    @property
    def cxx14_flag(self):
        # Adapted from CMake's rules for AppleClang
        if self.real_version < spack.version.ver('5.1.0'):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C++14 standard", "cxx14_flag", "Xcode < 5.1.0"
            )
        elif self.real_version < spack.version.ver('6.1.0'):
            return "-std=c++1y"

        return "-std=c++14"

    @property
    def cxx17_flag(self):
        # Adapted from CMake's rules for AppleClang
        if self.real_version < spack.version.ver('6.1.0'):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C++17 standard", "cxx17_flag", "Xcode < 6.1.0"
            )
        return "-std=c++1z"

    def setup_custom_environment(self, pkg, env):
        """Set the DEVELOPER_DIR environment for the Xcode toolchain.

        On macOS, not all buildsystems support querying CC and CXX for the
        compilers to use and instead query the Xcode toolchain for what
        compiler to run. This side-steps the spack wrappers. In order to inject
        spack into this setup, we need to copy (a subset of) Xcode.app and
        replace the compiler executables with symlinks to the spack wrapper.
        Currently, the stage is used to store the Xcode.app copies. We then set
        the 'DEVELOPER_DIR' environment variables to cause the xcrun and
        related tools to use this Xcode.app.
        """
        super(AppleClang, self).setup_custom_environment(pkg, env)

        if not pkg.use_xcode:
            # if we do it for all packages, we get into big troubles with MPI:
            # filter_compilers(self) will use mockup XCode compilers on macOS
            # with Clang. Those point to Spack's compiler wrappers and
            # consequently render MPI non-functional outside of Spack.
            return

        # Use special XCode versions of compiler wrappers when using XCode
        # Overwrites build_environment's setting of SPACK_CC and SPACK_CXX
        xcrun = spack.util.executable.Executable('xcrun')
        xcode_clang = xcrun('-f', 'clang', output=str).strip()
        xcode_clangpp = xcrun('-f', 'clang++', output=str).strip()
        env.set('SPACK_CC', xcode_clang, force=True)
        env.set('SPACK_CXX', xcode_clangpp, force=True)

        xcode_select = spack.util.executable.Executable('xcode-select')

        # Get the path of the active developer directory
        real_root = xcode_select('--print-path', output=str).strip()

        # The path name can be used to determine whether the full Xcode suite
        # or just the command-line tools are installed
        if real_root.endswith('Developer'):
            # The full Xcode suite is installed
            pass
        else:
            if real_root.endswith('CommandLineTools'):
                # Only the command-line tools are installed
                msg  = 'It appears that you have the Xcode command-line tools '
                msg += 'but not the full Xcode suite installed.\n'

            else:
                # Xcode is not installed
                msg  = 'It appears that you do not have Xcode installed.\n'

            msg += 'In order to use Spack to build the requested application, '
            msg += 'you need the full Xcode suite. It can be installed '
            msg += 'through the App Store. Make sure you launch the '
            msg += 'application and accept the license agreement.\n'

            raise OSError(msg)

        real_root = os.path.dirname(os.path.dirname(real_root))
        developer_root = os.path.join(spack.stage.get_stage_root(),
                                      'xcode-select',
                                      self.name,
                                      str(self.version))
        xcode_link = os.path.join(developer_root, 'Xcode.app')

        if not os.path.exists(developer_root):
            tty.warn('Copying Xcode from %s to %s in order to add spack '
                     'wrappers to it. Please do not interrupt.'
                     % (real_root, developer_root))

            # We need to make a new Xcode.app instance, but with symlinks to
            # the spack wrappers for the compilers it ships. This is necessary
            # because some projects insist on just asking xcrun and related
            # tools where the compiler runs. These tools are very hard to trick
            # as they do realpath and end up ignoring the symlinks in a
            # "softer" tree of nothing but symlinks in the right places.
            shutil.copytree(
                real_root, developer_root, symlinks=True,
                ignore=shutil.ignore_patterns(
                    'AppleTV*.platform', 'Watch*.platform', 'iPhone*.platform',
                    'Documentation', 'swift*'
                ))

            real_dirs = [
                'Toolchains/XcodeDefault.xctoolchain/usr/bin',
                'usr/bin',
            ]

            bins = ['c++', 'c89', 'c99', 'cc', 'clang', 'clang++', 'cpp']

            for real_dir in real_dirs:
                dev_dir = os.path.join(developer_root,
                                       'Contents',
                                       'Developer',
                                       real_dir)
                for fname in os.listdir(dev_dir):
                    if fname in bins:
                        os.unlink(os.path.join(dev_dir, fname))
                        os.symlink(
                            os.path.join(spack.paths.build_env_path, 'cc'),
                            os.path.join(dev_dir, fname))

            os.symlink(developer_root, xcode_link)

        env.set('DEVELOPER_DIR', xcode_link)
