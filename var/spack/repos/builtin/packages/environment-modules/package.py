# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class EnvironmentModules(Package):
    """The Environment Modules package provides for the dynamic
    modification of a user's environment via module files.
    """

    homepage = "https://cea-hpc.github.io/modules/"
    url = "https://github.com/cea-hpc/modules/releases/download/v5.4.0/modules-5.4.0.tar.gz"
    git = "https://github.com/cea-hpc/modules.git"

    maintainers("xdelaruelle")

    version("main", branch="main")
    version("5.4.0", sha256="586245cbf9420866078d8c28fce8ef4f192530c69a0f368f51e848340dcf3b90")
    version("5.3.1", sha256="d02f9ce4f8baf6c99edceb7c73bfdd1e97d77bcc4725810b86efed9f58dda962")
    version("5.3.0", sha256="21b8daa0181044ef65097a1e3517af1f24e7c7343cc5bdaf70be11e3cb0edb51")
    version("5.2.0", sha256="48f9f10864303df628a48cab17074820a6251ad8cd7d66dd62aa7798af479254")
    version("5.1.1", sha256="1985f79e0337f63d6564b08db0238cf96a276a4184def822bb8ad37996dc8295")
    version("5.1.0", sha256="1ab1e859b9c8bca8a8d332945366567fae4cf8dd7e312a689daaff46e7ffa949")
    version("5.0.1", sha256="33a598eaff0713de09e479c2636ecde188b982584e56377f234e5065a61be7ba")
    version("5.0.0", sha256="428e23ac51a6006605de65ed9114d544a5506cb4b6bfb03d8522778f13e4f7ea")
    version("4.8.0", sha256="d6b45cadc2146ed5e0b25a96d44643ad516054eb7745acb14a1dc7bf30744f6e")
    version("4.7.1", sha256="ee7ecd62bbbde6d51e30788a97800c39e72515b6a910839fb84041b35ba42b4d")
    version("4.7.0", sha256="3ab0a649e23b4dd00963e4cae60e573b449194ecb4035c5ce487330b272b4d06")
    version("4.6.1", sha256="3445df39abe5838b94552b53e7dbff56ada8347b9fdc6c04a72297d5b04af76f")
    version("4.6.0", sha256="b42b14bb696bf1075ade1ecaefe7735dbe411db4c29031a1dae549435eafa946")
    version("4.5.3", sha256="7cbd9c61e6dcd82a3f81b5ced92c3cf84ecc5489639bdfc94869256383a2c915")
    version("4.5.2", sha256="74ccc9ab0fea0064ff3f4c5841435cef13cc6d9869b3c2b25e5ca4efa64a69a1")
    version("4.5.1", sha256="7d4bcc8559e7fbbc52e526fc86a15b161ff4422aa49eee37897ee7a48eb64ac2")
    version("4.5.0", sha256="5f46336f612553af5553d99347f387f733de0aaa0d80d4572e67615289382ec8")
    version("4.4.1", sha256="3c20cfb2ff8a4d74ac6d566e7b5fa9dd220d96d17e6d8a4ae29b1ec0107ee407")
    version("4.4.0", sha256="4dd55ad6cc684905e891ad1ba9e3c542e79eea0a9cd9a0e99cd77abe6ed63fab")
    version("4.3.1", sha256="979efb5b3d3c8df2c3c364aaba61f97a459456fc5bbc092dfc02677da63e5654")
    version("4.3.0", sha256="231f059c4109a2d3028c771f483f6c92f1f3689eb0033648ce00060dad00e103")
    version("4.2.5", sha256="3375b454568e7bbec7748cd6173516ef9f30a3d8e13c3e99c02794a6a3bc3c8c")
    version("4.2.4", sha256="416dda94141e4778356e2aa9ba8687e6522a1eb197b3caf00a82e5fa2707709a")
    version("4.2.3", sha256="f667134cca8e2c75e12a00b50b5605d0d8068efa5b821f5b3c3f0df06fd79411")
    version("4.2.2", sha256="481fe8d03eec6806c1b401d764536edc2c233ac9d82091a10094de6101867afc")
    version("4.2.1", sha256="c796ea6a03e22d63886ca9ec6b1bef821e8cb09f186bd007f63653e31e9cb595")
    version("4.2.0", sha256="d439dfa579a633108c4f06574ed9bc3b91b8610d2ce3a6eb803bf377d0284be7")
    version("4.1.4", sha256="965b6056ea6b72b87d9352d4c1db1d7a7f9f358b9408df2689d823b932d6aa7f")
    version("4.1.3", sha256="dab82c5bc20ccea284b042d6af4bd6eaba95f4eaadd495a75413115d33a3151f")
    version("4.1.2", sha256="d1f54f639d1946aa1d7ae8ae03752f8ac464a879c14bc35e63b6a87b8a0b7522")
    version("4.1.1", sha256="998e9cc936045b4e84f28ca60c4680c08385a210d6bb95fc31c28a7d634a9357")
    version("4.1.0", sha256="d98aa369219bf0a4ec41efe7cb8d1127d34cb07666088dd79da6b424196d4cfd")
    version("4.0.0", sha256="f0ab7f6a747863cb980681a904a3c9380e2e52de6eb046cfa285e5e225f9ac47")
    version(
        "3.2.10",
        sha256="fb05c82a83477805a1d97737a9f0ca0db23f69b7bce504f1609ba99477b03955",
        url="http://prdownloads.sourceforge.net/modules/modules-3.2.10.tar.gz",
    )

    depends_on("c", type="build")  # generated

    variant("X", default=True, description="Build with X functionality")

    depends_on("less", type=("build", "run"), when="@4.1:")
    with when("@main"):
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("libtool", type="build")
        depends_on("m4", type="build")
        depends_on("python", type="build")
        depends_on("py-sphinx@1.0:", type="build")
        depends_on("gzip", type="build")

    # Dependencies:
    depends_on("tcl", type=("build", "link", "run"))
    depends_on("tcl@8.4:", type=("build", "link", "run"), when="@4.0.0:4.8")
    depends_on("tcl@8.5:", type=("build", "link", "run"), when="@5.0.0:")

    def install(self, spec, prefix):
        tcl = spec["tcl"]

        config_args = [
            "--prefix=" + prefix,
            # It looks for tclConfig.sh
            "--with-tcl=" + tcl.libs.directories[0],
            "--datarootdir=" + prefix.share,
        ]

        # ./configure script on version 4.5.2 breaks when specific options are
        # set (see https://github.com/cea-hpc/modules/issues/354)
        if not spec.satisfies("@4.5.2"):
            config_args.extend(["--disable-dependency-tracking", "--disable-silent-rules"])

        if spec.satisfies("~X"):
            config_args = ["--without-x"] + config_args

        if self.spec.satisfies("@4.4.0:4.8"):
            config_args.extend(
                [
                    "--with-icase=search",
                    "--enable-extended-default",
                    "--enable-advanced-version-spec",
                ]
            )

        if self.spec.satisfies("@4.3.0:4.8"):
            config_args.extend(["--enable-color"])

        if self.spec.satisfies("@4.2.0:4.8"):
            config_args.extend(["--enable-auto-handling"])

        if self.spec.satisfies("@4.1.0:"):
            config_args.extend(
                [
                    # Variables in quarantine are empty during module command
                    # start-up and they will be restored to the value they had
                    # in the environment once the command starts
                    "--with-quarantine-vars=LD_LIBRARY_PATH LD_PRELOAD"
                ]
            )

        if self.spec.satisfies("@4.0.0:4.8"):
            config_args.extend(["--disable-compat-version"])

        if self.spec.satisfies("@4.0.0:"):
            config_args.extend(["--with-tclsh={0}".format(tcl.prefix.bin.tclsh)])

        if self.spec.satisfies("@3.2.10"):
            # See: https://sourceforge.net/p/modules/bugs/62/
            config_args.extend(["--disable-debug", "CPPFLAGS=-DUSE_INTERP_ERRORLINE"])

        if self.spec.satisfies("@:3.2"):
            config_args.extend(
                [
                    "--without-tclx",
                    "--with-tclx-ver=0.0",
                    "--with-tcl-ver={0}".format(tcl.version.up_to(2)),
                    "--disable-versioning",
                ]
            )

        if self.spec.satisfies("@4.1:"):
            config_args.append(f"--with-pager={str(self.spec['less'].prefix.bin.less)}")

        configure(*config_args)
        make()
        make("install")
