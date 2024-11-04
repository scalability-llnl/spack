# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.util.executable
from spack.build_systems.autotools import AutotoolsBuilder
from spack.build_systems.cmake import CMakeBuilder
from spack.package import *


class FluxSched(CMakePackage, AutotoolsPackage):
    """A scheduler for flux-core"""

    homepage = "https://github.com/flux-framework/flux-sched"
    url = "https://github.com/flux-framework/flux-sched/releases/download/v0.5.0/flux-sched-0.5.0.tar.gz"
    git = "https://github.com/flux-framework/flux-sched.git"
    tags = ["radiuss", "e4s"]

    maintainers("grondo")

    license("LGPL-3.0-only")

    version("master", branch="master")
    version("0.38.0", sha256="0cb3efbd490256b28df580bb14f8e89c02084a9126e0b1754d6334a99ecfa969")
    version("0.37.0", sha256="b354d451183fcb8455e6a61d31e18c7f4af13e16a86b71216738f0991a7bcd50")
    version("0.36.1", sha256="0ee37ed364912f3f5a48ed5b5f5f21cb86cda43ff357486695b9454c217ad8b8")
    version("0.36.0", sha256="c20814eae65b6eb9f2c919dbcc216dd4b87f038a341cf99510cca88d43631c41")
    version("0.35.0", sha256="38fde51464f4e34ecbd1e4fbbf00267f96b639db5987257a7ad07f811e2f09d2")
    version("0.34.0", sha256="10c03d78fa2302de7ddf9599ea59fb7a2dc7ccf6f526fd9fbfc9e3ff6ba39713")
    version("0.33.1", sha256="d0a1e504226d69fa8a247e9090d94ccc5e5f5fb028aab805f9cd95379bd8b1b3")
    version("0.33.0", sha256="d2e97121aed29bb1c6bfac602d890edb2f0a18d5303205b266a33c66fff1d61c")
    version("0.32.0", sha256="f0b88881f0154057de3dd5485a3e1cfc0b9b64c98052bda7d5fed7c05b5e02f3")
    version("0.31.0", sha256="4440156b7f2d43e3db2cbfa0dbc43671074c397525f6b97e3748c3d96a035cdb")
    version("0.30.0", sha256="1ccb2e53f4caede0233f19b2707e868f0cee9d2c957a06f97c22936ba9a43552")
    version("0.29.0", sha256="b93b18788e677535aa8ef945cdbeeced6d1408a4d16cb4a816ead53f31dd78d2")
    version("0.28.0", sha256="9431c671bed5d76fd95b4a4a7f36224d4bf76f416a2a1a5c4908f3ca790d434d")
    version("0.27.0", sha256="1e131924440c904fa0c925b7aa14c47b97f4e67b43af7efd2ebc0ef7ce90eb7c")
    version("0.26.0", sha256="184faec800cf45952ef79bda113f710bf91a05be584034d36a3234627d4a54c7")
    version("0.25.0", sha256="a984b238d8b6968ef51f1948a550bf57887bf3da8002dcd1734ce26afc4bff07")
    version("0.24.0", sha256="e104eb740e94f26a6a690f1c299bbe643f88751cc14a2596f0779a19cfeb5e6f")
    version("0.23.0", sha256="159b62cc4d25ef3d5da5338511ff38449a893d8adca13383cda7b322295acc1c")
    version("0.22.0", sha256="33cab21b667eeccd5665c5f139293b7b3e17cd3847e5fb2633c0dbacb33c611f")
    version("0.21.1", sha256="4dbe8a2e06a816535ef43f34cec960c1e4108932438cd6dbb1d0040423f4477d")
    version("0.21.0", sha256="156fe5b078a7c0b2075a1f1925ec9303a608c846c93187272f52c23eea24e06d")
    version("0.20.0", sha256="1d2074e1458ba1e7a1d4c33341b9f09769559cd1b8c68edc32097e220c4240b8")
    version("0.19.0", sha256="8dffa8eaec95a81286f621639ef851c52dc4c562d365971233bbd91100c31ed2")
    version("0.18.0", sha256="a4d8a6444fdb7b857b26f47fdea57992b486c9522f4ff92d5a6f547d95b586ae")
    version("0.17.0", sha256="5acfcb757e2294a92eaa91be58ba9b42736b88b42d2937de4a78f4642b1c4933")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # Avoid the infinite symlink issue
    # This workaround is documented in PR #3543
    build_directory = "spack-build"

    variant("docs", default=False, description="Build flux manpages and docs")
    variant("cuda", default=False, description="Build dependencies with support for CUDA")

    # Needs to be seen if tis is needed once we remove the default variants
    depends_on(
        "boost+exception+filesystem+system+serialization+graph+container+regex@1.53.0,1.59.0: "
    )
    depends_on("py-pyyaml@3.10:", type=("build", "run"))
    depends_on("py-jsonschema@2.3:", type=("build", "run"))
    depends_on("libedit")
    depends_on("libxml2@2.9.1:")
    # pin yaml-cpp to 0.6.3 due to issue #886
    # https://github.com/flux-framework/flux-sched/issues/886
    depends_on("yaml-cpp@0.6.3")
    depends_on("uuid")
    depends_on("pkgconfig")
    conflicts("%gcc@:9.3", when="@0.34:")
    conflicts("%gcc@:11", when="@0.37:", msg="gcc version must be 12 or higher")
    conflicts("%clang@:14", when="@0.37:", msg="clang must be version 15 or higher")
    depends_on("py-sphinx@1.6.3:", when="+docs", type="build")

    depends_on("flux-core", type=("build", "link", "run"))
    depends_on("flux-core+cuda", when="+cuda", type=("build", "run", "link"))
    depends_on("flux-core@0.29.0:", when="@0.18.0", type=("build", "run", "link"))
    depends_on("flux-core@0.30.0:", when="@0.19.0", type=("build", "run", "link"))
    depends_on("flux-core@0.31.0:", when="@0.19.0", type=("build", "run", "link"))
    depends_on("flux-core@0.38.0:", when="@0.21.0", type=("build", "run", "link"))
    depends_on("flux-core@master", when="@master", type=("build", "run", "link"))

    # Need autotools when building on master:
    depends_on("autoconf", type="build", when="@master")
    depends_on("automake", type="build", when="@master")
    depends_on("libtool", type="build", when="@master")

    # Set default to cmake so master (and branches) use it
    build_system(
        conditional("cmake", when="@0.29.0:"),
        conditional("autotools", when="@:0.28.0"),
        default="cmake",
    )

    # Required dependencies
    with when("build_system=cmake"):
        generator("ninja")
        depends_on("cmake@3.18:", type="build")

    # Disable t5000-valgrind.t by default due to false positives not yet
    # in the suppressions file. (This patch will be in v0.21.0)
    patch("no-valgrind.patch", when="@:0.20.0")
    patch("jobid-sign-compare-fix.patch", when="@:0.22.0")

    def url_for_version(self, version):
        """
        Flux uses a fork of ZeroMQ's Collective Code Construction Contract
        (https://github.com/flux-framework/rfc/blob/master/spec_1.adoc).
        This model requires a repository fork for every stable release that has
        patch releases.  For example, 0.8.0 and 0.9.0 are both tags within the
        main repository, but 0.8.1 and 0.9.5 would be releases on the v0.8 and
        v0.9 forks, respectively.

        Rather than provide an explicit URL for each patch release, make Spack
        aware of this repo structure.
        """
        if version[-1] == 0:
            url = "https://github.com/flux-framework/flux-sched/releases/download/v{0}/flux-sched-{0}.tar.gz"
        else:
            url = "https://github.com/flux-framework/flux-sched-v{1}/releases/download/v{0}/flux-sched-{0}.tar.gz"
        return url.format(version.up_to(3), version.up_to(2))

    def setup(self):
        pass

    @when("@master")
    def setup(self):
        with working_dir(self.stage.source_path):
            # Allow git-describe to get last tag so flux-version works:
            git = which("git")
            # When using spack develop, this will already be unshallow
            try:
                git("fetch", "--unshallow")
                git("config", "remote.origin.fetch", "+refs/heads/*:refs/remotes/origin/*")
                git("fetch", "origin")
            except spack.util.executable.ProcessError:
                git("fetch")

    def autoreconf(self, spec, prefix):
        self.setup()
        if os.path.exists(self.configure_abs_path):
            return
        # make sure configure doesn't get confused by the staging symlink
        with working_dir(self.configure_directory):
            # Bootstrap with autotools
            bash = which("bash")
            bash("./autogen.sh")

    @when("@:0.20")
    def patch(self):
        """Fix build with clang@13 and gcc@11"""
        filter_file("NULL", "nullptr", "resource/schema/sched_data.hpp")
        filter_file("size_t", "std::size_t", "resource/planner/planner.h")

    @property
    def lua_version(self):
        return self.spec["lua"].version.up_to(2)

    @property
    def lua_share_dir(self):
        return os.path.join("share", "lua", str(self.lua_version))

    @property
    def lua_lib_dir(self):
        return os.path.join("lib", "lua", str(self.lua_version))

    def setup_run_environment(self, env):
        # If this package is external, we expect the external provider to set
        # things like LUA paths. So, we early return. If the package is not
        # external, properly set these environment variables to make sure the
        # user environment is configured correctly
        if self.spec.external:
            return
        env.prepend_path(
            "LUA_PATH", os.path.join(self.spec.prefix, self.lua_share_dir, "?.lua"), separator=";"
        )
        env.prepend_path(
            "LUA_CPATH", os.path.join(self.spec.prefix, self.lua_lib_dir, "?.so"), separator=";"
        )

        env.prepend_path("FLUX_MODULE_PATH", self.prefix.lib.flux.modules)
        env.prepend_path("FLUX_MODULE_PATH", self.prefix.lib.flux.modules.sched)
        # On some systems modules are in lib64 and lib
        env.prepend_path("FLUX_MODULE_PATH", self.prefix.lib64.flux.modules)
        env.prepend_path("FLUX_MODULE_PATH", self.prefix.lib64.flux.modules.sched)
        env.prepend_path("FLUX_EXEC_PATH", self.prefix.libexec.flux.cmd)
        env.prepend_path("FLUX_RC_EXTRA", self.prefix.etc.flux)


