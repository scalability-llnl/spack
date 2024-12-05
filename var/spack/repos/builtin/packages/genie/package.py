# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack.package import *
from spack.version import Version


class Genie(Package):
    """Genie is a neutrino Monte Carlo Generator."""

    homepage = "https://www.genie-mc.org"
    url = "https://github.com/GENIE-MC/Generator/archive/R-3_00_06.tar.gz"
    git = "https://github.com/GENIE-MC/Generator.git"

    tags = ["neutrino", "hep"]

    maintainers("davehadley")

    version("master", branch="master")
    version("3.4.2", sha256="c5935aea86d2ba9897ab55bb581622c561575957d19e572691d3bc0833ed9512")
    version("3.0.6", sha256="ab56ea85d0c1d09029254365bfe75a1427effa717389753b9e0c1b6c2eaa5eaf")
    version("3.0.4", sha256="53f034618fef9f7f0e17d1c4ed72743e4bba590e824b795177a1a8a8486c861e")
    version("3.0.2", sha256="34d6c37017b2387c781aea7bc727a0aac0ef45d6b3f3982cc6f3fc82493f65c3")
    version("3.0.0", sha256="3953c7d9f1f832dd32dfbc0b9260be59431206c204aec6ab0aa68c01176f2ae6")
    version("2.12.10", sha256="c8762db3dcc490f80f8a61268f5b964d4d35b80134b622e89fe2307a836f2a0b")
    version("2.12.8", sha256="7ca169a8d9eda7267d28b76b2f3110552852f8eeae263a03cd5139caacebb4ea")
    version("2.12.6", sha256="3b450c609875459798ec98e12cf671cc971cbb13345af6d75bd6278d422f3309")
    version("2.12.4", sha256="19a4a1633b0847a9f16a44e0c74b9c224ca3bb93975aecf108603c22e807517b")
    version("2.12.2", sha256="cbdc45a739878940dadcaaed575b5cad6b5e7035f29605045b1ca557e6faa6d1")
    version("2.12.0", sha256="d2b01c80f38d269cb0296b3f2932798ef3f1d51bd130e81274fbfeeb381fac6b")
    version("2.11.2", sha256="0f4c25d8ceb7513553671643c9cdac5aa98c40fc8594a5ecb25c077c6b36166e")
    version("2.11.0", sha256="1ebe0eb65d797595413632f1cec1cb2621cb8e8d0384a2843799724a79b1d80c")
    version("2.10.10", sha256="1dfaadcf1bbaf6e164b612f410c4399301e63497ad6a4891706b1787ac11a7a1")
    version("2.10.8", sha256="4f6f5af2062e7c505b76e70547ac2ae304a9790c3e9b9592818d8aebeebc8398")
    version("2.10.6", sha256="d00b4288c886f81459fb2967e539f30315d4385f82d1d3f4330298d313f9a176")
    version("2.10.4", sha256="df909bf7e1a789ca01794995687da2af803769f0823273a4a3a31678d6d5b0f1")
    version("2.10.2", sha256="6abe4e0cdb5e8f5beddf0ccdbebc94c175a9f72592b1cbbffe01b88ee3972bf9")
    version("2.10.0", sha256="17bda900c996b6f4f10a7f6a3be94e56c3b8dcdeb2ef8865ca7f20c5fe725291")
    version("2.9.0", sha256="8229beb73f65f5af86a77bf141acfbe4a8b68cba9d797aae083a929906f6f2a2")
    version("2.8.6", sha256="310dc8e0d17a65e6b9773e398250703a3a6f94ceafe94f599ae0f7b3fecf7e6c")

    depends_on("cxx", type="build")  # generated

    depends_on("root+pythia6")
    depends_on("pythia6")
    depends_on("lhapdf", when="@3:")
    depends_on("lhapdf5", when="@:2")
    depends_on("log4cpp")
    depends_on("libxml2")
    depends_on("gsl")

    # GENIE does not actually require cmake, but root does.
    # Spack's concretizer fails with "unsatisfiable constraint" if we don't add this.
    depends_on("cmake@3:")

    # GENIE Makefile's think that the spack compiler is invalid.
    # Disables this check.
    patch("genie_disable_gopt_with_compiler_check.patch", level=0, when="@2.11:")
    patch(
        "https://patch-diff.githubusercontent.com/raw/GENIE-MC/Generator/pull/376.patch?full_index=1",
        sha256="7eca9bf44251cd99edd962483ca24c5072f8e2eee688f1e95b076425f2dc59f6",
        when="@3.4.2",
    )
    # Flags for GENIE"s optional but disabled by default features
    variant(
        "atmo", default=False, description="Enable GENIE Atmospheric neutrino event generation app"
    )
    variant(
        "fnal", default=False, description="Enables FNAL experiment-specific event generation app"
    )
    variant(
        "nucleondecay",
        default=False,
        description="Enable GENIE Nucleon decay event generation app",
    )
    variant("masterclass", default=False, description="Enable GENIE neutrino masterclass app")
    variant("t2k", default=False, description="Enable T2K-specific generation app")
    variant(
        "vleextension",
        default=False,
        description="Enable GENIE very low energy (1 MeV - 100 MeV) extension",
    )

    def url_for_version(self, version):
        url = "https://github.com/GENIE-MC/Generator/archive/R-{0}.tar.gz"
        if version >= Version("3"):
            return url.format("{0}_{1:02d}_{2:02d}".format(*version))
        else:
            return url.format(version.underscored)

    def setup_build_environment(self, env):
        env.set("GENIE", self.stage.source_path)

    def setup_run_environment(self, env):
        env.set("GENIE", self.prefix)

    def install(self, spec, prefix):
        configure = Executable("./configure")
        args = self._configure_args(spec, prefix)
        configure(*args)
        self._make(parallel=spec.satisfies("@3:"))
        # GENIE make install does not support parallel jobs
        self._make("install", parallel=False)
        # GENIE requires these files to be present at runtime, but doesn"t install them
        # so we must install them ourselves
        # install_tree function is injected into scope by spack build_environment.py
        install_tree("config", os.sep.join((prefix, "config")))
        install_tree("data", os.sep.join((prefix, "data")))

    def _configure_args(self, spec, prefix):
        args = [
            "--prefix=" + prefix,
            "--with-compiler=" + os.environ["CC"],
            "--with-libxml2-inc={0}{1}libxml2".format(spec["libxml2"].prefix.include, os.sep),
            "--with-libxml2-lib=" + spec["libxml2"].prefix.lib,
            "--with-log4cpp-inc=" + spec["log4cpp"].prefix.include,
            "--with-log4cpp-lib=" + spec["log4cpp"].prefix.lib,
            "--with-pythia6-lib=" + spec["pythia6"].prefix.lib,
        ]
        if self.spec.satisfies("@:2"):
            args += [
                "--enable-lhapdf",
                "--with-lhapdf-inc=" + spec["lhapdf5"].prefix.include,
                "--with-lhapdf-lib=" + spec["lhapdf5"].prefix.lib,
                # must be enabled or some GENIE 2 versions fail to link
                # this option was removed in GENIE 3
                "--enable-rwght",
            ]
        else:
            args += [
                "--enable-lhapdf6",
                "--with-lhapdf6-inc=" + spec["lhapdf"].prefix.include,
                "--with-lhapdf6-lib=" + spec["lhapdf"].prefix.lib,
            ]
        if self.spec.satisfies("+vleextension"):
            args += ["--enable-vle-extension"]
        if self.spec.satisfies("+t2k"):
            args += ["--enable-t2k"]
        if self.spec.satisfies("+fnal"):
            args += ["--enable-fnal"]
        if self.spec.satisfies("+atmo"):
            args += ["--enable-atmo"]
        if self.spec.satisfies("+nucleondecay"):
            args += ["--enable-nucleon-decay"]
        if self.spec.satisfies("+masterclass"):
            args += ["--enable-masterclass"]
        return args

    def _make(self, *args, **kwargs):
        parallel = kwargs.get("parallel", False)
        args = list(self._make_args) + list(args)
        # make function is injected into scope by spack build_environment.py
        make(*args, parallel=parallel)

    @property
    def _make_args(self):
        return ["CC=c++", "CXX=c++", "LD=c++"]
