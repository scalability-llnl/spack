# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AppleLibunwind(BundlePackage):
    """This package is intended to be a placeholder for Apple's system-provided,
    non-GNU-compatible libunwind library.
    """

    homepage = "https://opensource.apple.com/source/libunwind/libunwind-35.3/"

    provides("unwind")

    requires("platform=darwin")

    @property
    def libs(self):
        """Export the Apple libunwind library. The Apple libunwind library
        cannot be linked to directly using an absolute path; doing so
        will cause the linker to throw an error 'cannot link directly
        with /usr/lib/system/libunwind.dylib' and the linker will
        suggest linking with System.framework instead. Linking to this
        framework is equivalent to linking with libSystem.dylib, which
        can be confirmed on a macOS system by executing at a terminal
        the command `ls -l
        /System/Library/Frameworks/System.Framework` -- the file
        "System" is a symlink to `/usr/lib/libSystem.B.dylib`, and
        `/usr/lib/libSystem.dylib` also symlinks to this file.

        Running `otool -L /usr/lib/libSystem.dylib` confirms that
        it will link dynamically to `/usr/lib/system/libunwind.dylib`.

        """
        libs = find_libraries("libSystem", self.prefix.lib, shared=True, recursive=False)
        if libs:
            return libs
        return None

    @property
    def headers(self):
        """Export the Apple libunwind header"""
        hdrs = HeaderList(find(self.prefix.include, "libunwind.h", recursive=False))
        return hdrs or None
