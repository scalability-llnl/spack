# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class VepCache(Package):
    """Separate installation and management for the Ensembl Variant Effect Predictor (vep)"""

    homepage = "https://useast.ensembl.org/info/docs/tools/vep/index.html"
    maintainers("teaguesterling")
    # This is a dummy value to get spack to resolve resources, which are not downloaded
    # when has_code = False
    has_code = False

    license("Apache-2.0", checked_by="teaguesterling")

    vep_versions = ["112", "111", "110"]
    depends_on("vep", type="build")
    for major in vep_versions:
        version(major)
        depends_on(f"vep@{major}", type="build", when=f"@{major}+match_vep_version")

    vep_assembly_sources = ["ensembl", "refseq", "merged"]

    # This is an incomplete list
    vep_species = {
        "bos_taurus": ["UMD3.1"],
        "danio_rerio": ["GRCz11"],
        "homo_sapiens": ["GRCh38", "GRCh37"],
        "mus_musculus": ["GRCm38"],
        "rattus_norvegicus": ["Rnor_6.0"],
    }

    variant("match_vep_version", default=True, description="Match cache and software version")
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
        values=vep_species.keys(),
        default="homo_sapiens",
        description="Which species to download the cache for (only one at a time)",
    )
    variant(
        "assembly",
        values=["latest"]
        + [
            conditional(*assemblies, when=f"species={species}")
            for species, assemblies in vep_species.items()
        ],
        default="latest",
        multi=False,
        description="Which assembly of genome to use (only needed for homo sapiens)",
    )

    def cache_from_spec(self, spec):
        variants = spec.variants
        indexed = spec.satisfies("+indexed")
        cache_type = variants["assembly_source"].value
        species = variants["species"].value
        assembly = variants["assembly"].value
        assembly = self.vep_species[species][0] if assembly == "latest" else assembly
        return indexed, cache_type, species, assembly

    def vep_cache_config(self, base):
        spec = self.spec
        cache_version = spec.version.up_to(1)
        indexed, cache_type, species, assembly = self.cache_from_spec(spec)
        user_root = join_path(base, "share", "vep")
        root = user_root  # Should this be VEP install dir?

        suffix = "" if cache_type == "ensembl" else f"_{cache_type}"
        species_cache = f"{species}{suffix}"

        if species == "homo_sapiens":
            cache_dir = join_path(species, f"{cache_version}_{assembly}")
        else:
            cache_dir = join_path(species, f"{cache_version}")

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
        if cache["species"] == "homo_sapiens":
            args += ["--ASSEMBLY", cache["assembly"]]

        return args

    def installer_args(self):
        auto = "cf" if self.spec.satisfies("+fasta") else "c"
        args = ["--AUTO", auto, "--NO_UPDATE", "--NO_TEST"]
        args += self.cache_installer_args()
        return args

    def install_with_installer(self):
        vep = self.spec["vep"].package
        installer = which(vep.vep_installer_path)
        installer(*self.installer_args())

    def install(self, spec, prefix):
        cache = self.vep_cache_config(self.prefix)
        mkdirp(cache["full_path"])
        self.install_with_installer()
