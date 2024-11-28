# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
import os
import traceback
import warnings

import jsonschema
import jsonschema.exceptions

import llnl.util.tty as tty

import spack.cmd
import spack.compilers
import spack.deptypes as dt
import spack.error
import spack.hash_types as hash_types
import spack.platforms
import spack.repo
import spack.spec
import spack.store
from spack.schema.cray_manifest import schema as manifest_schema

#: Cray systems can store a Spack-compatible description of system
#: packages here.
default_path = "/opt/cray/pe/cpe-descriptive-manifest/"

compiler_name_translation = {"nvidia": "nvhpc", "rocm": "rocmcc"}


def translated_compiler_name(manifest_compiler_name):
    """
    When creating a Compiler object, Spack expects a name matching
    one of the classes in `spack.compilers`. Names in the Cray manifest
    may differ; for cases where we know the name refers to a compiler in
    Spack, this function translates it automatically.

    This function will raise an error if there is no recorded translation
    and the name doesn't match a known compiler name.
    """
    if manifest_compiler_name in compiler_name_translation:
        return compiler_name_translation[manifest_compiler_name]
    elif manifest_compiler_name in spack.compilers.supported_compilers():
        return manifest_compiler_name
    else:
        raise spack.compilers.UnknownCompilerError(
            "Manifest parsing - unknown compiler: {0}".format(manifest_compiler_name)
        )


def compiler_from_entry(entry: dict, manifest_path: str):
    # Note that manifest_path is only passed here to compose a
    # useful warning message when paths appear to be missing.
    compiler_name = translated_compiler_name(entry["name"])

    if "prefix" in entry:
        prefix = entry["prefix"]
        paths = dict(
            (lang, os.path.join(prefix, relpath))
            for (lang, relpath) in entry["executables"].items()
        )
    else:
        paths = entry["executables"]

    # Do a check for missing paths. Note that this isn't possible for
    # all compiler entries, since their "paths" might actually be
    # exe names like "cc" that depend on modules being loaded. Cray
    # manifest entries are always paths though.
    missing_paths = []
    for path in paths.values():
        if not os.path.exists(path):
            missing_paths.append(path)

    # to instantiate a compiler class we may need a concrete version:
    version = "={}".format(entry["version"])
    arch = entry["arch"]
    operating_system = arch["os"]
    target = arch["target"]

    compiler_cls = spack.compilers.class_for_compiler_name(compiler_name)
    spec = spack.spec.CompilerSpec(compiler_cls.name, version)
    path_list = [paths.get(x, None) for x in ("cc", "cxx", "f77", "fc")]

    if missing_paths:
        warnings.warn(
            "Manifest entry refers to nonexistent paths:\n\t"
            + "\n\t".join(missing_paths)
            + f"\nfor {str(spec)}"
            + f"\nin {manifest_path}"
            + "\nPlease report this issue"
        )

    return compiler_cls(spec, operating_system, target, path_list)


