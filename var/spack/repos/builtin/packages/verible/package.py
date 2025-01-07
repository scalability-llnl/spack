# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Verible(Package):
    """The Verible project’s main mission is to parse SystemVerilog
    (IEEE 1800-2017) (as standardized in the [SV-LRM]) for a wide variety of
    applications, including developer tools.

    It was born out of a need to parse un-preprocessed source files, which is
    suitable for single-file applications like style-linting and formatting.
    In doing so, it can be adapted to parse preprocessed source files, which
    is what real compilers and toolchains require.

    The spirit of the project is that no-one should ever have to develop a
    SystemVerilog parser for their own application, because developing a
    standard-compliant parser is an enormous task due to the syntactic
    complexity of the language. Verible’s parser is also regularly tested
    against an ever-growing suite of (tool-independent) language compliance
    tests at https://symbiflow.github.io/sv-tests/.

    A lesser (but notable) objective is that the language-agnostic components
    of Verible be usable for rapidly developing language support tools for
    other languages."""

    homepage = "https://chipsalliance.github.io/verible"
    git = "https://github.com/chipsalliance/verible.git"

    license("BSD-3-Clause")

    version("master", branch="master")

    version(
        "0.0.3876",
        sha256="42b933b52cf394fa2cfcb841edb6cf3649f5453bf43178f8f630fc3e626f3e03",
        url="https://github.com/chipsalliance/verible/archive/refs/tags/v0.0-3876-g2f99cdc9.tar.gz",
    )
    version(
        "0.0.3864",
        sha256="aa67a8f3f76828779d61ce35fedee0a9020a03214385c76abb18a7d4dabef081",
        url="https://github.com/chipsalliance/verible/archive/refs/tags/v0.0-3864-g3d821c62.tar.gz",
    )
    version(
        "0.0.3841",
        sha256="fbc9cb32aa8a64ba60f24dc89e8573c8ea62c45d76113a0f2ab5b73babed5990",
        url="https://github.com/chipsalliance/verible/archive/refs/tags/v0.0-3841-g5eb8aa34.tar.gz",
    )
    version(
        "0.0.3836",
        sha256="946625a1527d0a97772ea031ab7358af29e61258c189a2ab0d9533b43e71f35b",
        url="https://github.com/chipsalliance/verible/archive/refs/tags/v0.0-3836-g86ee9bab.tar.gz",
    )
    version(
        "0.0.3671",
        sha256="9f492cdc64b047f4e91aece8aa01fd2b846d9695510360dde34980daf5dbe0dd",
        url="https://github.com/chipsalliance/verible/archive/refs/tags/v0.0-3671-gf2731544.tar.gz",
    )
    version(
        "0.0.3667",
        sha256="6a13a902bfd37ecabfd772d619251da40e8ad8e44cf75ec2bc8663046200b02a",
        url="https://github.com/chipsalliance/verible/archive/refs/tags/v0.0-3667-g88d12889.tar.gz",
    )
    version(
        "0.0.3624",
        sha256="e5995644e092e72c9d37c492f319b0d4861a3c63d03d1c3cfefe2363bcd6b74f",
        url="https://github.com/chipsalliance/verible/archive/refs/tags/v0.0-3624-gd256d779.tar.gz",
    )
    version(
        "0.0.3607",
        sha256="5ea427ed843916f8c1b5d7263c1aaad526dc7181de5afcf84542bca4c4f8f1ca",
        url="https://github.com/chipsalliance/verible/archive/refs/tags/v0.0-3607-g46de0f64.tar.gz",
    )
    version(
        "0.0.3539",
        sha256="e93c9638dac7d314cea506d483b0f078b80aa6837afa74db68ace322b0dbba31",
        url="https://github.com/chipsalliance/verible/archive/refs/tags/v0.0-3539-g9442853c.tar.gz",
    )
    version(
        "0.0.3483",
        sha256="c40591813a7cf6b1a6f46f7e02d81526c999966c3ceb9a67c5542234cf49dddb",
        url="https://github.com/chipsalliance/verible/archive/refs/tags/v0.0-3483-ga4d61b11.tar.gz",
    )
    version(
        "0.0.3430",
        sha256="580ab39c82da9f67523658c0bb0859e2b6c662f7c06855859f476eeedd92a7e0",
        url="https://github.com/chipsalliance/verible/archive/refs/tags/v0.0-3430-g060bde0f.tar.gz",
    )
    version(
        "0.0.3428",
        sha256="2b83497662b890f875bfe859175aa8e4b87db6e6a177ad08a0694002b8767cb0",
        url="https://github.com/chipsalliance/verible/archive/refs/tags/v0.0-3428-gcfcbb82b.tar.gz",
    )

    depends_on("cxx", type="build")  # generated

    maintainers("davekeeshan")

    depends_on("flex", type="build")
    depends_on("bison", type="build")
    depends_on("bazel", type="build")

    conflicts("%gcc@:8", msg="Only works with gcc9 and above")

    @when("@:0.0.3841")
    def install(self, spec, prefix):
        bazel("build", "-c", "opt", "//...")
        bazel("run", "-c", "opt", ":install", "--", prefix.bin)

    @when("@0.0.3841:")
    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        bash = which("bash")
        bazel("build", "-c", "opt", ":install-binaries")
        bash(".github/bin/simple-install.sh", prefix.bin)
