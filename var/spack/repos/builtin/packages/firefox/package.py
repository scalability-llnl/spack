# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *
from spack.util.prefix import Prefix


class Firefox(Package):
    """The FireFox web browser by Mozilla"""

    homepage = "https://www.firefox.com"
    url = "https://archive.mozilla.org/pub/firefox/releases/128.3.1esr/source/firefox-128.3.1esr.source.tar.xz"
    list_url = "https://archive.mozilla.org/pub/firefox/releases/"

    maintainers("teaguesterling")

    license("MPL", checked_by="teaguesterling")

    # ESR releases are enterprise support
    version("130.0.1", sha256="027225a1e9b074f0072e22c7264cf27b0d2364c675c3ca811aa6c25fb01b9f70")
    version(
        "128.3.1esr",
        sha256="c1f4052f3a88d96a122551d5025053304007f7649886d5e2fdfd1a11ce3d70a8",
        preferred=True,
    )
    version("127.0", sha256="ea6b089ff046ca503978fdaf11ea123c64f66bbcdc4a968bed8f7c93e9994321")

    phases = ["configure", "build", "install"]

    # From Arch build notes
    depends_on("dbus-glib")
    depends_on("ffmpeg")
    depends_on("gtkplus@3")
    depends_on("libxscrnsaver")
    depends_on("libxt")
    depends_on("nss")
    depends_on("pulseaudio")
    depends_on("shared-mime-info")

    # Also needed for mach configure to succeeed
    depends_on("libx11")
    depends_on("libxcb")
    depends_on("libxext")
    depends_on("libxrandr@1.4.0:")
    depends_on("libxcursor")
    depends_on("libxdamage")
    depends_on("libxcomposite")
    depends_on("libxkbcommon")

    # Needed for build to succeed after configuration
    depends_on("at-spi2-core@2")
    depends_on("libnotify")

    with default_args(type="build"):
        depends_on("binutils")
        depends_on("diffutils")
        depends_on("git")
        depends_on("gmake")
        depends_on("imake")
        depends_on("llvm")
        depends_on("m4")
        depends_on("mawk")
        depends_on("mesa")
        depends_on("nasm")
        depends_on("node-js")
        depends_on("pciutils")
        depends_on("pkgconfig")
        depends_on("python@3.6:3.11")
        depends_on("rust")
        depends_on("unzip")
        depends_on("wasi-sdk@14:")
        depends_on("wget")
        depends_on("yasm")
        depends_on("zip")

        depends_on("cbindgen")
        depends_on("generate-ninja")  # Maybe this should be a buid_system option

        # Python requirements for mach
        depends_on("py-appdirs@1.4:")
        depends_on("py-attrs@17.4.0:")
        depends_on("py-click@7:")
        depends_on("py-diskcache@4:")
        depends_on("py-jinja2@2.10.1:")
        depends_on("py-jsonschema@3.0.2:")
        depends_on("py-markupsafe@2.0:")
        depends_on("py-pyrsistent@0.16.0:")  # This states 0.14.0 but we need it a bit higher
        depends_on("py-pyyaml@5.3.1:")
        depends_on("py-semver@2.13.0:")
        depends_on("py-six")

        # These are strictly limited or bounded in the pyproject.toml
        depends_on("py-psutil@5.4.2:5.9.4")
        depends_on("py-zstandard@0.11.1:0.22.0")

        # Version specific build/api dependency requirements
        with when("@127:128"):
            depends_on("rust@:1.79")  # API changes after 1.80 break
            depends_on("at-spi2-core@2:2.38")  # Version 2.58 fails, 2.38 confirmed
            depends_on("py-attrs@17.4.0")
            depends_on("py-glean-sdk@60.0.1")
            depends_on("py-glean-parser@14.0")
        with when("@131"):  # These may apply more generally backwards/forwards
            depends_on("rust@1.80:")
            depends_on("at-spi2-core@2:2.38")  # Version 2.58 fails, 2.38 confirmed
            depends_on("py-attrs@23.1")
            depends_on("py-glean-sdk@60.4.0")
            depends_on("py-glean-parser@14.3")

    conflicts("py-pyrsistent@0.17.0:0.17.2", msg="Noted in mach requirements file")

    # Until full GCC 14 support has been patched (check each new release)
    with when("@127:128%gcc@14:"):
        patch("gcc14-implicit-include-fix.patch")
        patch("gcc14-implicit-pointer-cast-fix.patch")

    def url_for_version(self, version):
        return f"{self.list_url}/{version}/source/firefox-{version}.source.tar.xz"

    def mach(self, command, *args):
        mach = which("./mach")
        print(f"Running {mach} {command} {args}")
        return mach("--verbose", command, *args)

    @property
    def build_cache_dir(self):
        return Prefix(f"{self.stage.source_path}/.mozbuild")

    @property
    def build_config(self):
        return self.build_cache_dir.join("mozconfig-firefox")

    def setup_build_enviroment(self, env):
        # Adapted from: https://www.talospace.com/2021/12/firefox-95-on-power.html
        print("BUILD ENV SETUP")
        env.set("MOZBUILD_STATE_PATH", self.build_cache_dir)
        env.set("MOZCONFIG", self.build_config)
        env.set("GN", self.spec["generate-ninja"].home.bin.gn)
        env.set("RUSTC_OPT_LEVEL", "2")

    def patch(self):
        # Make the wasi clib available without re-downloading
        # Adapted from LibreWolf insatller:
        # https://codeberg.org/librewolf/source/src/branch/main/scripts/setup-wasi-linux.sh
        mozbuild = self.build_cache_dir
        mkdirp(mozbuild.wrlb)
        symlink(self.spec["wasi-sdk"].home, mozbuild.wrlb.join("wasi-sysroot"))

    def build_args(self):
        args = []
        args.append(f"--jobs={make_jobs}")
        return args

    def configure_args(self):
        args = []

        # Adapted from: https://www.talospace.com/2021/12/firefox-95-on-power.html
        args += [
            "--without-wasm-sandboxed-libraries",  # Required to use wasi-sdk
            "--enable-application=browser",  # Build the desktop browser (not android)
            "--enable-release",
            "--with-branding=browser/branding/official",
            # "--enable-lto=full",  # Should this be a varaint?
            "MOZ_PGO=1",
        ]
        return args

    def configure(self, spec, prefix):
        self.mach("configure", *self.configure_args())

    def build(self, spec, prefix):
        self.mach("build", *self.build_args())

    def install(self, spec, prefix):
        arch = spec.architecture.target.family.name
        platform = spec.architecture.platform
        found = find(".", f"obj-{arch}-*-{platform}-*")
        package_dir = found[0]
        self.mach("package")
        install_tree(f"{package_dir}/dist/firefox", prefix.opt.firefox)
        mkdir(prefix.bin)
        symlink(prefix.opt.firefox.firefox, prefix.bin.firefox)
