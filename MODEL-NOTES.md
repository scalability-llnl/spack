# Type / Location Model Notes

This is what I'm currently doing. Please yell at me if something is wrong!
There are a lot of details and I want to get them down here so you can also
look them over carefully and give feedback. You can also just look at the modified
asp.py in the pull request for the "code documentation" version. :)

## 1. Get corpora

The user is going to run a command that asks to run an analyzer for a specific
package. E.g., "tcl" (pronounced "tickle.")

```bash
$ spack analyze run -a abi_type_location tcl
```

Importantly, this package along with its dependencies needs to be built
with debug.

```bash
$ spack install tcl+debug ^zlib+debug
```

We can then get a build manifest for the tcl spec, and create Corpora, or
general classes that wrap an elffile, for each entry in the manifest
`binary_to_relocate_fullpath`. These entries are labeled as main corpora,
meaning directionality (e.g., import vs. export) we define in context to them,
and we generate a few extra rules to declare them as main corpora.
We then loop through the main spec dependencies, and get the same manifest
and key to add (potential) supporting libraries. These are not labeled as 
main corpora, and the directionality (discussed later) is reversed.

## 2. Get system corpora

For each corpora (a library file) we use ldd on the library file to get
a list of additional (system typically) libraries that we want to parse.
We use "which" to get the fullpath, and only add the new corpus if
the path is not already represented by another corpus.

## 3. Set needed symbols

We only care about a symbol if it's defined in one of our main corpora, so
we create a lookup of needed symbols (by symbol name)
that constitutes any symbol in a main corpus. We will not add symbol facts
from dependency libraries that are not found in a main corpus. We don't
care about what specific main library the symbol comes from - if it's found
in any main library it's flagged as needed.

## 4. Create symbol lookup

We aren't actually going to parse through the list of main symbols directly,
but rather the Dwarf Information Entries (DIEs) that the main corpora have,
and then we will add information for a symbol only if it's represented in a DIE.
To make this easy, we create a symbol lookup, where we can quickly
check if some needed symbol is defined for a corpus. It's a set for easy
lookup:

```python
for corpus in corpora:
   self.symbols[corpus.basename] = set()
   for symbol, _ in corpus.elfsymbols.items():
        self.symbols[corpus.basename].add(symbol)
```

And then later we can easily see if it's defined for a specific corpus,
and if so, retrieve it directly from the `corpus.elfsymbols`. This
is just an implementation detail.

## 5. Generate corpus metadata

For each corpus, we generate basic metadata like it's name, path, and whether
it's a main corpus. E.g.,

```asp
corpus("tclsh8.6").
is_main_corpus("tcl","8.6.11").
corpus_machine("tcl","EM_X86_64").
```

## 6. Define logic to get register based on type

This will need work, but we have a function that can take a die type,
and based on the type, return the register that it is found in. Below,
you'll see that we parse over a parent die's children in order to determine
the order of parameters. When we hit a parent function for the first time,
we generate a cache of child parameter orders (so we only do it once).

```python
def get_parameter_register(self, die, corpus, die_type):
    """
    Given the order and type of formal parameter, return the register

    We cache the order of the children for lookup by later parameter calls.
    """
    # We first have to derive the order from the parent children
    # If we do it for the first time, cache it
    parent = die.get_parent()
    parent_id = self._die_hash(parent, corpus)

    # If we haven't seen it yet, create a lookup
    if parent_id not in self.child_lookup[corpus.basename]:
        self.child_lookup[corpus.basename][parent_id] = {}
        order = 1
        for child in parent.iter_children():

            # Don't include children that are not formal parameters
            if "formal_parameter" not in child.tag:
                continue
            child_id = self._die_hash(child, corpus)
            self.child_lookup[corpus.basename][parent_id][child_id] = order
            order += 1

    # Retrieve the parameter order we need (this is one of the children)
    die_id = self._die_hash(die, corpus)
    order = self.child_lookup[corpus.basename][parent_id][die_id]

    # Signed and unsigned Bool,char,short,int,long,long long, and pointers
    INTEGER = False
    if re.search("(int|char|short|long|pointer|bool)", die_type):
        INTEGER = True

    # float,double,_Decimal32,_Decimal64and__m64are in class SSE.
    SSE = ['double', 'decimal']

    if INTEGER and order == 1:
        return "%rdi"

    elif INTEGER and order == 2:
        return "%rsi"

    elif INTEGER and order == 3:
        return "%rdx"

    elif INTEGER and order == 4:
        return "%rcx"

    elif INTEGER and order == 5:
        return "%r8"

    elif INTEGER and order == 6:
        return "%r9"

    # I think constants are stored on the stack?
    elif die_type == "const":
        return "stack"

    # This could be stack too, or the above memory
    elif INTEGER and order > 6:
        return "memory"

    elif die_type in SSE and order <= 8:
        return "%xmm" + str(order - 1)
```

## 7. Iterate over DIEs

Now we can iterate over DIEs, and for each, we:

### Base of Model is Name, Type, Location

For any DIE we can match to a symbol, we attempt to define a name, location,
and die type.

```python
# We want to represent things as names, locations, and types
name = None
loc = None
die_type = None
```

### Check for a name

We can only match to a symbol if the DIE has a `DW_AT_name` or `DW_AT_linkage_name`
(the mangled string) attribute. We check for the mangled string first. If the DIE
does not have a name, we skip it because we cannot match to a needed symbol.
If the name is present but not in the needed symbols lookup, we also skip it.
We don't care about symbols that a main corpora does not use.


### Get an export status

