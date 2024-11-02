# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import itertools

from spack.package import *


def _vep_cache_filename(version, species, source, assembly):
    assembly_source = "vep" if source == "ensembl" else f"{source}_vep"
    return f"{species}_{assembly_source}_{version}_{assembly}.tar.gz"


def _vep_cache_resource_kwargs(version, species, source, assembly, indexed, dest=None):
    filename = _vep_cache_filename(version, species, source, assembly)
    dir_name = "indexed_vep_cache" if indexed else "vep"
    root = f"https://ftp.ensembl.org/pub/release-{version}/variation/{dir_name}"
    url = join_path(root, filename)
    when = [
        f"@{version}",
        "~use_vep_installer",  # Only need these resources when we don't use the installer
        "+indexed" if indexed else "~indexed",  # Only need the appropriate indexed versiona
        f"assembly_source={source}",  # Only reference the assembly source defined here
        f"species={species}",  # Only need the requested species
        # We only need to match the specified assembly for human assemblies
        f"assembly={assembly.lower()}" if species == "homo_sapiens" else "",
    ]
    dest = filename if dest is None else dest

    kwargs = {
        "name": filename,
        "url": url,
        "when": " ".join(when),
        "destination": dest,
        "expand": False,  # We'll expand this where it needs to go later
    }

    return kwargs


class VepCache(Package):
    """Separate installation and management for the Ensembl Variant Effect Predictor (vep)"""

    homepage = "https://useast.ensembl.org/info/docs/tools/vep/index.html"
    maintainers("teaguesterling")
    # This is a dummy value to get spack to resolve resources, which are not downloaded
    # when has_code = False
    url = "https://raw.githubusercontent.com/Ensembl/ensembl-vep/release/112/INSTALL.pl"

    license("Apache-2.0", checked_by="teaguesterling")

    # The cache *should* be pinned to the VEP version, but there are reasons
    # that one may want to avoid that
    vep_versions = ["110", "111", "112"]
    vep_assembly_sources = ["ensembl", "refseq", "merged"]
    # This is an incomplete list
    vep_species = [
        ("bos_taurus", ["UMD3.1"]),
        ("danio_rerio", ["GRCz11"]),
        ("homo_sapiens", ["GRCh37", "GRCh38"]),
        ("mus_musculus", ["GRCm38"]),
        ("rattus_norvegicus", ["Rnor_6.0"]),
    ]
    # We only need to (and only can) specify an assembly for humans
    vep_assembly_choices = [
        assembly
        for species, assemblies in vep_species
        for assembly in assemblies
        if species == "homo_sapiens"
    ]

    variant("use_vep_installer", default=False, description="Use VEP installer script to download")
    variant("env", default=True, description="Setup VEP environment variables for this cache")

    # Cache configuration options
    variant("fasta", default=True, description="Add FASTA files to the cache")
    variant("indexed", default=True, description="Use indexed cache")

    variant(
        "assembly_source",
        values=vep_assembly_sources,
        default="ensembl",
        description="What reference genome source",
    )
    variant(
        "species",
        values=[species for species, _ in vep_species],
        default="homo_sapiens",
        description="Which species to download the cache for (only one at a time)",
    )
    variant(
        "assembly",
        values=[assembly.lower() for assembly in vep_assembly_choices],
        default="grch38",
        when="species=homo_sapiens",
        description="Which assembly of genome to use (only needed for homo sapiens)",
    )

    # Add all species for each VEP version
    for major, source, indexed, (species, assemblies) in itertools.product(
        vep_versions,  # All VEP versions
        vep_assembly_sources,  # The three VEP assembly sources
        [True, False],  # Indexed or not
        vep_species,  # All species with caches defined
    ):
        # A possibility of more than one assembly, even though most only have one
        for assembly in assemblies:
            version(major, expand=False)
            resource(**_vep_cache_resource_kwargs(
                version=major, species=species, source=source, assembly=assembly, indexed=indexed
            ))

    depends_on("vep", type="build")

    @property
    def vep(self):
        return self.spec["vep"].package

    def vep_cache_config(self, base):
        spec = self.spec
        satisfies = spec.satisfies
        variants = spec.variants
        cache_version = spec.version.up_to(1)
        vep_version = self.vep.version.up_to(1)
        user_root = join_path(base, "share", "vep")
        root = user_root  # Should this be VEP install dir?

        if cache_version == "default":
            cache_version = vep_version

        indexed = satisfies("+indexed")
        cache_type = variants["assembly_source"].value
        species_name = variants["species"].value
        assembly_name = variants["assembly"].value

        species = f"{species_name}"
        suffix = "" if cache_type == "ensembl" else f"_{cache_type}"
        species_cache = f"{species_name}{suffix}"

        if "homo_sapiens" in species_name:
            assembly = assembly_name.replace("grch", "GRCh")
            cache_dir = join_path(species, f"{vep_version}_{assembly}")
        else:
            for check_species, assemblies in self.vep_species:
                if species == check_species:
                    assembly = assemblies[0]
                    break
            else:
                assembly = ""
            cache_dir = join_path(species, f"{vep_version}")

        return {
            "root": root,
            "user_root": user_root,
            "version": f"{cache_version}",
            "type": f"{cache_type}",
            "species": species,
            "cache_species": species_cache,
            "assembly": f"{assembly}",
            "indexed": indexed,
            "dir": cache_dir,
            "full_path": join_path(root, cache_dir),
        }

    def url_for_version(self, version):
        major = version.up_to(1)
        url = f"https://raw.githubusercontent.com/Ensembl/ensembl-vep/release/{major}/INSTALL.pl"
        vep = Spec(f"vep+installer@{major}")
        return vep.package.vep_installer_path if vep.installed else url

    def setup_run_environment(self, env):
        if self.spec.satisfies("+env"):
            cache = self.vep_cache_config(self.home)
            env.set("VEP_OFFLINE", "1")
            env.set("VEP_CACHE", "1")
            env.set("VEP_DIR", cache["user_root"])
            env.set("VEP_SPECIES", cache["species"])
            env.set("VEP_CACHE_VERSION", cache["version"])
            if cache["assembly"] is not None:
                env.set("VEP_ASSEMBLY", cache["assembly"])
            if cache["type"] == "refseq":
                env.set("VEP_REFSEQ", "1")
            if cache["type"] == "merged":
                env.set("VEP_MERGED", "1")
            if self.spec.satisfies("+fasta"):
                pass

    def cache_installer_args(self):
        cache = self.vep_cache_config(self.prefix)
        args = [
            "--CACHEDIR",
            cache["full_path"],
            "--CACHE_VERSION",
            cache["version"],
            "--SPECIES",
            cache["cache_species"],
        ]
        if cache["assembly"] is not None:
            args += ["--ASSEMBLY", cache["assembly"]]

        return args

    def installer_args(self):
        auto = "cf" if self.spec.satisfies("+fasta") else "c"
        args = ["--AUTO", auto, "--NO_UPDATE", "--NO_TEST"]
        args += self.cache_installer_args()
        return args

    def install_with_installer(self):
        installer = which(self.vep.vep_installer_path)
        installer(*self.installer_args())

    def install(self, spec, prefix):
        cache = self.vep_cache_config(self.prefix)
        mkdirp(cache["full_path"])
        if spec.satisfies("+use_vep_installer"):
            self.install_with_installer()
        else:
            tarball = _vep_cache_filename(
                version=cache["version"], 
                species=cache["species"], 
                assembly=cache["assembly"], 
                source=cache["type"],
            )
            tar = which("tar")
            tar("xzvf", tarball, "-C", cache["root"])
