# Copyright Spack Project Developers. See COPYRIGHT file for details.
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

import archspec.cpu

import spack
import spack.cmd
import spack.cmd.external
import spack.compilers.config
import spack.cray_manifest as cray_manifest
import spack.platforms
import spack.platforms.test
import spack.solver.asp
import spack.spec
import spack.store
from spack.cray_manifest import compiler_from_entry, entries_to_specs

pytestmark = [
    pytest.mark.skipif(
        str(spack.platforms.host()) != "linux", reason="Cray manifest files are only for linux"
    ),
    pytest.mark.usefixtures("mutable_config", "mock_packages"),
]


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
    def __init__(self, *, name, version, arch=None, executables=None, prefix=None):
        self.name = name
        self.version = version
        self.arch = arch or JsonArchEntry("anyplatform", "anyos", "anytarget")
        self.executables = executables or {"cc": "cc", "cxx": "cxx", "fc": "fc"}
        self.prefix = prefix

    def compiler_json(self):
        result = {
            "name": self.name,
            "version": self.version,
            "arch": self.arch.compiler_json(),
            "executables": self.executables,
        }
        # See https://github.com/spack/spack/pull/40061
        if self.prefix is not None:
            result["prefix"] = self.prefix
        return result

    def spec_json(self):
        """The compiler spec only lists the name/version, not
        arch/executables.
        """
        return {"name": self.name, "version": self.version}


@pytest.fixture
def _common_arch(test_platform):
    generic = archspec.cpu.TARGETS[test_platform.default].family
    return JsonArchEntry(platform=test_platform.name, os="redhat6", target=generic.name)


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


def test_compiler_from_entry(mock_executable):
    """Tests that we can detect a compiler from a valid entry in the Cray manifest"""
    cc = mock_executable("gcc", output="echo 7.5.0")
    cxx = mock_executable("g++", output="echo 7.5.0")
    fc = mock_executable("gfortran", output="echo 7.5.0")

    compiler = compiler_from_entry(
        JsonCompilerEntry(
            name="gcc",
            version="7.5.0",
            arch=JsonArchEntry(platform="linux", os="centos8", target="x86_64"),
            prefix=str(cc.parent),
            executables={"cc": "gcc", "cxx": "g++", "fc": "gfortran"},
        ).compiler_json(),
        manifest_path="/example/file",
    )

    assert compiler.satisfies("gcc@7.5.0 target=x86_64 os=centos8")
    assert compiler.extra_attributes["compilers"]["c"] == str(cc)
    assert compiler.extra_attributes["compilers"]["cxx"] == str(cxx)
    assert compiler.extra_attributes["compilers"]["fortran"] == str(fc)


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
        name="mpich",
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


@pytest.mark.parametrize(
    "name_in_manifest,expected_name",
    [("nvidia", "nvhpc"), ("rocm", "llvm-amdgpu"), ("clang", "llvm")],
)
def test_translated_compiler_name(name_in_manifest, expected_name):
    assert cray_manifest.translated_compiler_name(name_in_manifest) == expected_name


def test_failed_translate_compiler_name(_common_arch):
    unknown_compiler = JsonCompilerEntry(name="unknown", version="1.0")

    with pytest.raises(spack.compilers.config.UnknownCompilerError):
        compiler_from_entry(unknown_compiler.compiler_json(), manifest_path="/example/file")

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

    with pytest.raises(spack.compilers.config.UnknownCompilerError):
        entries_to_specs([spec_json])


@pytest.fixture
def manifest_content(generate_openmpi_entries, _common_compiler, _other_compiler):
    return {
        "_meta": {
            "file-type": "cray-pe-json",
            "system-type": "EX",
            "schema-version": "1.3",
            "cpe-version": "22.06",
        },
        "specs": generate_openmpi_entries,
        "compilers": [_common_compiler.compiler_json(), _other_compiler.compiler_json()],
    }


