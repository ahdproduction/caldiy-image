"""Force le format 24 h sur la page de reservation et retire le bouton 12h/24h.

Lance depuis la racine du depot calcom/cal.diy. Echoue si le code amont a change.
"""
import re
import sys
from pathlib import Path


def patch(path, pattern, repl, flags=0):
    p = Path(path)
    src = p.read_text()
    new, n = re.subn(pattern, repl, src, count=1, flags=flags)
    if n != 1:
        sys.exit(f"motif introuvable dans {path}: {pattern[:60]}")
    p.write_text(new)
    print(f"patched {path}")


# 1. Le navigateur est toujours considere comme 24 h.
patch(
    "packages/lib/timeFormat.ts",
    r"export const isBrowserLocale24h = \(\) => \{.*?\n\};\n",
    "export const isBrowserLocale24h = () => true;\n",
    re.S,
)

# 2. Le choix memorise par un visiteur (localStorage) est ignore.
patch(
    "packages/features/bookings/lib/timePreferences.ts",
    r"timeFormat: detectBrowserTimeFormat,",
    "timeFormat: TimeFormat.TWENTY_FOUR_HOUR,",
)

# 3. Le bouton 12h/24h n'est plus affiche.
patch(
    "packages/features/bookings/components/TimeFormatToggle.tsx",
    r"\n  return \(\n    <ToggleGroup",
    "\n  if (timeFormat) return null;\n  return (\n    <ToggleGroup",
)
