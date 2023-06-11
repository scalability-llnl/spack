# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Rust(Package):
    """The Rust programming language toolchain."""

    homepage = "https://www.rust-lang.org"
    url = "https://static.rust-lang.org/dist/rustc-1.42.0-src.tar.gz"
    git = "git://github.com/rust-lang/rust.git"

    maintainers("alecbcs", "AndrewGaspar")

    depends_on("cmake@3.13.4:", type="build")
    depends_on("curl+nghttp2")
    depends_on("libgit2")
    depends_on("ninja", type="build")
    depends_on("openssl")
    depends_on("pkgconfig", type="build")
    depends_on("python", type="build")

    # Compiling Rust requires a previous version of Rust. The
    # easiest way to bootstrap a Rust environment is to download the binary
    # distribution of the compiler and build with that.
    depends_on("rust-bootstrap", type="build")
    depends_on("rust-bootstrap@1.59:1.60", type="build", when="@1.60")
    depends_on("rust-bootstrap@1.64:1.65", type="build", when="@1.65")
    depends_on("rust-bootstrap@1.69:1.70", type="build", when="@1.70")

    # When adding a version of Rust you may need to add an additional
    # version to rust-bootstrap as the minimum bootstrapping requirements
    # increase. As a general rule of thumb Rust can be built with the previous
    # major version of the compiler or the current version of the compiler as
    # shown above.
    version("nightly")

    version("1.70.0", sha256="b2bfae000b7a5040e4ec4bbc50a09f21548190cb7570b0ed77358368413bd27c")
    version("1.65.0", sha256="5828bb67f677eabf8c384020582b0ce7af884e1c84389484f7f8d00dd82c0038")
    version("1.60.0", sha256="20ca826d1cf674daf8e22c4f8c4b9743af07973211c839b85839742314c838b7")

    variant(
        "analysis",
        default=False,
        description="Outputs code analysis that can be consumed by other tools",
    )
    variant(
        "clippy",
        default=True,
        description="A bunch of lints to catch common mistakes and improve your Rust code.",
    )
    variant("docs", default=False, description="Build Rust documentation.")
    variant("rustfmt", default=True, description="Formatting tool for Rust code.")
    variant("src", default=True, description="Include standard library source files.")

    extendable = True
    executables = ["^rustc$", "^cargo$"]

    phases = ["configure", "build", "install"]

    @classmethod
    def determine_version(csl, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.match(r"rustc (\S+)", output)
        return match.group(1) if match else None

    def setup_build_environment(self, env):
        ar = which("ar", required=True)
        env.set("AR", ar.path)

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

        # Convert opts to '--set key=value' format.
        flags = [flag for opt in opts for flag in ("--set", opt)]

        # Include both cargo and rustdoc in minimal install to match
        # standard download of rust.
        tools = ["cargo", "rustdoc"]

        # Add additional tools as directed by the package variants.
        if spec.satisfies("+analysis"):
            tools.append("analysis")

        if spec.satisfies("+clippy"):
            tools.append("clippy")

        if spec.satisfies("+src"):
            tools.append("src")

        if spec.satisfies("+rustfmt"):
            tools.append("rustfmt")

        # Compile tools into flag for configure.
        flags.append(f"--tools={','.join(tools)}")

        configure(*flags)

    def build(self, spec, prefix):
        python("./x.py", "build")

    def install(self, spec, prefix):
        python("./x.py", "install")