We want to generally say if a variable, function, member, or parameter is exported
or imported, which is a term relative to our main corpora. This means that:

 1. If we have a main corpus and it has a `DW_AT_external` flag, it's an "export"
 2. If it's not a main corpus and it has a `DW_AT_external` flag, it's an "import"
 3. If we have a main corpus and it's a formal parameter type, it's an "import"
 4. If it's the main corpus and a variable or member, it's exported (not sure about this one)
 5. If it's not the main corpus and it's a variable or member, it's imported (not sure about this one)
 6. If it's the main corpus and it's a function (return) it's exported
 7. If it's not the main corpus and it's a function (return) it's imported
 8. If it's a main corpus (anything else) we label "unknown-export"
 9. If it's not a main corpus and anything else, we also label "unknown-export"

This is one of the variables that is added to an abi_typelocation fact.


### Add symbol metadata

At this point, if we've found a name and the name is in needed symbols,
we can generate metadata for the symbol. This typically looks like:

```asp
has_symbol("libtcl8.6.so","free").
symbol_type("libtcl8.6.so","free","FUNC").
symbol_binding("libtcl8.6.so","free","GLOBAL").
symbol_definition("libtcl8.6.so","free","UND").
```

We are interested in symbols that are needed that are undefined (UND above).

### Get type and location

We then look for `DW_AT_type` and `DW_AT_location` to get a location (which can
be multiple if a location list is found, they will be separated by commas in a string)
and a type.

```python
if "DW_AT_type" in die.attributes:
    die_type = self._get_die_type(die)

if "DW_AT_location" in die.attributes:
    loc = self.get_location(die)
```

Getting the die type (I think) is done fairly reasonably - I was hitting an error where an
address was outside of a CU unit, but I read that I just need to add the CU offset
(and then I get an answer). 

```python
# DWARFError: refaddr 48991 not in DIE range of CU 66699
# https://github.com/eliben/pyelftools/blob/master/elftools/dwarf/compileunit.py#L113
# When using a reference class attribute with a form that is
# relative to the compile unit, add unit add the compile unit's
# .cu_addr before calling this function.
except et.exceptions.DWARFError:
    type_die = query_die.cu.get_DIE_from_refaddr(
    query_die.attributes["DW_AT_type"].value + query_die.cu.cu_offset
)
```

In my dummy case I haven't yet seen any `DW_AT_type` that have a ref address
which means an absolute offset.

```python
# Absolute offset
elif query_die.attributes["DW_AT_type"].startswith("DW_FORM_ref_addr")
```

Given that we have a type_die (derived from an address we either need to):

1. recursively call the function if that thing still has a `DW_AT_type` attribute
2. If the type_die tag is `DW_TAG_const_type` I return "const" as the string of the type
3. same with structure or pointer for `DW_TAG_structure_type` and `DW_TAG_pointer_type`
4. otherwise I get the type name again from `DW_AT_linkage_type` or `DW_AT_name`.


Note that I'm using cu.cu_offset instead of cu.cu_die_offset (which from the
comments above I think is the one I want?)

### Skip structures

I think structures are represented by their guts? So for now we skip
them, meaning tags `structure` and `structure_type`. We do this by checking if `die_type` 
one of these strings. In practice structures don't have a known export status 
nor do they have a die_type.

### Get a parent

If we have a formal parameter, we are going to want to say what function it is
from, and the function (`DW_TAG_subprogram`) is the parent that we need to parse.
So we always derive the name of a parent, which can be a function, but for
variables (and maybe members?) it's a filename, which we don't care about.


### Generate facts

For fact generation, the structure depends on what we found (e.g., sometimes
we don't have a location). I think this could probably be simplified a lot -
the cases of what we should find aren't totally clear to me.

### Generate interfaces

Functions are always labeled as interfaces.

```asp
# tag, corpus basename, name, export status
interface("function","libtcl8.6.so","compact","export").
```

Likely there are other tag types we want to call interfaces too?
The next facts are all related to abi_typelocation.

#### Case 1: we have a parent, loc, name, and die_type

If we have everything, this typically is a formal parameter (and we check too,
since we are going to look up a register). We additionally
derive the register name with the function we described in #6. We generate
a location fact with:

```python
# tag corpus.basename, parent name, name, export status, die_type, register, loc
abi_typelocation("formal_parameter","libtcl8.6.so","TclNREvalObjEx","word","import","int","%r8","(DW_OP_fbreg: -184)").
```

We are including the tag for now so it's easier to debug the facts (e.g.,
see what DIE tag generated each). I'm not sure if a formal_parameter can ever
not have a loc - if this is the case, the loc will show up as None.

#### Case 3: A variable with a type and loc

If we have a variable, we don't care about it's parent name, but
we do care about it's location and die type.

```python
# tag, corpus.basename, name, exported, die_type, loc
abi_typelocation("variable","libtcl8.6.so","backd","export","short unsigned int","(DW_OP_addr: 204320)").
```

#### Case 4: We have all attributes, but it's not a formal parameter

```python
tag, corpus.basename, pname, name, exported, die_type, loc)
```

This is sort of a catch all for #4, except we know it's not a variable (so we try
including the parent name, pname). I'm not sure if this is ever used.

#### Case 5: just die_type and loc

I'm again not sure if we ever hit this case. Maybe this would trigger for
a variable?

```python
# tag, corpus.basename, name, exported, die_type, loc
```

#### Case 6: A function with a die_type is a return type

```python
# tag, cname, name, exported, die_type, "%rax")
abi_typelocation("function","libtcl8.6.so","casecmp","export","int","%rax").
```

#### Case 7: Catch all

If we don't hit a case above, we generate the abi_typelocation fact
and just include everything that might be there. In practice this does not
include loc, and it looks like we hit members and variables.

```python
# tag, cname, name, exported, die_type)
abi_typelocation("member","libtcl8.6.so","free","export","short int").
abi_typelocation("variable","libtcl8.6.so","tclPlatform","export","unsigned int").
```
