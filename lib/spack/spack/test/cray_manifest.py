# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Note that where possible, this should produce specs using `entries_to_specs`
rather than `spec_from_entry`, since the former does additional work to
establish dependency relationships (and in general the manifest-parsing
logic needs to consume all related specs in a single pass).
"""
import json
import os

import pytest

import spack
import spack.cmd
import spack.cmd.external
import spack.compilers
import spack.cray_manifest as cray_manifest
import spack.platforms
import spack.platforms.test
import spack.solver.asp
import spack.spec
import spack.store
from spack.cray_manifest import compiler_from_entry, entries_to_specs


class JsonSpecEntry:
    def __init__(self, name, hash, prefix, version, arch, compiler, dependencies, parameters):
        self.name = name
        self.hash = hash
        self.prefix = prefix
        self.version = version
        self.arch = arch
        self.compiler = compiler
        self.dependencies = dependencies
        self.parameters = parameters

    def to_dict(self):
        return {
            "name": self.name,
            "hash": self.hash,
            "prefix": self.prefix,
            "version": self.version,
            "arch": self.arch,
            "compiler": self.compiler,
            "dependencies": self.dependencies,
            "parameters": self.parameters,
        }

    def as_dependency(self, deptypes):
        return (self.name, {"hash": self.hash, "type": list(deptypes)})


class JsonArchEntry:
    def __init__(self, platform, os, target):
        self.platform = platform
        self.os = os
        self.target = target

    def spec_json(self):
        return {"platform": self.platform, "platform_os": self.os, "target": {"name": self.target}}

    def compiler_json(self):
        return {"os": self.os, "target": self.target}


class JsonCompilerEntry:
    def __init__(self, name, version, arch=None, executables=None):
        self.name = name
        self.version = version
        if not arch:
            arch = JsonArchEntry("anyplatform", "anyos", "anytarget")
        if not executables:
            executables = {
                "cc": "/path/to/compiler/cc",
                "cxx": "/path/to/compiler/cxx",
                "fc": "/path/to/compiler/fc",
            }
        self.arch = arch
        self.executables = executables

    def compiler_json(self):
        return {
            "name": self.name,
            "version": self.version,
            "arch": self.arch.compiler_json(),
            "executables": self.executables,
        }

    def spec_json(self):
        """The compiler spec only lists the name/version, not
        arch/executables.
        """
        return {"name": self.name, "version": self.version}


@pytest.fixture
def _common_arch(test_platform):
    return JsonArchEntry(
        platform=test_platform.name,
        os=test_platform.front_os,
        target=test_platform.target("fe").name,
    )


@pytest.fixture
def _common_compiler(_common_arch):
    return JsonCompilerEntry(
        name="gcc",
        version="10.2.0.2112",
        arch=_common_arch,
        executables={
            "cc": "/path/to/compiler/cc",
            "cxx": "/path/to/compiler/cxx",
            "fc": "/path/to/compiler/fc",
        },
    )


@pytest.fixture
def _other_compiler(_common_arch):
    return JsonCompilerEntry(
        name="clang",
        version="3.0.0",
        arch=_common_arch,
        executables={
            "cc": "/path/to/compiler/clang",
            "cxx": "/path/to/compiler/clang++",
            "fc": "/path/to/compiler/flang",
        },
    )


@pytest.fixture
def _raw_json_x(_common_arch):
    return {
        "name": "packagex",
        "hash": "hash-of-x",
        "prefix": "/path/to/packagex-install/",
        "version": "1.0",
        "arch": _common_arch.spec_json(),
        "compiler": {"name": "gcc", "version": "10.2.0.2112"},
        "dependencies": {"packagey": {"hash": "hash-of-y", "type": ["link"]}},
        "parameters": {"precision": ["double", "float"]},
    }


def test_manifest_compatibility(_common_arch, _common_compiler, _raw_json_x):
    """Make sure that JsonSpecEntry outputs the expected JSON structure
    by comparing it with JSON parsed from an example string. This
    ensures that the testing objects like JsonSpecEntry produce the
    same JSON structure as the expected file format.
    """
    y = JsonSpecEntry(
        name="packagey",
        hash="hash-of-y",
        prefix="/path/to/packagey-install/",
        version="1.0",
        arch=_common_arch.spec_json(),
        compiler=_common_compiler.spec_json(),
        dependencies={},
        parameters={},
    )

    x = JsonSpecEntry(
        name="packagex",
        hash="hash-of-x",
        prefix="/path/to/packagex-install/",
        version="1.0",
        arch=_common_arch.spec_json(),
        compiler=_common_compiler.spec_json(),
        dependencies=dict([y.as_dependency(deptypes=["link"])]),
        parameters={"precision": ["double", "float"]},
    )

    x_from_entry = x.to_dict()
    assert x_from_entry == _raw_json_x


def test_compiler_from_entry():
    compiler_data = json.loads(
        """\
{
  "name": "gcc",
  "prefix": "/path/to/compiler/",
  "version": "7.5.0",
  "arch": {
    "os": "centos8",
    "target": "x86_64"
  },
  "executables": {
    "cc": "/path/to/compiler/cc",
    "cxx": "/path/to/compiler/cxx",
    "fc": "/path/to/compiler/fc"
  }
}
"""
    )
    compiler = compiler_from_entry(compiler_data, "/example/file")
    assert compiler.cc == "/path/to/compiler/cc"
    assert compiler.cxx == "/path/to/compiler/cxx"
    assert compiler.fc == "/path/to/compiler/fc"
    assert compiler.operating_system == "centos8"


@pytest.fixture
def generate_openmpi_entries(_common_arch, _common_compiler):
    """Generate two example JSON entries that refer to an OpenMPI
    installation and a hwloc dependency.
    """
    # The hashes need to be padded with 'a' at the end to align with 8-byte
    # boundaries (for base-32 decoding)
    hwloc = JsonSpecEntry(
        name="hwloc",
        hash="hwlocfakehashaaa",
        prefix="/path/to/hwloc-install/",
        version="2.0.3",
        arch=_common_arch.spec_json(),
        compiler=_common_compiler.spec_json(),
        dependencies={},
        parameters={},
    )

    # This includes a variant which is guaranteed not to appear in the
    # OpenMPI package: we need to make sure we can use such package
    # descriptions.
    openmpi = JsonSpecEntry(
        name="openmpi",
        hash="openmpifakehasha",
        prefix="/path/to/openmpi-install/",
        version="4.1.0",
        arch=_common_arch.spec_json(),
        compiler=_common_compiler.spec_json(),
        dependencies=dict([hwloc.as_dependency(deptypes=["link"])]),
        parameters={"internal-hwloc": False, "fabrics": ["psm"], "missing_variant": True},
    )

    return list(x.to_dict() for x in [openmpi, hwloc])


def test_generate_specs_from_manifest(generate_openmpi_entries):
    """Given JSON entries, check that we can form a set of Specs
    including dependency references.
    """
    specs = entries_to_specs(generate_openmpi_entries)
    (openmpi_spec,) = list(x for x in specs.values() if x.name == "openmpi")
    assert openmpi_spec["hwloc"]


def test_translate_cray_platform_to_linux(monkeypatch, _common_compiler):
    """Manifests might list specs on newer Cray platforms as being "cray",
    but Spack identifies such platforms as "linux". Make sure we
    automaticaly transform these entries.
    """
    test_linux_platform = spack.platforms.test.Test("linux")

    def the_host_is_linux():
        return test_linux_platform

    monkeypatch.setattr(spack.platforms, "host", the_host_is_linux)

    cray_arch = JsonArchEntry(platform="cray", os="rhel8", target="x86_64")
    spec_json = JsonSpecEntry(
        name="cray-mpich",
        hash="craympichfakehashaaa",
        prefix="/path/to/cray-mpich/",
        version="1.0.0",
        arch=cray_arch.spec_json(),
        compiler=_common_compiler.spec_json(),
        dependencies={},
        parameters={},
    ).to_dict()

    (spec,) = entries_to_specs([spec_json]).values()
    assert spec.architecture.platform == "linux"


def test_translate_compiler_name(_common_arch):
    nvidia_compiler = JsonCompilerEntry(
        name="nvidia",
        version="19.1",
        arch=_common_arch,
        executables={"cc": "/path/to/compiler/nvc", "cxx": "/path/to/compiler/nvc++"},
    )

    compiler = compiler_from_entry(nvidia_compiler.compiler_json(), "/example/file")
    assert compiler.name == "nvhpc"

    spec_json = JsonSpecEntry(
        name="hwloc",
        hash="hwlocfakehashaaa",
        prefix="/path/to/hwloc-install/",
        version="2.0.3",
        arch=_common_arch.spec_json(),
        compiler=nvidia_compiler.spec_json(),
        dependencies={},
        parameters={},
    ).to_dict()

    (spec,) = entries_to_specs([spec_json]).values()
    assert spec.compiler.name == "nvhpc"


def test_failed_translate_compiler_name(_common_arch):
    unknown_compiler = JsonCompilerEntry(name="unknown", version="1.0")

    with pytest.raises(spack.compilers.UnknownCompilerError):
        compiler_from_entry(unknown_compiler.compiler_json(), "/example/file")

    spec_json = JsonSpecEntry(
        name="packagey",
        hash="hash-of-y",
        prefix="/path/to/packagey-install/",
        version="1.0",
        arch=_common_arch.spec_json(),
        compiler=unknown_compiler.spec_json(),
        dependencies={},
        parameters={},
    ).to_dict()

    with pytest.raises(spack.compilers.UnknownCompilerError):
        entries_to_specs([spec_json])


@pytest.fixture
def manifest_content(generate_openmpi_entries, _common_compiler, _other_compiler):
    return {
        # Note: the cray_manifest module doesn't use the _meta section right
        # now, but it is anticipated to be useful
        "_meta": {
            "file-type": "cray-pe-json",
            "system-type": "test",
            "schema-version": "1.3",
            "cpe-version": "22.06",
        },
        "specs": generate_openmpi_entries,
        "compilers": [_common_compiler.compiler_json(), _other_compiler.compiler_json()],
    }


def test_read_cray_manifest(
    tmpdir, mutable_config, mock_packages, mutable_database, manifest_content
):
    """Check that (a) we can read the cray manifest and add it to the Spack
    Database and (b) we can concretize specs based on that.
    """
    with tmpdir.as_cwd():
        test_db_fname = "external-db.json"
        with open(test_db_fname, "w") as db_file:
            json.dump(manifest_content, db_file)
        cray_manifest.read(test_db_fname, True)
        query_specs = spack.store.STORE.db.query("openmpi")
        assert any(x.dag_hash() == "openmpifakehasha" for x in query_specs)

        concretized_specs = spack.cmd.parse_specs(
            "depends-on-openmpi ^/openmpifakehasha".split(), concretize=True
        )
        assert concretized_specs[0]["hwloc"].dag_hash() == "hwlocfakehashaaa"


def test_read_cray_manifest_add_compiler_failure(
    tmpdir, mutable_config, mock_packages, mutable_database, manifest_content, monkeypatch
):
    """Check that cray manifest can be read even if some compilers cannot
    be added.
    """
    orig_add_compilers_to_config = spack.compilers.add_compilers_to_config

    class fail_for_clang:
        def __init__(self):
            self.called_with_clang = False

        def __call__(self, compilers, **kwargs):
            if any(x.name == "clang" for x in compilers):
                self.called_with_clang = True
                raise Exception()
            return orig_add_compilers_to_config(compilers, **kwargs)

    checker = fail_for_clang()
    monkeypatch.setattr(spack.compilers, "add_compilers_to_config", checker)

    with tmpdir.as_cwd():
        test_db_fname = "external-db.json"
        with open(test_db_fname, "w") as db_file:
            json.dump(manifest_content, db_file)
        cray_manifest.read(test_db_fname, True)
        query_specs = spack.store.STORE.db.query("openmpi")
        assert any(x.dag_hash() == "openmpifakehasha" for x in query_specs)

    assert checker.called_with_clang


def test_read_cray_manifest_twice_no_compiler_duplicates(
    tmpdir, mutable_config, mock_packages, mutable_database, manifest_content
):
    with tmpdir.as_cwd():
        test_db_fname = "external-db.json"
        with open(test_db_fname, "w") as db_file:
            json.dump(manifest_content, db_file)

        # Read the manifest twice
        cray_manifest.read(test_db_fname, True)
        cray_manifest.read(test_db_fname, True)

        compilers = spack.compilers.all_compilers()
        filtered = list(
            c for c in compilers if c.spec == spack.spec.CompilerSpec("gcc@=10.2.0.2112")
        )
        assert len(filtered) == 1


def test_read_old_manifest_v1_2(tmpdir, mutable_config, mock_packages, mutable_database):
    """Test reading a file using the older format
    ('version' instead of 'schema-version').
    """
    manifest_dir = str(tmpdir.mkdir("manifest_dir"))
    manifest_file_path = os.path.join(manifest_dir, "test.json")
    with open(manifest_file_path, "w") as manifest_file:
        manifest_file.write(
            """\
{
  "_meta": {
    "file-type": "cray-pe-json",
    "system-type": "EX",
    "version": "1.3"
  },
  "specs": []
}
"""
        )
    cray_manifest.read(manifest_file_path, True)


def test_convert_validation_error(tmpdir, mutable_config, mock_packages, mutable_database):
    manifest_dir = str(tmpdir.mkdir("manifest_dir"))
    # Does not parse as valid JSON
    invalid_json_path = os.path.join(manifest_dir, "invalid-json.json")
    with open(invalid_json_path, "w") as f:
        f.write(
            """\
{
"""
        )
    with pytest.raises(cray_manifest.ManifestValidationError) as e:
        cray_manifest.read(invalid_json_path, True)
    str(e)

    # Valid JSON, but does not conform to schema (schema-version is not a string
    # of length > 0)
    invalid_schema_path = os.path.join(manifest_dir, "invalid-schema.json")
    with open(invalid_schema_path, "w") as f:
        f.write(
            """\
{
  "_meta": {
    "file-type": "cray-pe-json",
    "system-type": "EX",
    "schema-version": ""
  },
  "specs": []
}
"""
        )
    with pytest.raises(cray_manifest.ManifestValidationError) as e:
        cray_manifest.read(invalid_schema_path, True)
    str(e)


@pytest.fixture
def directory_with_manifest(tmpdir, manifest_content):
    """Create a manifest file in a directory. Used by 'spack external'."""
    with tmpdir.as_cwd():
        test_db_fname = "external-db.json"
        with open(test_db_fname, "w") as db_file:
            json.dump(manifest_content, db_file)

    yield str(tmpdir)


def test_find_external_nonempty_default_manifest_dir(
    mutable_database, mutable_mock_repo, tmpdir, monkeypatch, directory_with_manifest
):
    """The user runs 'spack external find'; the default manifest directory
    contains a manifest file. Ensure that the specs are read.
    """
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(spack.cray_manifest, "default_path", str(directory_with_manifest))
    spack.cmd.external._collect_and_consume_cray_manifest_files(ignore_default_dir=False)
    specs = spack.store.STORE.db.query("hwloc")
    assert any(x.dag_hash() == "hwlocfakehashaaa" for x in specs)


def test_reusable_externals_cray_manifest(
    tmpdir, mutable_config, mock_packages, temporary_store, manifest_content
):
    """The concretizer should be able to reuse specs imported from a manifest without a
    externals config entry in packages.yaml"""
    with tmpdir.as_cwd():
        with open("external-db.json", "w") as f:
            json.dump(manifest_content, f)
        cray_manifest.read(path="external-db.json", apply_updates=True)

        # Get any imported spec
        spec = temporary_store.db.query_local()[0]

        # Reusable if imported locally
        assert spack.solver.asp._is_reusable(spec, packages={}, local=True)

        # If cray manifest entries end up in a build cache somehow, they are not reusable
        assert not spack.solver.asp._is_reusable(spec, packages={}, local=False)
