# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Bazel(Package):
    """Bazel is an open-source build and test tool similar to Make, Maven, and
    Gradle. It uses a human-readable, high-level build language. Bazel supports
    projects in multiple languages and builds outputs for multiple platforms.
    Bazel supports large codebases across multiple repositories, and large
    numbers of users."""

    homepage = "https://bazel.build/"
    url = "https://github.com/bazelbuild/bazel/releases/download/3.1.0/bazel-3.1.0-dist.zip"

    maintainers("LydDeb")

    tags = ["build-tools"]

    license("Apache-2.0")

    version("7.0.2", sha256="dea2b90575d43ef3e41c402f64c2481844ecbf0b40f8548b75a204a4d504e035")
    version("7.0.1", sha256="596b13e071d27c43343ec8f5d263cb5312fafe7ef8702401f7ed492f182f4e6c")
    version("7.0.0", sha256="477e54f6374001f439a9471ba1de9d7824daf129db95510849ecc5e19ce88170")
    version("6.5.0", sha256="fc89da919415289f29e4ff18a5e01270ece9a6fe83cb60967218bac4a3bb3ed2")
    version("6.4.0", sha256="bd88ff602c8bbb29ee82ba2a6b12ad092d51ec668c6577f9628f18e48ff4e51e")
    version("6.3.2", sha256="8cd7feac58193be2bcba451ba6688a46824d37ca6359ff58e0d44eb98f042948")
    version("6.3.1", sha256="2676319e86c5aeab142dccd42434364a33aa330a091c13562b7de87a10e68775")
    version("6.3.0", sha256="902198981b1d26112fc05913e79f1b3e9772c3f95594caf85619d041ba06ede0")
    version("6.2.1", sha256="4cf4d264bff388ee0012735728630d23832d3c9d021383b2fadceadb0775dd6b")
    version("6.2.0", sha256="f1e8f788637ac574d471d619d2096baaca04a19b57a034399e079633db441945")
    version("6.1.2", sha256="6fb3ee22fe9fa86d82e173572d504c089f10825d749725592626e090b38c9679")
    version("6.1.1", sha256="6b900f26d676c7eca1d2e7dff9b71890dabd3ff59cab2a2d2178bc8a0395342a")
    version("6.1.0", sha256="c4b85675541cf66ee7cb71514097fdd6c5fc0e02527243617a4f20ca6b4f2932")
    version("6.0.0", sha256="7bc0c5145c19a56d82a08fce6908c5e1a0e75e4fbfb3b6f12b4deae7f4b38cbc")
    version("5.4.0", sha256="a1c62d9bcb4e03106ddf0b7bd96196ba246e1c9b7a935daf8d9beda8bbdcb8a1")
    version("5.3.2", sha256="3880ad919592d1e3e40c506f13b32cd0a2e26f129d87cb6ba170f1801d7d7b82")
    version("5.3.1", sha256="18486e7152ca26b26585e9b2a6f49f332b116310d3b7e5b70583f1f1f24bb8ae")
    version("5.3.0", sha256="ee801491ff0ec3a562422322a033c9afe8809b64199e4a94c7433d4e14e6b921")
    version("5.2.0", sha256="820a94dbb14071ed6d8c266cf0c080ecb265a5eea65307579489c4662c2d582a")
    version("5.1.1", sha256="7f5d3bc1d344692b2400f3765fd4b5c0b636eb4e7a8a7b17923095c7b56a4f78")
    version("5.1.0", sha256="4de301f509fc6d0cbc697b2017384ecdc94df8f36245bbcbedc7ea6780acc9f5")
    version("5.0.0", sha256="072dd62d237dbc11e0bac02e118d8c2db4d0ba3ba09f1a0eb1e2a460fb8419db")
    version("4.2.4", sha256="d5ba2ef28da5275f22e832aaa7f9319c61ea5db9b6a3e23b28a6a64ad03078f3")
    version("4.2.3", sha256="b0e84d0538f3ec2b95a49bae31a5066f0967281a3ca99965016fbe178acd2d3d")
    version("4.2.2", sha256="9981d0d53a356c4e87962847750a97c9e8054e460854748006c80f0d7e2b2d33")
    version("4.2.1", sha256="12ea7aa11e2bdb12de1dceb9939a22e96f5a480437cb17c123379d8e0fdf5e82")
    version("4.2.0", sha256="74814b63920aaee47dbbbee7082e5c4317e4eebaf07e03c5fb5626e1716f1034")
    version("4.1.0", sha256="f377d755c96a50f6bd2f423562598d822f43356783330a0b780ad442864d6eeb")
    version("4.0.0", sha256="d350f80e70654932db252db380d2ec0144a00e86f8d9f2b4c799ffdb48e9cdd1")
    version("3.7.2", sha256="de255bb42163a915312df9f4b86e5b874b46d9e8d4b72604b5123c3a845ed9b1")
    version("3.7.1", sha256="c9244e5905df6b0190113e26082c72d58b56b1b0dec66d076f083ce4089b0307")
    version("3.7.0", sha256="63873623917c756d1be49ff4d5fc23049736180e6b9a7d5236c6f204eddae3cc")
    version("3.6.0", sha256="3a18f24febb5203f11b0985b27e120ac623058d1d5ca79cd6df992e67d57240a")
    version("3.5.1", sha256="67eae714578b22d24192b0eb3a2d35b07578bbd57a33c50f1e74f8acd6378b3c")
    version("3.5.0", sha256="334429059cf82e222ca8a9d9dbbd26f8e1eb308613463c2b8655dd4201b127ec")
    version("3.4.1", sha256="27af1f11c8f23436915925b25cf6e1fb07fccf2d2a193a307c93437c60f63ba8")
    version("3.4.0", sha256="7583abf8905ba9dd5394294e815e8873635ac4e5067e63392e8a33b397e450d8")
    version("3.3.1", sha256="e0f1f43c65c4e0a38522b37e81f6129d8a1f7cd3d8884847be306544a7492747")
    version("3.3.0", sha256="05a03960de09d5775839c5766ad8a0a30f261feaba5fa53ce3e49168d1eee826")
    version("3.2.0", sha256="44ec129436f6de45f2230e14100104919443a1364c2491f5601666b358738bfa")
    version("3.1.0", sha256="d7f40d0cac95a06cea6cb5b7f7769085257caebc3ee84269dd9298da760d5615")
    version("3.0.0", sha256="530f5132e0a50da7ebb0ed08d9b6f1ddfd0d7d9b5d0beb2df5d687a4c8daf6b3")
    version("2.2.0", sha256="9379878a834d105a47a87d3d7b981852dd9f64bc16620eacd564b48533e169a7")
    version("2.1.1", sha256="83f67f28f4e47ff69043307d1791c9bffe83949e84165d49058b84eded932647")
    version("2.1.0", sha256="3371cd9050989173a3b27364668328653a65653a50a85c320adc53953b4d5f46")
    version("2.0.1", sha256="a863ed9e6fc420fbd92e63a12fe1a5b9be1a7a36f11f61f1fdc582c813bbe543")
    version("2.0.0", sha256="724da3c656f68e787a86ebb9844773aa1c2e3a873cc39462a8f1b336153d6cbb")

    variant(
        "nodepfail",
        default=True,
        description="Disable failing dependency checks due to injected absolute paths - "
        "required for most builds using bazel with spack",
    )

    # https://bazel.build/install/compile-source#bootstrap-unix-prereq
    depends_on("java@11", when="@5.3:", type=("build", "run"))
    depends_on("java@8,11", when="@3.3:5.2", type=("build", "run"))
    depends_on("java@8", when="@0.6:3.2", type=("build", "run"))
    depends_on("python+pythoncmd", type=("build", "run"))
    depends_on("zip", when="platform=linux", type=("build", "run"))

    # Pass Spack environment variables to the build
    patch("bazelruleclassprovider-0.25.patch")

    # Inject include paths
    patch("unix_cc_configure-3.0.patch", when="@3:")
    patch("unix_cc_configure-0.15.patch", when="@:2")

    # Set CC and CXX
    patch("compile-0.29.patch")

    # Disable dependency search
    patch("cppcompileaction-7.0.0.patch", when="@7: +nodepfail")
    patch("cppcompileaction-0.3.2.patch", when="@:6 +nodepfail")

    # https://github.com/bazelbuild/bazel/issues/17956
    patch("apple-clang-14.0.3.patch", when="@:4.2.3,5:6.1.1")

    # https://github.com/bazelbuild/bazel/issues/17958
    patch(
        "https://github.com/bazelbuild/bazel/commit/43dadb275b3f9690242bf2d94a0757c721d231a9.patch?full_index=1",
        sha256="af73a49006baa05475b1b79dad83e1e014ebfe22f38aa55774f9a465404aed54",
        when="@5.0:5.4.0,6.0",
    )

    # Fix build with Fujitsu compiler
    patch("blaze_util_posix-0.29.1.patch", when="%fj")
    patch("unix_cc_configure_fj-5.2.patch", when="@5.2:%fj")
    patch("unix_cc_configure_fj-5.0.patch", when="@5.0:5.1%fj")
    patch("unix_cc_configure_fj-0.29.1.patch", when="@:4%fj")
    patch("bazelruleclassprovider_fj-0.25.patch", when="%fj")

    # https://blog.bazel.build/2021/05/21/bazel-4-1.html
    conflicts("platform=darwin target=aarch64:", when="@:4.0")

    # https://github.com/bazelbuild/bazel/issues/18642
    patch(
        "https://github.com/bazelbuild/bazel/pull/20785.patch?full_index=1",
        sha256="85dde31d129bbd31e004c5c87f23cdda9295fbb22946dc6d362f23d83bae1fd8",
        when="@6.0:6.4",
    )
    conflicts("%gcc@13:", when="@:5")

    # Patches for compiling various older bazels which had ICWYU violations revealed by
    # (but not unique to) GCC 11 header changes. These are derived from
    # https://gitlab.alpinelinux.org/alpine/aports/-/merge_requests/29084/
    patch("gcc11_1.patch", when="@:4")
    patch("gcc11_2.patch", when="@:4")
    patch("gcc11_3.patch", when="@:4")
    patch("gcc11_4.patch", when="@4.1:4")

    # Bazel-4.0.0 does not compile with gcc-11
    # Newer versions of grpc and abseil dependencies are needed but are not in bazel-4.0.0
    conflicts("@4.0.0", when="%gcc@11:")

    executables = ["^bazel$"]

    # Download resources to perform offline build with bazel.
    # The following URLs and sha256 are in the file distdir_deps.bzl at the root of bazel sources.
    resource_dictionary = {}
    resource_dictionary["bazel_skylib"] = {
        "url": "https://github.com/bazelbuild/bazel-skylib/releases/download/1.0.1/bazel-skylib-1.0.1.tar.gz",
        "sha256": "f1c8360c01fcf276778d3519394805dc2a71a64274a3a0908bc9edff7b5aebc8",
        "when": "@4:6",
    }
    resource_dictionary["com_google_absl"] = {
        "url": "https://github.com/abseil/abseil-cpp/archive/refs/tags/20230802.0.tar.gz",
        "sha256": "59d2976af9d6ecf001a81a35749a6e551a335b949d34918cfade07737b9d93c5",
        "when": "@6.0:6.4",
    }
    resource_dictionary["zulu_11_56_19"] = {
        "url": "https://mirror.bazel.build/cdn.azul.com/zulu/bin/zulu11.56.19-ca-jdk11.0.15-linux_x64.tar.gz",
        "sha256": "e064b61d93304012351242bf0823c6a2e41d9e28add7ea7f05378b7243d34247",
        "when": "@6",
    }
    resource_dictionary["zulu_11_50_19"] = {
        "url": "https://mirror.bazel.build/openjdk/azul-zulu11.50.19-ca-jdk11.0.12/zulu11.50.19-ca-jdk11.0.12-linux_x64.tar.gz",
        "sha256": "b8e8a63b79bc312aa90f3558edbea59e71495ef1a9c340e38900dd28a1c579f3",
        "when": "@5",
    }
    resource_dictionary["zulu_11_37_17"] = {
        "url": "https://mirror.bazel.build/openjdk/azul-zulu11.37.17-ca-jdk11.0.6/zulu11.37.17-ca-jdk11.0.6-linux_x64.tar.gz",
        "sha256": "360626cc19063bc411bfed2914301b908a8f77a7919aaea007a977fa8fb3cde1",
        "when": "@4",
    }
    for resource_name in resource_dictionary.keys():
        resource(
            when=resource_dictionary[resource_name]["when"],
            name=resource_name,
            url=resource_dictionary[resource_name]["url"],
            sha256=resource_dictionary[resource_name]["sha256"],
            destination="archive",
            expand=False,
        )

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("version", output=str, error=str)
        match = re.search(r"Build label: ([\d.]+)", output)
        return match.group(1) if match else None

    def setup_build_environment(self, env):
        # fix the broken linking (on power9)
        # https://github.com/bazelbuild/bazel/issues/10327
        env.set("BAZEL_LINKOPTS", "")
        env.set("BAZEL_LINKLIBS", "-lstdc++")

        # .WARNING: Option 'host_javabase' is deprecated
        # Use local java installation
        args = "--color=no --define=ABSOLUTE_JAVABASE={0} --verbose_failures --jobs={1}".format(
            self.spec["java"].prefix, make_jobs
        )

        resource_stages = self.stage[1:]
        for _resource in resource_stages:
            try:
                resource_name = _resource.resource.name
                if self.spec.satisfies(self.resource_dictionary[resource_name]["when"]):
                    archive_path = _resource.source_path
                    args += " --distdir={0}".format(archive_path)
            except AttributeError:
                continue

        env.set("EXTRA_BAZEL_ARGS", args)

    @run_before("install")
    def bootstrap(self):
        bash = which("bash")
        bash("./compile.sh")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("output/bazel", prefix.bin)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        # https://github.com/Homebrew/homebrew-core/blob/master/Formula/bazel.rb

        # Bazel does not work properly on NFS, switch to /tmp
        with working_dir("/tmp/spack/bazel/spack-test", create=True):
            touch("WORKSPACE")

            with open("ProjectRunner.java", "w") as f:
                f.write(
                    """\
public class ProjectRunner {
    public static void main(String args[]) {
        System.out.println("Hi!");
    }
}"""
                )

            with open("BUILD", "w") as f:
                f.write(
                    """\
java_binary(
    name = "bazel-test",
    srcs = glob(["*.java"]),
    main_class = "ProjectRunner",
)"""
                )

            # Spack's logs don't handle colored output well
            bazel = Executable(self.spec["bazel"].command.path)
            bazel(
                "--output_user_root=/tmp/spack/bazel/spack-test",
                "build",
                "--color=no",
                f"--jobs={make_jobs}",
                "//:bazel-test",
            )

            exe = Executable("bazel-bin/bazel-test")
            assert exe(output=str) == "Hi!\n"

    def setup_dependent_package(self, module, dependent_spec):
        module.bazel = Executable(self.spec["bazel"].command.path)

    @property
    def parallel(self):
        return not self.spec.satisfies("%fj")
