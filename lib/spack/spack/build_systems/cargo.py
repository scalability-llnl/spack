# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import inspect
import json

from llnl.util.filesystem import join_path, copy, mkdirp
from spack.directives import cargo_manifest, conflicts, depends_on, variant
from spack.package import PackageBase
from spack.util.executable import Executable
from spack.util.rust import target_triple_for_spec, RustQuery


class CargoPackage(PackageBase):
    """
    Specialized class for installing packages that use the Cargo package
    manager.

    Cargo is the official build tool and package manager of the Rust
    programming language. It has its own package repository, which this
    class will automatically pull from while ensuring checksums are respected.

    This package can install both executable files and C-style static and
    dynamic libraries from a cargo package. It can not install native
    Rust-style libraries.
    """

    phases = ['build', 'install']

    build_system_class = 'CargoPackage'

    variant('build_type',
            default='release',
            description='Cargo build type',
            values=('debug', 'release'))

    variant(
        'prefer_dynamic',
        default=True,
        description='Link Rust standard library dynamically'
    )

    variant(
        'lto',
        default='none',
        description='Link binaries with link-time optimization',
        values=('none', 'thin', 'fat')
    )

    conflicts(
        'lto=thin',
        when='+prefer_dynamic',
        msg="LTO is not possible when linking the Rust standard library "
            "dynamically. Set '~prefer_dynamic' for this package to enable "
            "LTO."
    )

    conflicts(
        'lto=fat',
        when='+prefer_dynamic',
        msg="LTO is not possible when linking the Rust standard library "
            "dynamically. Set '~prefer_dynamic' for this package to enable "
            "LTO."
    )

    # The differing dependency type is OK because the two `when` conditions
    # are mutually exclusive.
    depends_on('rust', type='build', when='~prefer_dynamic')
    depends_on('rust', type=('build', 'link'), when='+prefer_dynamic')

    cargo_manifest()

    @property
    def cargo(self):
        cargo = Executable(self.spec['rust'].prefix.bin.cargo)
        cargo.add_default_arg('--locked')
        cargo.add_default_arg('--offline')
        return cargo

    @property
    def rustc(self):
        return Executable(self.spec['rust'].prefix.bin.rustc)

    @property
    def target_cpu(self):
        """This routine returns the target_cpu that Rust should optimize for.
        It uses the same names as clang thanks to the shared LLVM backend. We
        use Rust's LLVM version in place of the clang version."""

        return RustQuery(self.rustc).target_cpu(self.spec)

    @property
    def manifest_path(self):
        return join_path(self.stage.source_path, self.cargo_manifest)

    @property
    def metadata(self):
        """Returns the metadata description of the crate.

        Used to determine the installable targets in the crate"""

        feature_args = self._feature_args()

        return json.loads(inspect.getmodule(self).cargo(
            'metadata', '--manifest-path', self.manifest_path,
            '--format-version', '1',
            *feature_args,
            output=str))

    @property
    def target_path(self):
        return join_path(
            self.stage.source_path, 'target',
            target_triple_for_spec(self.spec),
            self.spec.variants['build_type'].value)

    def do_stage(self, mirror_only=False):
        """Stages and sets the config for chosen build settings"""
        super(CargoPackage, self).do_stage(mirror_only)

        rustflags = []

        target = target_triple_for_spec(self.spec)

        target_cpu = self.target_cpu
        if target_cpu:
            rustflags.extend(["-C", "target-cpu={0}".format(target_cpu)])

        # Put config in spack-src so that it does not overwrite the config
        # from vendoring dependencies
        mkdirp(join_path(self.stage.source_path, '.cargo'))
        config_path = join_path(self.stage.source_path, '.cargo/config')

        build_type = self.spec.variants['build_type'].value
        lto = self.spec.variants['lto'].value

        profile = 'dev' if build_type == 'debug' else build_type
        lto = 'off' if lto == 'none' else lto

        with open(config_path, 'w') as f:
            f.write("""
[build]
target = "{target}"
rustflags = "{flags}"

[profile.{profile}]
rpath = true
lto = "{lto}"
""".format(
                target=target,
                flags=" ".join(rustflags),
                profile=profile,
                lto=lto
            ))

    def workspace_targets(self):
        metadata = self.metadata
        for p in metadata["packages"]:
            for w in metadata["workspace_members"]:
                if p["id"] == w:
                    for target in p["targets"]:
                        yield target

    def cargo_features(self):
        """Features to build cargo project with. Overridable by package."""
        return None

    def _feature_args(self):
        """Returns the args associated with cargo_features"""
        features = self.cargo_features()
        if features is None:
            return []

        args = ["--no-default-features"]

        for feature in features:
            args += ["--features", feature]

        return args

    def build(self, spec, prefix):
        """cargo build"""
        jobs = inspect.getmodule(self).make_jobs

        # Explicitly build each target in the workspace
        for target in self.workspace_targets():
            args = [
                "rustc", "--jobs", str(jobs), "-vv", "--manifest-path",
                self.manifest_path
            ]

            if 'build_type=release' in self.spec:
                args += ["--release"]

            args += self._feature_args()

            if "bin" in target["kind"]:
                args += ["--bin"]
            elif "staticlib" in target["kind"]:
                args += ["--lib"]
            elif "cdylib" in target["kind"]:
                args += ["--lib"]
            else:
                continue

            args += [target["name"], "--"]

            args += ["--cap-lints", "warn"]
            if '+prefer_dynamic' in self.spec:
                args += ["--codegen", "prefer-dynamic"]

            self.cargo(*args)

    def install(self, spec, prefix):
        """Install cargo targets"""

        # This is not implemented using "cargo install" because we want to
        # install libraries, too.
        so_ext = 'dylib' if 'platform=darwin' in self.spec else 'so'

        # This loop attempts to install all
        for target in self.workspace_targets():
            if "bin" in target["kind"]:
                mkdirp(prefix.bin)
                copy(
                    join_path(self.target_path, target["name"]),
                    prefix.bin
                )

            if "staticlib" in target["kind"]:
                mkdirp(prefix.lib)
                copy(
                    join_path(
                        self.target_path, "lib{0}.a".format(target["name"])),
                    prefix.lib
                )

            if "cdylib" in target["kind"]:
                mkdirp(prefix.lib)
                copy(
                    join_path(
                        self.target_path,
                        "lib{0}.{1}".format(target["name"], so_ext)
                    ),
                    prefix.lib
                )
