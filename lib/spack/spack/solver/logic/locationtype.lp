%==============================================================================
% The location type compatitiblity model looks at elf symbols, types, locations
%==============================================================================

%=============================================================================
% Matching function and variable symbols
% symbols are missing if they are needed (present in the working library),
% not undefined in the working library (indicating they come from elsewhere)
% and undefined in both the potential library and binary.
%=============================================================================

% These are symbols to skip checking (profiling and other)
skip_symbol("_ITM_deregisterTMCloneTable").
skip_symbol("__gmon_start__").
skip_symbol("_ITM_registerTMCloneTable").

%----------------------------------------------------------------------------
% Corpus symbols: libtcl8.6.so
%----------------------------------------------------------------------------

% model 1: base (spack solver)
% model 2: symbols
% model 3: libabigail
% model 4: type/location model "code centric model"
% model 5: inlined code "data centric model" 

% something is a symbol if any binary has it
symbol :- has_symbol(_, Symbol).

% a package corpus needs a symbol if:
needs_symbol(Package, Version, Symbol, Corpus)

    % it's not one flagged to skip
    :- not skip_symbol(Symbol),

    % the corpus has it
    corpus(Package, Version, Corpus),

    % the corpus has the symbol
    has_symbol(Corpus, Symbol).


% A symbol is undefined for a package and corpus
% (a corpus is a binary/library provided by the package) if:
undefined_symbol(Package, Version, Symbol, Corpus)

    % the package needs the symbol
    :- needs_symbol(Package, Version, Symbol, Corpus),

    % and it's definition is UND
    symbol_definition(Corpus, Symbol, "UND").


% a symbol is undefined for a package version if
undefined_symbol(Package, Version, Symbol) 

    % it's undefined in any corpora
    :- undefined_symbol(Package, Version, Symbol, _).


% A symbol is defined for a package version if:
defined_symbol(Package, Version, Symbol, Corpus, Definition)

    % the package needs the symbol
    :- needs_symbol(Package, Version, Symbol, Corpus),

    % the corpus has a symbol definition
    symbol_definition(Corpus, Symbol, Definition),

    % and definition != UND
    Definition != "UND".

% A symbol is defined for a package verison across all corpora if
defined_symbol(Package, Version, Symbol)

    % it's defined for any corpora
    :- defined_symbol(Package, Version, Symbol, _, _).


% a package and dependency are linkable if
linkable(Package, Dependency)

    % The package and dependency are nodes in the graph
    :- node(Package),
    node(Dependency),

    % And the dependency holds
    dependency_holds(Package, Dependency, _).

% base rule for incompatible
incompatible_base(Package, V1, Dependency, V2)

    % they are linkable
    :- linkable(Package, Dependency),

    % The package and dependency each have their own version
    version(Package, V1),
    version(Dependency, V2).


% A package and dependency are incompatible if:
incompatible(Package, V1, Dependency, V2)

    :- incompatible_base(Package, V1, Dependency, V2),

    % The package has an undefined symbol
    undefined_symbol(Package, V1, Symbol),

    % the package depends on the dependency
    depends_on(Package, Dependency),

    % and the symbol is not defined for the dependency
    not defined_symbol(Dependency, V2, Symbol).


% incompatible if matching variables are different types
% abi_typelocation("variable","libtcl8.6.so","environ","export","char").
incompatible(Package, V1, Corpus1, Type1, Dependency, V2, Corpus2, Variable, Type2, VariableType)

    :- incompatible_base(Package, V1, Dependency, V2),

    % it's a variable needed (imported) by Corpus1
    abi_typelocation(VariableType, Corpus1, Variable, "import", Type1),

    % it's exported by Corpus 2
    abi_typelocation(VariableType, Corpus2, Variable, "export", Type2),

    % but the type is wrong
    Type1 != Type2.   

% flatten into the rule that fits into solver
incompatible(Package, V1, Dependency, V2)

    % we don't care about the corpus, variable name, or type
    :- incompatible(Package, V1, _, _, Dependency, V2, _, _, _, _).

% abi_typelocation("variable","libtcl8.6.so","graphCharTable","export","short unsigned int","(DW_OP_addr: 206660)").

% Not sure how to compare the last variables
% abi_typelocation("function","libtcl8.6.so","carc_cmp","export","int","%rax").
% incompatile if their locations are off
%incompatible(Package, V1, Corpus1, Type1, Dependency, V2, Corpus2, Variable, Type2, VariableType)

%    :- incompatible_base(Package, V1, Dependency, V2),

    % it's a variable needed (imported) by Corpus1
%    abi_typelocation(VariableType, Corpus1, Variable, "import", Type1),

    % it's exported by Corpus 2
%    abi_typelocation(VariableType, Corpus2, Variable, "export", Type2),

    % but the type is wrong
%    Type1 != Type2.   


#show incompatible/4.
