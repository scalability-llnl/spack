%==============================================================================
% The "no-op" abi_compatible model always returns true.
%==============================================================================

abi_compatible(Package) :- depends_on(Package, _).
