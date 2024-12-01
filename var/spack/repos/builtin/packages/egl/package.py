# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import sys

from spack.package import *


class Egl(BundlePackage):
    """Placeholder for external EGL(OpenGL) libraries from hardware vendors"""

    homepage = "https://www.khronos.org/egl"
    maintainers("biddisco")

    version("1.5")

    # This should really be when='platform=linux' but can't because of a
    # current bug in when and how ArchSpecs are constructed
    if sys.platform.startswith("linux"):
        provides("gl@4.5")

    # conflict with GLX
    conflicts("glx")

    # not always available, but sometimes
    executables = ["^eglinfo$"]

    @classmethod
    def determine_version(cls, exe):
        if exe:
            output = Executable(exe)(output=str, error=str)
            match = re.search(r"EGL version string: (\S+)", output)
            return match.group(1) if match else None
        else:
            return None

    # Override the fetcher method to throw a useful error message;
    # fixes GitHub issue (#7061) in which this package threw a
    # generic, uninformative error during the `fetch` step,
    @property
    def fetcher(self):
        msg = """This package is intended to be a placeholder for
        system-provided EGL(OpenGL) libraries from hardware vendors.  Please
        download and install EGL drivers/libraries for your graphics
        hardware separately, and then set that up as an external package.
        An example of a working packages.yaml:

        packages:
          egl:
            buildable: False
            externals:
            - spec: egl@1.5.0
              prefix: /usr/

        In that case, /usr/ should contain these two folders:

        include/EGL/      (egl headers, including "egl.h")
        lib               (egl libraries, including "libEGL.so")

        """
        raise InstallError(msg)

    @fetcher.setter  # Since fetcher is read-write, must override both
    def fetcher(self):
        _ = self.fetcher

    @property
    def headers(self):
        return self.egl_headers

    @property
    def libs(self):
        return self.egl_libs

    @property
    def egl_headers(self):
        header_name = "GL/gl"
        gl_header = find_headers(header_name, root=self.prefix, recursive=True)
        header_name = "EGL/egl"
        egl_header = find_headers(header_name, root=self.prefix, recursive=True)
        return gl_header + egl_header

    @property
    def egl_libs(self):
        lib_name = "libGL"
        gl_lib = find_libraries(lib_name, root=self.prefix, recursive=True)
        lib_name = "libEGL"
        egl_lib = find_libraries(lib_name, root=self.prefix, recursive=True)
        return gl_lib + egl_lib
