# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class AppleLibuuid(BundlePackage):
    """Placeholder package for Apple's analogue to non-GNU libuuid"""

    homepage = "https://opensource.apple.com/tarballs/Libsystem/"

    version('1353.100.2')

    provides('uuid')

    # Only supported on 'platform=darwin'
    conflicts('platform=linux')
    conflicts('platform=cray')

    @property
    def libs(self):
        """Export the Apple libuuid library.

        According to https://bugs.freedesktop.org/show_bug.cgi?id=105366,
        libuuid is provided as part of libsystem_c. The Apple libsystem_c
        library cannot be linked to directly using an absolute path; doing so
        will cause the linker to throw an error 'cannot link directly with
        /usr/lib/system/libsystem_c.dylib' and the linker will suggest linking
        with System.framework instead. Linking to this framework is equivalent
        to linking with libSystem.dylib, which can be confirmed on a macOS
        system by executing at a terminal the command `ls -l
        /System/Library/Frameworks/System.Framework` -- the file "System" is a
        symlink to `/usr/lib/libSystem.B.dylib`, and `/usr/lib/libSystem.dylib`
        also symlinks to this file. Running `otool -L /usr/lib/libSystem.dylib`
        confirms that it will link dynamically to
        `/usr/lib/system/libsystem_c.dylib`."""

        return LibraryList('/usr/lib/libSystem.dylib')

    @property
    def headers(self):
        """Export the Apple libuuid header."""
        return HeaderList(self.prefix.include.uuid.join('uuid.h'))