def spec_from_entry(entry):
    arch_str = ""
    if "arch" in entry:
        local_platform = spack.platforms.host()
        spec_platform = entry["arch"]["platform"]
        # Note that Cray systems are now treated as Linux. Specs
        # in the manifest which specify "cray" as the platform
        # should be registered in the DB as "linux"
        if local_platform.name == "linux" and spec_platform.lower() == "cray":
            spec_platform = "linux"
        arch_format = "arch={platform}-{os}-{target}"
        arch_str = arch_format.format(
            platform=spec_platform,
            os=entry["arch"]["platform_os"],
            target=entry["arch"]["target"]["name"],
        )

    compiler_str = ""
    if "compiler" in entry:
        compiler_format = "%{name}@={version}"
        compiler_str = compiler_format.format(
            name=translated_compiler_name(entry["compiler"]["name"]),
            version=entry["compiler"]["version"],
        )

    spec_format = "{name}@={version} {compiler} {arch}"
    spec_str = spec_format.format(
        name=entry["name"], version=entry["version"], compiler=compiler_str, arch=arch_str
    )

    pkg_cls = spack.repo.PATH.get_pkg_class(entry["name"])

    if "parameters" in entry:
        variant_strs = list()
        for name, value in entry["parameters"].items():
            # TODO: also ensure that the variant value is valid?
            if not pkg_cls.has_variant(name):
                tty.debug(
                    "Omitting variant {0} for entry {1}/{2}".format(
                        name, entry["name"], entry["hash"][:7]
                    )
                )
                continue

            # Value could be a list (of strings), boolean, or string
            if isinstance(value, str):
                variant_strs.append("{0}={1}".format(name, value))
            else:
                try:
                    iter(value)
                    variant_strs.append("{0}={1}".format(name, ",".join(value)))
                    continue
                except TypeError:
                    # Not an iterable
                    pass
                # At this point not a string or collection, check for boolean
                if value in [True, False]:
                    bool_symbol = "+" if value else "~"
                    variant_strs.append("{0}{1}".format(bool_symbol, name))
                else:
                    raise ValueError(
                        "Unexpected value for {0} ({1}): {2}".format(
                            name, str(type(value)), str(value)
                        )
                    )
        spec_str += " " + " ".join(variant_strs)

    (spec,) = spack.cmd.parse_specs(spec_str.split())

    for ht in [hash_types.dag_hash, hash_types.build_hash, hash_types.full_hash]:
        setattr(spec, ht.attr, entry["hash"])

    spec._concrete = True
    spec._hashes_final = True
    spec.external_path = entry["prefix"]
    spec.origin = "external-db"
    spack.spec.Spec.ensure_valid_variants(spec)

    return spec


def entries_to_specs(entries):
    spec_dict = {}
    for entry in entries:
        try:
            spec = spec_from_entry(entry)
            spec_dict[spec._hash] = spec
        except spack.repo.UnknownPackageError:
            tty.debug("Omitting package {0}: no corresponding repo package".format(entry["name"]))
        except spack.error.SpackError:
            raise
        except Exception:
            tty.warn("Could not parse entry: " + str(entry))

    for entry in filter(lambda x: "dependencies" in x, entries):
        dependencies = entry["dependencies"]
        for name, properties in dependencies.items():
            dep_hash = properties["hash"]
            depflag = dt.canonicalize(properties["type"])
            if dep_hash in spec_dict:
                if entry["hash"] not in spec_dict:
                    continue
                parent_spec = spec_dict[entry["hash"]]
                dep_spec = spec_dict[dep_hash]
                parent_spec._add_dependency(dep_spec, depflag=depflag, virtuals=())

    for spec in spec_dict.values():
        spack.spec.reconstruct_virtuals_on_edges(spec)

    return spec_dict


def read(path, apply_updates):
    decode_exception_type = json.decoder.JSONDecodeError
    try:
        with open(path, "r") as json_file:
            json_data = json.load(json_file)

        jsonschema.validate(json_data, manifest_schema)
    except (jsonschema.exceptions.ValidationError, decode_exception_type) as e:
        raise ManifestValidationError("error parsing manifest JSON:", str(e)) from e

    specs = entries_to_specs(json_data["specs"])
    tty.debug("{0}: {1} specs read from manifest".format(path, str(len(specs))))
    compilers = list()
    if "compilers" in json_data:
        compilers.extend(compiler_from_entry(x, path) for x in json_data["compilers"])
    tty.debug("{0}: {1} compilers read from manifest".format(path, str(len(compilers))))
    # Filter out the compilers that already appear in the configuration
    compilers = spack.compilers.select_new_compilers(compilers)
    if apply_updates and compilers:
        for compiler in compilers:
            try:
                spack.compilers.add_compilers_to_config([compiler])
            except Exception:
                warnings.warn(
                    f"Could not add compiler {str(compiler.spec)}: "
                    f"\n\tfrom manifest: {path}"
                    "\nPlease reexecute with 'spack -d' and include the stack trace"
                )
                tty.debug(f"Include this\n{traceback.format_exc()}")
    if apply_updates:
        for spec in specs.values():
            spack.store.STORE.db.add(spec)


class ManifestValidationError(spack.error.SpackError):
    def __init__(self, msg, long_msg=None):
        super().__init__(msg, long_msg)
