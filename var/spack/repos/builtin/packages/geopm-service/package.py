# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class GeopmService(AutotoolsPackage):
    """The Global Extensible Open Power Manager (GEOPM) Service provides a
    user interface for accessing hardware telemetry and settings securely.

    Note: GEOPM interfaces with hardware using Model Specific Registers (MSRs).
    For proper usage make sure MSRs are made available via the msr or
    msr-safe kernel modules by your administrator."""

    homepage = "https://geopm.github.io"
    git = "https://github.com/geopm/geopm.git"
    url = "https://github.com/geopm/geopm/tarball/v3.1.0"

    maintainers("bgeltz", "cmcantalupo")
    license("BSD-3-Clause")
    tags = ["e4s"]

    version("develop", branch="dev", get_full_repo=True)
    version("3.1.0", sha256="2d890cad906fd2008dc57f4e06537695d4a027e1dc1ed92feed4d81bb1a1449e")
    version("3.0.1", sha256="32ba1948de58815ee055470dcdea64593d1113a6cad70ce00ab0286c127f8234")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("debug", default=False, description="Enable debug")
    variant("docs", default=True, when="@3.0.1", description="Create man pages with Sphinx")
    variant("systemd", default=True, description="Enable use of systemd/DBus")
    variant("liburing", default=True, description="Enables the use of liburing for batch I/O")
    variant(
        "libcap", default=True, description="Enables the use of libcap to do capabilities checks"
    )
    variant("gnu-ld", default=False, description="Assume C compiler uses gnu-ld")

    variant("levelzero", default=False, description="Enables the use of oneAPI Level Zero loader")
    variant("nvml", default=False, description="Enable NVML support")

    variant(
        "rawmsr",
        default=True,
        description="Enable direct use of standard msr device driver",
        when="@develop",
    )

    conflicts("+nvml", when="+levelzero", msg="LevelZero and NVML support are mutually exclusive")

    conflicts("%gcc@:7.2", msg="Requires C++17 support")
    conflicts("%clang@:4", msg="Requires C++17 support")

    conflicts("platform=darwin", msg="Darwin is not supported")
    conflicts("platform=windows", msg="Windows is not supported")

    conflicts("target=aarch64:", msg="Only available on x86_64", when="@3.0.1")
    conflicts("target=ppc64:", msg="Only available on x86_64", when="@3.0.1")
    conflicts("target=ppc64le:", msg="Only available on x86_64", when="@3.0.1")

    patch("0001-Support-NVML-via-CUDA-installation.patch", when="+nvml")

    # Autotools dependencies
    depends_on("automake", type="build")
    depends_on("autoconf", type="build")
    depends_on("libtool", type="build")
    depends_on("file")

    with when("@3.0.1"):
        # Docs dependencies
        #   Moved to python3-geopm-doc as of v3.1
        depends_on("doxygen", type="build", when="+docs")
        depends_on("py-docstring-parser@0.13.0:", type="build", when="+docs")
        depends_on("py-sphinx", type="build", when="+docs")
        depends_on("py-sphinx-rtd-theme@1:", type="build", when="+docs")
        depends_on("py-sphinxemoji@0.2.0:", type="build", when="+docs")
        depends_on("py-sphinx-tabs@3.3.1:", type="build", when="+docs")
        depends_on("py-pygments@2.13.0:", type="build", when="+docs")

        # Other Python dependencies - from service/setup.py
        #   Moved to python3-geopmdpy as of v3.1
        depends_on("py-setuptools@53.0.0:", type="build")
        depends_on("py-dasbus@1.6.0:", type=("build", "run"))
        depends_on("py-psutil@5.8.0:", type=("build", "run"))
        depends_on("py-jsonschema@3.2.0:", type=("build", "run"))
        depends_on("py-pyyaml@6.0:", type=("build", "run"))
        depends_on("py-cffi@1.14.5:", type="run")

    # Other dependencies
    for ver in ["3.1.0", "develop"]:
        depends_on(f"py-geopmdpy@{ver}", type="run", when=f"@{ver}")
    depends_on("py-setuptools-scm@7.0.3:", when="@3.1:", type="build")
    depends_on("bash-completion")
    depends_on("unzip")
    depends_on("systemd", when="+systemd")
    depends_on("libcap", when="+libcap")
    depends_on("liburing", when="+liburing")
    depends_on("oneapi-level-zero", when="+levelzero")
    depends_on("cuda", when="+nvml")

    extends("python")

    @property
    def configure_directory(self):
        if self.version == Version("3.0.1"):
            return "service"
        else:
            return "libgeopmd"

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        with working_dir(self.configure_directory):
            if not spec.version.isdevelop():
                if self.version == Version("3.0.1"):
                    version_file = "VERSION_OVERRIDE"
                else:
                    version_file = "VERSION"
                # Required to workaround missing VERSION files
                # from GitHub generated source tarballs
                with open(version_file, "w") as fd:
                    fd.write(f"{spec.version}")
            bash("./autogen.sh")

    def configure_args(self):
        args = [
            "--with-bash-completion-dir="
            + join_path(self.spec.prefix, "share", "bash-completion", "completions")
        ]

        args += self.enable_or_disable("debug")
        args += self.enable_or_disable("docs")
        args += self.enable_or_disable("systemd")
        args += self.enable_or_disable("liburing")
        args += self.with_or_without("liburing", activation_value="prefix")
        args += self.enable_or_disable("libcap")
        args += self.with_or_without("gnu-ld")

        args += self.enable_or_disable("levelzero")
        args += self.enable_or_disable("nvml")
        if self.spec.satisfies("+nvml"):
            args += [
                "--with-nvml="
                + join_path(
                    self.spec["cuda"].prefix, "targets", f"{self.spec.target.family}-linux"
                )
            ]

        args += self.enable_or_disable("rawmsr")
        with when("@develop"):
            if self.spec.target.family != "x86_64":
                args += ["--disable-cpuid"]
        return args

    def setup_run_environment(self, env):
        # Required to ensure geopmdpy can load
        # libgeopmd.so.2 via CFFI
        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib
        env.prepend_path("LD_LIBRARY_PATH", lib_dir)
