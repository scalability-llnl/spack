# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""A Corpus object is used to extract Dwarf and ELF symbols from a library.
We exclude most of the Dwarf Information Entries to expose a reduced set.
Entries can be added as they are needed.
"""

import spack.bootstrap
import sys
import os


class ElftoolsWrapper(object):
    """Create a wrapper to elftools that we can share to expose subfunctions.
    """
    def __init__(self):
        try:
            import elftools # noqa
        except ImportError:
            with spack.bootstrap.ensure_bootstrap_configuration():
                spec = spack.spec.Spec("py-pyelftools@0.27:")
                spec.concretize()
                spack.bootstrap.make_module_available(
                    'elftools', spec=spec, install=True
                )

        from elftools.elf import (
            dynamic, descriptions, sections, gnuversions, elffile, constants)
        from elftools.dwarf import descriptions as dwarf
        from elftools.dwarf import locationlists as locationlists
        from elftools.common import py3compat as py3compat
        from elftools.common import exceptions as exceptions
        self.dynamic = dynamic
        self.descriptions = descriptions
        self.sections = sections
        self.gnuversions = gnuversions
        self.elffile = elffile
        self.constants = constants
        self.dwarf = dwarf
        self.locationlists = locationlists
        self.py3compat = py3compat
        self.exceptions = exceptions


et = ElftoolsWrapper()


class CorpusReader(et.elffile.ELFFile):  # noqa
    """
    A CorpusReader wraps an elffile.

    This allows us to easily open/close and keep the stream open while we are
    interacting with content. We close the file handle on any exit.
    """

    def __init__(self, filename):
        self.fd = open(filename, "rb")
        self.filename = filename
        try:
            self.elffile = et.elffile.ELFFile(self.fd)
        except Exception:
            sys.exit("%s is not an ELF file." % filename)

        # Cannot continue without dwarf info
        if not self.elffile.has_dwarf_info():
            sys.exit("%s is missing DWARF info." % self.filename)
        self.get_version_lookup()
        self.get_shndx_sections()

    def __str__(self):
        return "[CorpusReader:%s]" % self.filename

    def __repr__(self):
        return str(self)

    @property
    def header(self):
        return dict(self.elffile.header)

    def __exit__(self):
        print("Closing reader")
        self.fd.close()

    def get_architecture(self):
        return self.elffile.header.get("e_machine")

    def get_elf_class(self):
        return self.elffile.elfclass

    def get_version_lookup(self):
        """Get versioning used (GNU or Solaris)
        https://github.com/eliben/pyelftools/blob/master/scripts/readelf.py#L915
        """
        lookup = dict()
        types = {
            et.gnuversions.GNUVerSymSection: "versym",
            et.gnuversions.GNUVerDefSection: "verdef",
            et.gnuversions.GNUVerNeedSection: "verneed",
            et.dynamic.DynamicSection: "type",
        }

        for section in self.elffile.iter_sections():
            if type(section) in types:
                identifier = types[type(section)]
                if identifier == "type":
                    for tag in section.iter_tags():
                        if tag["d_tag"] == "DT_VERSYM":
                            lookup["type"] = "GNU"
                else:
                    lookup[identifier] = section

        # If we don't have a type but we have verneed or verdef, it's solaris
        if not lookup.get("type") and (lookup.get("verneed") or lookup.get("verdef")):
            lookup["type"] = "Solaris"
        self._versions = lookup

    def get_shndx_sections(self):
        """I think this referes to section index/indices. We want a mapping
        from a symbol table index to a corresponding section object. The
        SymbolTableIndexSection was added in pyelftools 0.27.
        """
        self._shndx_sections = {}
        for x in self.elffile.iter_sections():
            if isinstance(x, et.sections.SymbolTableIndexSection):
                self._shndx_sections[x.symboltable] = x

    def get_symbols(self):
        """Return a set of symbols from the dwarf symbol tables"""
        symbols = {}

        # We want .symtab and .dynsym
        tables = [
            (idx, s)
            for idx, s in enumerate(self.elffile.iter_sections())
            if isinstance(s, et.sections.SymbolTableSection)
        ]

        for idx, section in tables:
            # Symbol table has no entries if this is zero
            # section.num_symbols() shows count, section.name is name
            if section["sh_entsize"] == 0:
                continue

            # We need the index of the symbol to look up versions
            for sym_idx, symbol in enumerate(section.iter_symbols()):

                # Version info is from the versym / verneed / verdef sections.
                version_info = self._get_symbol_version(section, sym_idx, symbol)

                # Symbol Type
                symbol_type = et.descriptions.describe_symbol_type(
                    symbol["st_info"]["type"])

                # Symbol Binding
                binding = et.descriptions.describe_symbol_bind(
                    symbol["st_info"]["bind"])

                # Symbol Visibility
                visibility = et.descriptions.describe_symbol_visibility(
                    symbol["st_other"]["visibility"])

                # We aren't considering st_value, which could be many things
                # https://docs.oracle.com/cd/E19683-01/816-1386/6m7qcoblj/index.html#chapter6-35166
                symbols[symbol.name] = {
                    "version_info": version_info,
                    "type": symbol_type,
                    "binding": binding,
                    "visibility": visibility,
                    "defined": et.descriptions.describe_symbol_shndx(
                        self._get_symbol_shndx(symbol, sym_idx, idx)
                    ).strip(),
                }

        return symbols

    def _get_symbol_version(self, section, sym_idx, symbol):
        """
        Given a section, symbol index, and symbol, return version info.

        https://github.com/eliben/pyelftools/blob/master/scripts/readelf.py#L400
        """
        version_info = ""

        # I'm not sure why this would be empty
        if not self._versions:
            return version_info

        # readelf doesn't display version info for Solaris versioning
        if section["sh_type"] == "SHT_DYNSYM" and self._versions["type"] == "GNU":
            version = self._symbol_version(sym_idx)
            if version["name"] != symbol.name and version["index"] not in (
                "VER_NDX_LOCAL",
                "VER_NDX_GLOBAL",
            ):

                # This is an external symbol
                if version["filename"]:
                    version_info = "@%(name)s (%(index)i)" % version

                # This is an internal symbol
                elif version["hidden"]:
                    version_info = "@%(name)s" % version
                else:
                    version_info = "@@%(name)s" % version
        return version_info

    def _symbol_version(self, idx):
        """We can get version information for a symbol based on it's index
        https://github.com/eliben/pyelftools/blob/master/scripts/readelf.py#L942
        """
        symbol_version = dict.fromkeys(("index", "name", "filename", "hidden"))

        # No version information available
        if (
            not self._versions.get("versym")
            or idx >= self._versions.get("versym").num_symbols()
        ):
            return None

        symbol = self._versions["versym"].get_symbol(idx)
        index = symbol.entry["ndx"]
        if index not in ("VER_NDX_LOCAL", "VER_NDX_GLOBAL"):
            index = int(index)

            # GNU versioning means highest bit is used to store symbol visibility
            if self._versions["type"] == "GNU":
                if index & 0x8000:
                    index &= ~0x8000
                    symbol_version["hidden"] = True

            if (
                self._versions.get("verdef")
                and index <= self._versions["verdef"].num_versions()
            ):
                _, verdaux_iter = self._versions["verdef"].get_version(index)
                symbol_version["name"] = next(verdaux_iter).name
            else:
                verneed, vernaux = self._versions["verneed"].get_version(index)
                symbol_version["name"] = vernaux.name
                symbol_version["filename"] = verneed.name

        symbol_version["index"] = index
        return symbol_version

    def _get_symbol_shndx(self, symbol, symbol_index, symtab_index):
        """Every symbol table entry is defined in relation to some section.
        The st_shndx of a symbol holds the relevant section header table index.
        https://github.com/eliben/pyelftools/blob/master/scripts/readelf.py#L994
        """
        if symbol["st_shndx"] != et.constants.SHN_INDICES.SHN_XINDEX:
            return symbol["st_shndx"]

        # Check for or lazily construct index section mapping (symbol table
        # index -> corresponding symbol table index section object)
        if self._shndx_sections is None:
            self._shndx_sections = {}
            for sec in self.elffile.iter_sections():
                if isinstance(sec, et.sections.SymbolTableIndexSection):
                    self._shndx_sections[sec.symboltable] = sec
        return self._shndx_sections[symtab_index].get_section_index(symbol_index)

    def get_dynamic_tags(self):
        """Get the dyamic tags in the ELF file."""
        tags = {}
        for section in self.elffile.iter_sections():
            if not isinstance(section, et.dynamic.DynamicSection):
                continue

            # We are interested in architecture, soname, and needed
            def add_tag(section, tag):
                if section not in tags:
                    tags[section] = []
                tags[section].append(tag)

            for tag in section.iter_tags():
                if tag.entry.d_tag == "DT_NEEDED":
                    add_tag("needed", tag.needed)
                elif tag.entry.d_tag == "DT_RPATH":
                    add_tag("rpath", tag.rpath)
                elif tag.entry.d_tag == "DT_RUNPATH":
                    add_tag("runpath", tag.runpath)
                elif tag.entry.d_tag == "DT_SONAME":
                    tags["soname"] = tag.soname

            return tags

    def _iter_dwarf_information_entries(self):
        dwarfinfo = self.elffile.get_dwarf_info()

        # A CU is a Compilation Unit
        for cu in dwarfinfo.iter_CUs():

            # A DIE is a dwarf information entry
            for die in cu.iter_DIEs():
                yield die

    def iter_dwarf_information_entries(self):
        for die in self._iter_dwarf_information_entries():
            yield die


class Corpus:
    """
    Generate an ABi corpus.

    A Corpus is an ELF file header combined with complete elf symbols,
    variables, and nested Dwarf Information Entries
    """

    def __init__(self, filename, name=None, uid=None):

        filename = os.path.abspath(filename)
        if not os.path.exists(filename):
            sys.exit("%s does not exist." % filename)

        self.elfheader = {}
        self.name = name
        self.uid = uid

        self.elfsymbols = {}
        self.path = filename
        self.basename = os.path.basename(filename)
        self.dynamic_tags = {}
        self.architecture = None
        self._soname = None
        self.read_elf_corpus()

    def __str__(self):
        return "[Corpus:%s]" % self.path

    def __repr__(self):
        return str(self)

    def exists(self):
        return self.path is not None and os.path.exists(self.path)

    @property
    def soname(self):
        return self.dynamic_tags.get("soname")

    @property
    def needed(self):
        return self.dynamic_tags.get("needed", [])

    @property
    def runpath(self):
        return self.dynamic_tags.get("runpath")

    @property
    def rpath(self):
        return self.dynamic_tags.get("rpath")

    def iter_dwarf_information_entries(self):
        """Return flattened list of DIEs (Dwarf Information Entrys)"""
        reader = CorpusReader(self.path)
        for entry in reader.iter_dwarf_information_entries():
            yield entry

    def read_elf_corpus(self):
        """
        Read the entire elf corpus, including dynamic and other sections.
        """
        reader = CorpusReader(self.path)

        # Read in the header section as part of the corpus
        self.elfheader = reader.header

        # Read in dynamic tags, and symbols
        self.dynamic_tags = reader.get_dynamic_tags()
        self.architecture = reader.get_architecture()
        self.elfclass = reader.get_elf_class()
        self.elfsymbols = reader.get_symbols()