class CMakeBuilder(CMakeBuilder):
    def cmake_args(self):
        args = []
        ver_in_src = os.path.exists(os.path.join(self.stage.source_path, "flux-sched.ver"))
        # flux-sched before v0.33 does not correctly set the version even when the file is present.
        if self.spec.satisfies("@:0.33") or not ver_in_src:
            # ref_version only exists on git versions
            try:
                ver = self.spec.version.ref_version
            except AttributeError:
                ver = self.spec.version
            args.append(self.define("FLUX_SCHED_VER", ver))
        args.append(self.define_from_variant("ENABLE_DOCS", "docs"))
        return args


class AutotoolsBuilder(AutotoolsBuilder):
    def configure_args(self):
        args = []
        if self.spec.satisfies("@0.9.0:"):
            args.append("CXXFLAGS=-Wno-uninitialized")
        if self.spec.satisfies("%clang@12:"):
            args.append("CXXFLAGS=-Wno-defaulted-function-deleted")
        if self.spec.satisfies("%oneapi"):
            args.append("CXXFLAGS=-Wno-tautological-constant-compare")
        # flux-sched's ax_boost is sometimes weird about non-system locations
        # explicitly setting the path guarantees success
        args.append("--with-boost={0}".format(self.spec["boost"].prefix))
        return args
