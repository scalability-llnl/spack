% Copyright Spack Project Developers. See COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% Libc compatibility rules for reusing solves.
%
% These rules are used on Linux
%=============================================================================


% A package cannot be reused if it needs a libc that is not compatible with the current one
error(100, "Cannot reuse {0} since we cannot determine libc compatibility", ReusedPackage)
  :- provider(node(X, LibcPackage), node(0, "libc")),
     attr("version", node(X, LibcPackage), LibcVersion),
     concrete(node(R, ReusedPackage)),
     attr("needs_libc", node(R, ReusedPackage)),
     not attr("compatible_libc", node(R, ReusedPackage), LibcPackage, LibcVersion).

% In case we don't need a provider for libc, ensure there's at least one compatible libc on the host
error(100, "Cannot reuse {0} since we cannot determine libc compatibility", ReusedPackage)
  :- not provider(_, node(0, "libc")),
     concrete(node(R, ReusedPackage)),
     attr("needs_libc", node(R, ReusedPackage)),
     not attr("compatible_libc", node(R, ReusedPackage), _, _).

% Non-libc reused specs must be host libc compatible. In case we build packages, we get a
% host compatible libc provider from other rules. If nothing is built, there is no libc provider,
% since it's pruned from reusable specs, meaning we have to explicitly impose reused specs are host
% compatible.
%:- attr("hash", node(R, ReusedPackage), Hash),
%   not provider(node(R, ReusedPackage), node(0, "libc")),
%   not attr("compatible_libc", node(R, ReusedPackage), _, _).

% The libc provider must be one that a compiler can target
:- has_built_packages(),
   provider(node(X, LibcPackage), node(0, "libc")),
   attr("node", node(X, LibcPackage)),
   attr("version", node(X, LibcPackage), LibcVersion),
   not host_libc(LibcPackage, LibcVersion).
