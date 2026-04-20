# Snapshot file
# Unset all aliases to avoid conflicts with functions
unalias -a 2>/dev/null || true
# Functions
# Shell Options
setopt nohashdirs
setopt login
# Aliases
alias -- macmini='ssh macmini'
alias -- maid='ssh macmini -t "claude"'
alias -- run-help=man
alias -- which-command=whence
# Check for rg availability
if ! (unalias rg 2>/dev/null; command -v rg) >/dev/null 2>&1; then
  function rg {
  if [[ -n $ZSH_VERSION ]]; then
    ARGV0=rg '/Users/shigesan/Library/Application Support/Claude/claude-code/2.1.78/claude.app/Contents/MacOS/claude' "$@"
  elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
    ARGV0=rg '/Users/shigesan/Library/Application Support/Claude/claude-code/2.1.78/claude.app/Contents/MacOS/claude' "$@"
  elif [[ $BASHPID != $$ ]]; then
    exec -a rg '/Users/shigesan/Library/Application Support/Claude/claude-code/2.1.78/claude.app/Contents/MacOS/claude' "$@"
  else
    (exec -a rg '/Users/shigesan/Library/Application Support/Claude/claude-code/2.1.78/claude.app/Contents/MacOS/claude' "$@")
  fi
}
fi
export PATH=/Users/shigesan/Library/Python/3.9/bin\:/Users/shigesan/.bun/bin\:/opt/homebrew/bin\:/opt/homebrew/sbin\:/usr/local/bin\:/System/Cryptexes/App/usr/bin\:/usr/bin\:/bin\:/usr/sbin\:/sbin\:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin\:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin\:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin\:/opt/pkg/env/active/bin\:/opt/pmk/env/global/bin
