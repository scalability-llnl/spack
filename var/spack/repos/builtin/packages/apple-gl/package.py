# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class AppleGlBase(BundlePackage):
    homepage = "https://developer.apple.com/library/archive/documentation/GraphicsImaging/Conceptual/OpenGL-MacProgGuide/opengl_intro/opengl_intro.html"

    maintainers("aphecetche")

    def setup_dependent_build_environment(self, env, dependent_spec):
        # we try to setup a build environment with enough hints
        # for the build system to pick up on the Apple framework version
        # of OpenGL.
        # - for a cmake build we actually needs nothing at all as
        # find_package(OpenGL) will do the right thing
        # - for the rest of the build systems we'll assume that
        # setting the C_INCLUDE_PATH will be enough for the compilation phase
        # and *** for the link phase.
        env.prepend_path("C_INCLUDE_PATH", self.prefix[:-4])

    @property
    def headers(self):
        return HeaderList(
            join_path(self.prefix, "System/Library/Frameworks/OpenGL.framework/Headers")
        )

    @property
    def libs(self):
        return LibraryList(join_path(self.prefix, "System/Library/Frameworks/OpenGL.framework"))


class AppleGl(AppleGlBase):
    """Shim package for the core OpenGL library from Apple"""

    version("4.1.0")

    provides("gl@4.1")

    requires(
        "%apple-clang platform=darwin",
        msg="Apple-GL is only available on Darwin, when using Apple Clang",
    )
