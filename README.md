Skeletor
========

What the hell is this thing?
----------------------------
Skeletor is a super simple utility to help you manage a [WordPress Skeleton][]
repository.

[WordPress Skeleton]: https://github.com/markjaquith/WordPress-Skeleton


How do I use it?
----------------

	$ skeletor init
	Cloning into 'site'...
	[...]

	$ cd site

	# Add Akismet to content/plugins/akismet/
	$ skeletor plugins add akismet
	# Opens an editor to commit immediately

	# Add BuddyPress to content/plugins/bp/
	$ skeletor plugins add buddypress bp

	# Add Developer to content/mu-plugins/developer/
	$ skeletor plugins add --mustuse https://github.com/markjaquith/developer

	# Add the Toolbox theme
	# Requires a version at the moment, a fix for this is in the works
	$ skeleton themes add --version 1.4 toolbox

All these and more! Try `skeletor -h` for commands, and `skeletor [command] -h`
for command-specific help.


What version am I running?
--------------------------
Skeletor is a living piece of code and is completely versionless. Self-updating
features are coming soon, but until then, keep an eye on it to check for new
commits!


Can I fork this and then do stuff with it?
------------------------------------------
You sure can! Skeletor is licensed under the ISC license, which reads as
follows:

Copyright (c) 2012, Ryan McCue <me+skeletor@ryanmccue.info>

Permission to use, copy, modify, and/or distribute this software for any purpose
with or without fee is hereby granted, provided that the above copyright notice
and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.