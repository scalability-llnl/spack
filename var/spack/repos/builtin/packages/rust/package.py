# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *


class Rust(Package):
    """The Rust programming language toolchain."""

    homepage = "https://www.rust-lang.org"
    url = "https://static.rust-lang.org/dist/rustc-1.42.0-src.tar.gz"
    git = "https://github.com/rust-lang/rust.git"

    maintainers("alecbcs")

    license("Apache-2.0 OR MIT")

    # When adding a version of Rust you may need to add an additional version
    # to rust-bootstrap as the minimum bootstrapping requirements increase.
    # As a general rule of thumb Rust can be built with either the previous major
    # version or the current version of the compiler as shown above.
    #
    # Pre-release versions.
    # Note: If you plan to use these versions remember to install with
    # `-n` to prevent Spack from failing due to failed checksums.
    #
    #     $ spack install -n rust@pre-release-version
    #
    version("beta")
    version("master", branch="master", submodules=True)
    version("nightly")

    # Stable versions.
    version("1.81.0", sha256="872448febdff32e50c3c90a7e15f9bb2db131d13c588fe9071b0ed88837ccfa7")
    version("1.78.0", sha256="ff544823a5cb27f2738128577f1e7e00ee8f4c83f2a348781ae4fc355e91d5a9")
    version("1.76.0", sha256="9e5cff033a7f0d2266818982ad90e4d3e4ef8f8ee1715776c6e25073a136c021")
    version("1.75.0", sha256="5b739f45bc9d341e2d1c570d65d2375591e22c2d23ef5b8a37711a0386abc088")
    version("1.74.0", sha256="882b584bc321c5dcfe77cdaa69f277906b936255ef7808fcd5c7492925cf1049")
    version("1.73.0", sha256="96d62e6d1f2d21df7ac8acb3b9882411f9e7c7036173f7f2ede9e1f1f6b1bb3a")
    version("1.70.0", sha256="b2bfae000b7a5040e4ec4bbc50a09f21548190cb7570b0ed77358368413bd27c")
    version("1.65.0", sha256="5828bb67f677eabf8c384020582b0ce7af884e1c84389484f7f8d00dd82c0038")
    version("1.60.0", sha256="20ca826d1cf674daf8e22c4f8c4b9743af07973211c839b85839742314c838b7")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant(
        "dev",
        default=False,
        description="Include rust developer tools like rustfmt, clippy, and rust-analyzer.",
    )
    variant("docs", default=False, description="Build Rust core documentation.")
    variant("src", default=True, description="Include standard library source files.")

    # Core dependencies
    depends_on("curl+nghttp2")
    depends_on("libgit2")
    depends_on("libssh2")
    depends_on("ninja", type="build")
    depends_on("openssl")
    depends_on("pkgconfig", type="build")
    depends_on("python", type="build")
    depends_on("zlib-api")

    # cmake dependency comes from LLVM. Rust has their own fork of LLVM, with tags corresponding
    # to each Rust release, so it's easy to loop through tags and grep for "cmake_minimum_required"
    depends_on("cmake@3.4.3:", type="build", when="@:1.51")
    depends_on("cmake@3.13.4:", type="build", when="@1.52:1.72")
    depends_on("cmake@3.20.0:", type="build", when="@1.73:")

    # Compiling Rust requires a previous version of Rust.
    # The easiest way to bootstrap a Rust environment is to
    # download the binary distribution of the compiler and build with that.
    depends_on("rust-bootstrap", type="build")

    # Pre-release version dependencies
    depends_on("rust-bootstrap@beta", type="build", when="@beta")
    depends_on("rust-bootstrap@nightly", type="build", when="@master")
    depends_on("rust-bootstrap@nightly", type="build", when="@nightly")

    # Stable version dependencies
    depends_on("rust-bootstrap", type="build")
    depends_on("rust-bootstrap@1.59:1.60", type="build", when="@1.60")
    depends_on("rust-bootstrap@1.64:1.65", type="build", when="@1.65")
    depends_on("rust-bootstrap@1.69:1.70", type="build", when="@1.70")
    depends_on("rust-bootstrap@1.72:1.73", type="build", when="@1.73")
    depends_on("rust-bootstrap@1.73:1.74", type="build", when="@1.74")
    depends_on("rust-bootstrap@1.74:1.75", type="build", when="@1.75")
    depends_on("rust-bootstrap@1.77:1.78", type="build", when="@1.78")
    depends_on("rust-bootstrap@1.80:1.81", type="build", when="@1.81")

    # src/llvm-project/llvm/cmake/modules/CheckCompilerVersion.cmake
    conflicts("%gcc@:7.3", when="@1.73:", msg="Host GCC version must be at least 7.4")
    # https://github.com/rust-lang/llvm-project/commit/4d039a7a71899038b3bc6ed6fe5a8a48d915caa0
    conflicts("%gcc@13:", when="@:1.63", msg="Rust<1.64 not compatible with GCC>=13")
    conflicts("%intel", msg="Rust not compatible with Intel Classic compilers")
    conflicts("%oneapi", msg="Rust not compatible with Intel oneAPI compilers")

    extendable = True
    executables = ["^rustc$", "^cargo$"]

    phases = ["configure", "build", "install"]

    @classmethod
    def determine_spec_details(cls, prefix, exes_in_prefix):
        rustc_candidates = [x for x in exes_in_prefix if os.path.basename(x) == "rustc"]
        cargo_candidates = [x for x in exes_in_prefix if os.path.basename(x) == "cargo"]
        # Both rustc and cargo must be present
        if not (rustc_candidates and cargo_candidates):
            return
        output = Executable(rustc_candidates[0])("--version", output=str, error=str)
        match = re.match(r"rustc (\S+)", output)
        if match:
            version_str = match.group(1)
            return Spec.from_detection(f"rust@{version_str}", external_path=prefix)

    def setup_dependent_package(self, module, dependent_spec):
        module.cargo = Executable(os.path.join(self.spec.prefix.bin, "cargo"))

    def setup_build_environment(self, env):
        # Manually instruct Cargo dependency libssh2-sys to build with
        # the Spack installed libssh2 package. For more info see
        # https://github.com/alexcrichton/ssh2-rs/issues/173
        env.set("LIBSSH2_SYS_USE_PKG_CONFIG", "1")

        # Manually inject the path of ar for build.
        ar = which("ar", required=True)
        env.set("AR", ar.path)

        # Manually inject the path of openssl's certs for build
        # if certs are present on system via Spack or via external
        # openssl.
        def get_test_path(p):
            certs = join_path(p, "cert.pem")
            if os.path.exists(certs):
                return certs
            return None

        # find certs, don't set if no file is found in case
        # ca-certificates isn't installed
        certs = None
        openssl = self.spec["openssl"]
        if openssl.external:
            try:
                output = which("openssl", required=True)("version", "-d", output=str, error=str)
                openssl_dir = re.match('OPENSSLDIR: "([^"]+)"', output)
                if openssl_dir:
                    certs = get_test_path(openssl_dir.group(1))
            except ProcessError:
                pass

        if certs is None:
            certs = get_test_path(join_path(openssl.prefix, "etc/openssl"))

        if certs is not None:
            env.set("CARGO_HTTP_CAINFO", certs)

    def configure(self, spec, prefix):
        opts = []

        # Set prefix to install into spack prefix.
        opts.append(f"install.prefix={prefix}")

        # Set relative path to put system configuration files
        # under the Spack package prefix.
        opts.append("install.sysconfdir=etc")

        # Build extended suite of tools so dependent packages
        # packages can build using cargo.
        opts.append("build.extended=true")

        # Build docs if specified by the +docs variant.
        opts.append(f"build.docs={str(spec.satisfies('+docs')).lower()}")

        # Set binary locations for bootstrap rustc and cargo.
        opts.append(f"build.cargo={spec['rust-bootstrap'].prefix.bin.cargo}")
        opts.append(f"build.rustc={spec['rust-bootstrap'].prefix.bin.rustc}")

        # Disable bootstrap LLVM download.
        opts.append("llvm.download-ci-llvm=false")

        # Convert opts to '--set key=value' format.
        flags = [flag for opt in opts for flag in ("--set", opt)]

        # Core rust tools to install.
        tools = ["cargo"]

        # Add additional tools as directed by the package variants.
        if spec.satisfies("+dev"):
            tools.extend(["clippy", "rustdoc", "rustfmt", "rust-analyzer"])

        if spec.satisfies("+src"):
            tools.append("src")

        # Compile tools into flag for configure.
        flags.append(f"--tools={','.join(tools)}")

        # Use vendored resources to perform offline build.
        flags.append("--enable-vendor")

        configure(*flags)

    def build(self, spec, prefix):
        python("./x.py", "build")

    def install(self, spec, prefix):
        python("./x.py", "install")
