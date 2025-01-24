# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AppleLibunwind(Package):
    """Placeholder package for Apple's analogue to non-GNU libunwind"""

    homepage = "https://opensource.apple.com/source/libunwind/libunwind-35.3/"

    provides("unwind")

    # Only supported on 'platform=darwin'
    conflicts("platform=linux")
    conflicts("platform=windows")

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

    @property
    def headers(self):
        return HeaderList(join_path(self.prefix, "usr/include"))

    @property
    def libs(self):
        return LibraryList(join_path(self.prefix, "usr/lib"))