def test_read_cray_manifest(temporary_store, manifest_file):
    """Check that (a) we can read the cray manifest and add it to the Spack
    Database and (b) we can concretize specs based on that.
    """
    cray_manifest.read(str(manifest_file), True)

    query_specs = temporary_store.db.query("openmpi")
    assert any(x.dag_hash() == "openmpifakehasha" for x in query_specs)

    concretized_spec = spack.spec.Spec("depends-on-openmpi ^/openmpifakehasha").concretized()
    assert concretized_spec["hwloc"].dag_hash() == "hwlocfakehashaaa"


def test_read_cray_manifest_add_compiler_failure(temporary_store, manifest_file, monkeypatch):
    """Tests the Cray manifest can be read even if some compilers cannot be added."""

    def _mock(entry, *, manifest_path):
        if entry["name"] == "clang":
            raise RuntimeError("cannot determine the compiler")
        return spack.spec.Spec(f"{entry['name']}@{entry['version']}")

    monkeypatch.setattr(cray_manifest, "compiler_from_entry", _mock)

    cray_manifest.read(str(manifest_file), True)
    query_specs = spack.store.STORE.db.query("openmpi")
    assert any(x.dag_hash() == "openmpifakehasha" for x in query_specs)


def test_read_cray_manifest_twice_no_duplicates(
    mutable_config, temporary_store, manifest_file, monkeypatch, tmp_path
):
    def _mock(entry, *, manifest_path):
        return spack.spec.Spec(f"{entry['name']}@{entry['version']}", external_path=str(tmp_path))

    monkeypatch.setattr(cray_manifest, "compiler_from_entry", _mock)

    # Read the manifest twice
    cray_manifest.read(str(manifest_file), True)
    cray_manifest.read(str(manifest_file), True)

    config_data = mutable_config.get("packages")["gcc"]
    assert "externals" in config_data

    specs = [spack.spec.Spec(x["spec"]) for x in config_data["externals"]]
    assert len(specs) == len(set(specs))
    assert len([c for c in specs if c.satisfies("gcc@10.2.0.2112")]) == 1


def test_read_old_manifest_v1_2(tmp_path, temporary_store):
    """Test reading a file using the older format ('version' instead of 'schema-version')."""
    manifest = tmp_path / "manifest_dir" / "test.json"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(
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
    cray_manifest.read(str(manifest), True)


def test_convert_validation_error(tmpdir, mutable_config, mock_packages, temporary_store):
    manifest_dir = str(tmpdir.mkdir("manifest_dir"))
    # Does not parse as valid JSON
    invalid_json_path = os.path.join(manifest_dir, "invalid-json.json")
    with open(invalid_json_path, "w", encoding="utf-8") as f:
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
    with open(invalid_schema_path, "w", encoding="utf-8") as f:
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


@pytest.fixture
def manifest_file(tmp_path, manifest_content):
    """Create a manifest file in a directory. Used by 'spack external'."""
    filename = tmp_path / "external-db.json"
    with open(filename, "w", encoding="utf-8") as db_file:
        json.dump(manifest_content, db_file)
    return filename


def test_find_external_nonempty_default_manifest_dir(
    temporary_store, mutable_mock_repo, tmpdir, monkeypatch, manifest_file
):
    """The user runs 'spack external find'; the default manifest directory
    contains a manifest file. Ensure that the specs are read.
    """
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(spack.cray_manifest, "default_path", str(manifest_file.parent))
    spack.cmd.external._collect_and_consume_cray_manifest_files(ignore_default_dir=False)
    specs = temporary_store.db.query("hwloc")
    assert any(x.dag_hash() == "hwlocfakehashaaa" for x in specs)


def test_reusable_externals_cray_manifest(temporary_store, manifest_file):
    """The concretizer should be able to reuse specs imported from a manifest without a
    externals config entry in packages.yaml"""
    cray_manifest.read(path=str(manifest_file), apply_updates=True)

    # Get any imported spec
    spec = temporary_store.db.query_local()[0]

    # Reusable if imported locally
    assert spack.solver.asp._is_reusable(spec, packages={}, local=True)

    # If cray manifest entries end up in a build cache somehow, they are not reusable
    assert not spack.solver.asp._is_reusable(spec, packages={}, local=False)
