# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Bcftools(AutotoolsPackage):
    """BCFtools is a set of utilities that manipulate variant calls in the
    Variant Call Format (VCF) and its binary counterpart BCF. All
    commands work transparently with both VCFs and BCFs, both
    uncompressed and BGZF-compressed."""

    maintainers("jbeal-work")

    homepage = "https://samtools.github.io/bcftools/"
    url = "https://github.com/samtools/bcftools/releases/download/1.3.1/bcftools-1.3.1.tar.bz2"

    license("GPL-3.0-or-later")

    version("1.19", sha256="782b5f1bc690415192231e82213b3493b047f45e630dc8ef6f154d6126ab3e68")
    version("1.18", sha256="d9b9d36293e4cc62ab7473aa2539389d4e1de79b1a927d483f6e91f3c3ceac7e")
    version("1.17", sha256="01f75d8e701d85b2c759172412009cc04f29b61616ace2fa75116123de4596cc")
    version("1.16", sha256="293010736b076cf684d2873928924fcc3d2c231a091084c2ac23a8045c7df982")
    version("1.15.1", sha256="f21f9564873eb27ccf22d13b91a64acb8fbbfe4f9e4c37933a54b9a95857f2d7")
    version("1.14", sha256="b7ef88ae89fcb55658c5bea2e8cb8e756b055e13860036d6be13756782aa19cb")
    version("1.13", sha256="13bfa1da2a5edda8fa51196a47a0b4afb3fef17516451e4f0e78477f3dd30b90")
    version("1.12", sha256="7a0e6532b1495b9254e38c6698d955e5176c1ee08b760dfea2235ee161a024f5")
    version("1.10.2", sha256="f57301869d0055ce3b8e26d8ad880c0c1989bf25eaec8ea5db99b60e31354e2c")
    version("1.9", sha256="6f36d0e6f16ec4acf88649fb1565d443acf0ba40f25a9afd87f14d14d13070c8")
    version("1.8", sha256="4acbfd691f137742e0be63d09f516434f0faf617a5c60f466140e0677915fced")
    version("1.7", sha256="dd4f63d91b0dffb0f0ce88ac75c2387251930c8063f7799611265083f8d302d1")
    version("1.6", sha256="293010736b076cf684d2873928924fcc3d2c231a091084c2ac23a8045c7df982")
    version("1.4", sha256="8fb1b0a47ed4e1f9d7c70129d7993aa650da1688fd931b10646d1c4707ae234d")
    version("1.3.1", sha256="12c37a4054cbf1980223e2b3a80a7fdb3fd850324a4ba6832e38fdba91f1b924")
    version("1.2", sha256="53c628339020dd45334a007c9cefdaf1cba3f1032492ec813b116379fa684fd6")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "libgsl",
        default=False,
        description="build options that require the GNU scientific " "library",
    )

    variant(
        "perl-filters",
        default=False,
        description="build in support for PERL scripts in -i/-e "
        "filtering expressions, for versions >= 1.8.",
    )

    depends_on("gsl", when="+libgsl")
    depends_on("py-matplotlib", when="@1.6:", type="run")
    depends_on("py-gffutils", when="@1.9:", type="run")
    depends_on("perl", when="@1.8:~perl-filters", type="run")
    depends_on("perl", when="@1.8:+perl-filters", type=("build", "run"))

    depends_on("htslib@1.19", when="@1.19")
    depends_on("htslib@1.18", when="@1.18")
    depends_on("htslib@1.17", when="@1.17")
    depends_on("htslib@1.16", when="@1.16")
    depends_on("htslib@1.15", when="@1.15")
    depends_on("htslib@1.14", when="@1.14")
    depends_on("htslib@1.13", when="@1.13")
    depends_on("htslib@1.12", when="@1.12")
    depends_on("htslib@1.10.2", when="@1.10.2")
    depends_on("htslib@1.9", when="@1.9")
    depends_on("htslib@1.8", when="@1.8")
    depends_on("htslib@1.7", when="@1.7")
    depends_on("htslib@1.6", when="@1.6")
    depends_on("htslib@1.4", when="@1.4")
    depends_on("htslib@1.3.1", when="@1.3.1")
    depends_on("htslib@1.2", when="@1.2")

    patch("makefile_12.patch", when="@1.2")
    patch("fix_mk.patch", when="@1.2")
    patch("makefile_13.patch", when="@1.3")
    patch("makefile_14.patch", when="@1.4")
    patch("guess-ploidy.py_2to3.patch", when="@1.6:1.9")

    @when("@1.5:")
    def configure_args(self):
        args = []

        args.append("--with-htslib={0}".format(self.spec["htslib"].prefix))
        args.extend(self.enable_or_disable("libgsl"))

        if self.spec.satisfies("@1.8:"):
            args.extend(self.enable_or_disable("perl-filters"))

        return args

    @when("@1.2:1.4")
    def set_make_options(self):
        options = []

        options.append("prefix={0}".format(self.prefix))
        options.append("HTSDIR={0}".format(self.spec["htslib"].prefix))

        if self.spec.satisfies("+libgsl"):
            options.append("USE_GPL=1")

        return options

    @when("@1.2:1.4")
    def autoreconf(self, spec, prefix):
        touch("configure")

    @when("@1.2:1.4")
    def configure(self, spec, prefix):
        pass

    @when("@1.2:1.4")
    def build(self, spec, prefix):
        make_options = self.set_make_options()
        make(*make_options)

    @when("@1.2:1.4")
    def install(self, spec, prefix):
        make_options = self.set_make_options()
        make("install", *make_options)

        if spec.satisfies("@1.2"):
            mkdirp(self.prefix.libexec.bcftools)
            install("plugins/*.so", self.prefix.libexec.bcftools)

    @when("@1.2")
    def setup_run_environment(self, env):
        env.set("BCFTOOLS_PLUGINS", self.prefix.libexec.bcftools)
