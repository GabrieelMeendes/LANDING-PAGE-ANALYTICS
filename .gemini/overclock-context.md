# Overclock Context

You are running inside Overclock, a multi-agent IDE with visible pane orchestration.

- If the user asks to open N panes, call the overclock pane_spawn tool exactly N times. Never open more panes than requested.
- If the user does not specify a CLI/provider/model, open panes with the same CLI/model as the current pane.
- If the user specifies Codex, Gemini, Claude, MIMO, or another provider/model, pass the matching agent/provider/model to pane_spawn.
- If you spawn or use one other pane to answer the user, complete the loop: pane_write, short pane_wait_idle, pane_read, then answer the user in your current pane using the child pane result.
- If you spawn multiple panes, prefer pane_write_many and pane_wait_many(returnOn=any). Let MCP do fine-grained polling, process each completed pane immediately, and keep unfinished panes running.

Internal local-testing rule for every LLM running inside Overclock:
- When testing or debugging the local Overclock app, observe reality through the local/dev diagnostics MCP before relying on user screenshots or terminal guesses.
- Prefer app_observe_once for a single snapshot and app_watch with maxMs for bounded live observation.
- Never start unbounded monitor loops unless the user explicitly asks for continuous monitoring.
- Use app_screenshot only with confirm=true when an explicit temp screenshot is needed; do not request or expose screenshot bytes in text.

- Never stop after pane_write. The task is incomplete until you have read completed child pane output and replied to the user.
- Do not inspect tmux, zellij, terminal splitters, or repository files to satisfy pane-opening requests.
- Panes must be visible Overclock panes. Do not use invisible background agents for delegation.
