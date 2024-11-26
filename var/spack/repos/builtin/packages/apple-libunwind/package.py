# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AppleLibunwind(Package):
    """Placeholder package for Apple's analogue to non-GNU libunwind"""

    homepage = "https://opensource.apple.com/source/libunwind/libunwind-35.3/"

    provides("unwind")

    # The 'conflicts' directive only accepts valid spack specs;
    # platforms cannot be negated -- 'platform!=darwin' is not a valid
    # spec -- so expressing a conflict for any platform that isn't
    # Darwin must be expressed by listing a conflict with every
    # platform that isn't Darwin/macOS
    conflicts("platform=linux")

    # Override the fetcher method to throw a useful error message;
    # avoids GitHub issue (#7061) in which the opengl placeholder
    # package threw a generic, uninformative error during the `fetch`
    # step,
    @property
    def fetcher(self):
        msg = """This package is intended to be a placeholder for Apple's
        system-provided, non-GNU-compatible libunwind library.

        Add to your packages.yaml:

        packages:
          apple-libunwind:
            buildable: False
            externals:
            - spec: apple-libunwind@35.3
              prefix: /usr
        """
        raise InstallError(msg)

    @fetcher.setter  # Since fetcher is read-write, must override both
    def fetcher(self):
        _ = self.fetcher

    def install(self, spec, prefix):
        # sanity_check_prefix requires something in the install directory
        mkdirp(prefix.lib)

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
