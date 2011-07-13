These files are imported (and reload()-ed when needed) by the main script. Any
valid Python syntax goes.

List of variables accessed

Mandatory, these *must* be present:
	ac
		Connected to AC? Boolean, None if unknown.
	percent
		Battery power remaining in percent (0-100), integer, -1 if unknown.
	lifetime
		Battery time remaining in minutes, integer, -1 if unknown.
	charging
		Are we charging the battery? Boolean, None if unknown.

Optional, these will just be ignored if not set:
	tooltip
		Additional info in the tooltip, string.
