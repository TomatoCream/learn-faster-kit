#!/usr/bin/env python3
"""
Learn FASTER CLI - One-time installer for AI-assisted learning system.

Supports both Claude Code and OpenCode as AI agent backends.

Usage:
    uvx learn-faster init --agent claude
    uvx learn-faster init --agent opencode
    uvx learn-faster --agent claude
    uvx learn-faster --agent opencode
"""

import sys
import shutil
import platform
import inquirer
import json
from pathlib import Path


VALID_AGENTS = ("claude", "opencode")


# ANSI color codes
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Colors
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"


BANNER = f"""{Colors.CYAN}
██╗     ███████╗ █████╗ ██████╗ ███╗   ██╗    ███████╗ █████╗ ███████╗████████╗███████╗██████╗
██║     ██╔════╝██╔══██╗██╔══██╗████╗  ██║    ██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
██║     █████╗  ███████║██████╔╝██╔██╗ ██║    █████╗  ███████║███████╗   ██║   █████╗  ██████╔╝
██║     ██╔══╝  ██╔══██║██╔══██╗██║╚██╗██║    ██╔══╝  ██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗
███████╗███████╗██║  ██║██║  ██║██║ ╚████║    ██║     ██║  ██║███████║   ██║   ███████╗██║  ██║
╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝    ╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
{Colors.RESET}"""


def print_success(msg: str) -> None:
    """Print success message in green."""
    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")


def print_info(msg: str) -> None:
    """Print info message in cyan."""
    print(f"{Colors.CYAN}{msg}{Colors.RESET}")


def print_warning(msg: str) -> None:
    """Print warning message in yellow."""
    print(f"{Colors.YELLOW}!{Colors.RESET} {msg}")


def print_header(msg: str) -> None:
    """Print header message in bold magenta."""
    print(f"{Colors.BOLD}{Colors.MAGENTA}{msg}{Colors.RESET}")


def print_dim(msg: str) -> None:
    """Print dimmed message."""
    print(f"{Colors.DIM}{msg}{Colors.RESET}")


def print_error(msg: str) -> None:
    """Print error message in red."""
    print(f"{Colors.RED}✗{Colors.RESET} {msg}")


def get_templates_dir() -> Path:
    """Get the templates directory from the installed package."""
    return Path(__file__).parent.parent / "templates"


def agent_display_name(agent: str) -> str:
    """Get display name for agent."""
    return {"claude": "Claude Code", "opencode": "OpenCode"}[agent]


def agent_config_dir_name(agent: str) -> str:
    """Get the config directory name for the agent."""
    return {"claude": ".claude", "opencode": ".opencode"}[agent]


def agent_instructions_filename(agent: str) -> str:
    """Get the instructions filename for the agent."""
    return {"claude": "CLAUDE.md", "opencode": "INSTRUCTIONS.md"}[agent]


# Claude model short names -> OpenCode full model IDs
OPENCODE_MODEL_MAP = {
    "sonnet": "anthropic/claude-sonnet-4-20250514",
    "opus": "anthropic/claude-opus-4-20250514",
    "haiku": "anthropic/claude-haiku-4-5-20251001",
}

# Claude tool names -> OpenCode tool names (lowercase)
OPENCODE_TOOL_MAP = {
    "Read": "read",
    "Write": "write",
    "Edit": "edit",
    "Bash": "bash",
    "Glob": "glob",
    "Grep": "grep",
    "WebSearch": "websearch",
    "WebFetch": "webfetch",
}


def transform_agent_for_opencode(src_path: Path, dest_path: Path) -> None:
    """Copy an agent markdown file, transforming Claude frontmatter to OpenCode format.

    Claude format:
        name: practice-creator
        description: ...
        tools: Read, Write, Edit
        model: sonnet

    OpenCode format:
        description: ...
        mode: subagent
        model: anthropic/claude-sonnet-4-20250514
        tools:
          read: true
          write: true
          edit: true
    """
    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")

    # Parse frontmatter
    if not lines or lines[0].strip() != "---":
        # No frontmatter, copy as-is
        shutil.copy2(src_path, dest_path)
        return

    frontmatter_end = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            frontmatter_end = i
            break

    if frontmatter_end == -1:
        shutil.copy2(src_path, dest_path)
        return

    # Extract frontmatter key-value pairs
    fm_lines = lines[1:frontmatter_end]
    body = "\n".join(lines[frontmatter_end + 1 :])

    fm = {}
    for line in fm_lines:
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()

    # Build OpenCode frontmatter
    new_fm_lines = ["---"]

    # description (required)
    if "description" in fm:
        new_fm_lines.append(f"description: {fm['description']}")

    # mode: always subagent for these
    new_fm_lines.append("mode: subagent")

    # model: map short name to full ID
    if "model" in fm:
        model = OPENCODE_MODEL_MAP.get(fm["model"], fm["model"])
        new_fm_lines.append(f"model: {model}")

    # tools: convert comma-separated string to YAML mapping
    if "tools" in fm:
        tool_names = [t.strip() for t in fm["tools"].split(",")]
        new_fm_lines.append("tools:")
        for tool in tool_names:
            oc_name = OPENCODE_TOOL_MAP.get(tool, tool.lower())
            new_fm_lines.append(f"  {oc_name}: true")

    new_fm_lines.append("---")

    new_content = "\n".join(new_fm_lines) + body
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(new_content)


# --- Claude Code specifics ---


def create_or_update_claude_settings(claude_dir: Path) -> None:
    """Create or update .claude/settings.local.json."""
    settings_file = claude_dir / "settings.local.json"

    default_settings = {
        "permissions": {
            "allow": [
                "Bash(python3 .learning/scripts/:*)",
                "Bash(ls:*)",
                "Read(.learning/**)",
                "Write(.learning/**)",
                "Write(**/*.md)",
                "Read(**/*.md)",
            ],
            "deny": [
                "Bash(rm:*)",
                "Bash(curl:*)",
                "Read(.env)",
                "Read(.env.*)",
                "Write(.env)",
                "Write(.env.*)",
            ],
        },
        "companyAnnouncements": [
            'Learn FASTER is active! Use /learn "Topic" to start learning',
        ],
    }

    if settings_file.exists():
        with open(settings_file, "r") as f:
            settings = json.load(f)

        if "permissions" not in settings:
            settings["permissions"] = default_settings["permissions"]
        else:
            if "allow" not in settings["permissions"]:
                settings["permissions"]["allow"] = []
            for perm in default_settings["permissions"]["allow"]:
                if perm not in settings["permissions"]["allow"]:
                    settings["permissions"]["allow"].append(perm)

            if "deny" not in settings["permissions"]:
                settings["permissions"]["deny"] = []
            for perm in default_settings["permissions"]["deny"]:
                if perm not in settings["permissions"]["deny"]:
                    settings["permissions"]["deny"].append(perm)

        if "companyAnnouncements" not in settings:
            settings["companyAnnouncements"] = default_settings["companyAnnouncements"]

        print_success(f"Updated {settings_file}")
    else:
        settings = default_settings
        print_success(f"Created {settings_file}")

    with open(settings_file, "w") as f:
        json.dump(settings, f, indent=2)


# --- OpenCode specifics ---


def create_or_update_opencode_config(cwd: Path) -> None:
    """Create or update opencode.json in the project root."""
    config_file = cwd / "opencode.json"

    default_config = {
        "$schema": "https://opencode.ai/config.json",
        "instructions": ["INSTRUCTIONS.md"],
        "permission": {"*": "allow"},
    }

    if config_file.exists():
        with open(config_file, "r") as f:
            config = json.load(f)

        # Merge instructions
        if "instructions" not in config:
            config["instructions"] = default_config["instructions"]
        else:
            for instr in default_config["instructions"]:
                if instr not in config["instructions"]:
                    config["instructions"].append(instr)

        # Merge permissions
        if "permission" not in config:
            config["permission"] = default_config["permission"]

        print_success(f"Updated {config_file}")
    else:
        config = default_config
        print_success(f"Created {config_file}")

    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)


# --- Common ---


def check_initialization() -> bool:
    """Check if project has been initialized."""
    config_path = Path.cwd() / ".learning" / "config.json"
    if not config_path.exists():
        return False

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return config.get("initialized", False)
    except Exception:
        return False


def get_configured_agent() -> str:
    """Get the agent type from existing config, or return empty string."""
    config_path = Path.cwd() / ".learning" / "config.json"
    if not config_path.exists():
        return ""
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return config.get("agent", "")
    except Exception:
        return ""


def init_project(agent: str) -> None:
    """Initialize Learn FASTER in the current project."""

    cwd = Path.cwd()
    templates_dir = get_templates_dir()

    display = agent_display_name(agent)

    print(BANNER)
    print_header(f"\nInitializing Learn FASTER for {display}...\n")

    # Ask for learning mode selection
    learning_mode_question = [
        inquirer.List(
            "mode",
            message="Choose your learning mode",
            choices=[
                (
                    "Balanced         - Mix of theory, practice, and application",
                    "balanced",
                ),
                (
                    "Exam-Oriented   - Printable exam papers, practice tests, and certification prep",
                    "exam",
                ),
                (
                    "Theory-Focused   - Deep conceptual understanding and mental models",
                    "theory",
                ),
                (
                    "Practical        - Build projects immediately, learn by doing",
                    "practical",
                ),
                (
                    "Programming      - Learn programming through building projects",
                    "programming",
                ),
            ],
            default="balanced",
        ),
    ]

    mode_answer = inquirer.prompt(learning_mode_question)
    learning_mode = mode_answer["mode"] if mode_answer else "balanced"

    mode_names = {
        "exam": "Exam-Oriented",
        "theory": "Theory-Focused",
        "practical": "Practical",
        "balanced": "Balanced",
        "programming": "Programming",
    }
    print_success(f"Selected: {mode_names[learning_mode]} mode\n")

    # Ask about macOS Reminders (only on macOS)
    macos_reminders = False
    if platform.system() == "Darwin":
        response = (
            input(
                f"{Colors.CYAN}Enable macOS Reminders for review notifications? (y/n):{Colors.RESET} "
            )
            .strip()
            .lower()
        )
        macos_reminders = response in ["y", "yes"]

    # Create agent config directory structure
    config_dir_name = agent_config_dir_name(agent)
    config_dir = cwd / config_dir_name
    config_dir.mkdir(exist_ok=True)

    # Copy mode-specific agents and commands
    mode_templates_dir = templates_dir / "modes" / learning_mode

    # Copy agents for selected mode
    agents_dest = config_dir / "agents"
    agents_dest.mkdir(exist_ok=True)
    agents_src = mode_templates_dir / "agents"

    if agents_src.exists():
        for file in agents_src.glob("*.md"):
            if agent == "opencode":
                transform_agent_for_opencode(file, agents_dest / file.name)
            else:
                shutil.copy2(file, agents_dest / file.name)
            print_success(f"Copied agent: {file.name}")

    # Copy commands for selected mode
    commands_dest = config_dir / "commands"
    commands_dest.mkdir(exist_ok=True)
    commands_src = mode_templates_dir / "commands"

    if commands_src.exists():
        for file in commands_src.glob("*.md"):
            shutil.copy2(file, commands_dest / file.name)
            print_success(f"Copied command: {file.name}")

    # Agent-specific settings/config
    if agent == "claude":
        create_or_update_claude_settings(config_dir)
    elif agent == "opencode":
        create_or_update_opencode_config(cwd)

    # Create .learning directory structure
    learning_dir = cwd / ".learning"
    learning_dir.mkdir(exist_ok=True)

    # Create config.json with initialization flag
    config = {
        "initialized": True,
        "agent": agent,
        "learning_mode": learning_mode,
        "macos_reminders_enabled": macos_reminders,
    }
    config_path = learning_dir / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print_success(
        f"Created config.json (Agent: {display}, Mode: {mode_names[learning_mode]}, macOS Reminders: {'enabled' if macos_reminders else 'disabled'})"
    )

    # Copy scripts
    scripts_dest = learning_dir / "scripts"
    scripts_dest.mkdir(exist_ok=True)
    scripts_src = templates_dir / "scripts"
    if scripts_src.exists():
        for file in scripts_src.glob("*.py"):
            shutil.copy2(file, scripts_dest / file.name)
            print_success(f"Copied script: {file.name}")

    # Copy references
    references_dest = learning_dir / "references"
    references_dest.mkdir(exist_ok=True)
    references_src = templates_dir / "references"
    if references_src.exists():
        for file in references_src.glob("*.md"):
            shutil.copy2(file, references_dest / file.name)
            print_success(f"Copied reference: {file.name}")

    # Copy instructions to project root
    instructions_src = templates_dir / "instructions.md"
    instructions_filename = agent_instructions_filename(agent)
    instructions_dest = cwd / instructions_filename
    if instructions_src.exists() and not instructions_dest.exists():
        shutil.copy2(instructions_src, instructions_dest)
        print_success(f"Copied instructions to {instructions_filename} in project root")
    elif instructions_dest.exists():
        print_warning(f"{instructions_filename} already exists, skipping")

    print(f"\n{Colors.GREEN}{Colors.BOLD}Initialization complete!{Colors.RESET}\n")

    print_header(f"Available commands in {display}:")
    print(
        f"  {Colors.CYAN}/learn [topic]{Colors.RESET}    - Initialize or continue learning"
    )
    print(
        f"  {Colors.CYAN}/review{Colors.RESET}           - Spaced repetition review session"
    )
    print(
        f"  {Colors.CYAN}/progress{Colors.RESET}         - Show detailed progress report"
    )
    print()


def launch_coach(agent: str, auto_review: bool = False) -> None:
    """Launch the AI agent with learn-faster system prompt."""
    import subprocess

    # Get the learning mode from config
    config_path = Path.cwd() / ".learning" / "config.json"
    learning_mode = "balanced"  # default
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                learning_mode = config.get("learning_mode", "balanced")
        except Exception:
            pass

    # Get the path to the system prompt template
    templates_dir = Path(__file__).parent.parent / "templates"
    system_prompt_path = (
        templates_dir / "modes" / learning_mode / "system_prompts" / "learn-faster.md"
    )

    if not system_prompt_path.exists():
        print_error(f"Error: System prompt for '{learning_mode}' mode not found")
        print_dim(f"Expected at: {system_prompt_path}")
        sys.exit(1)

    # Read the system prompt content (skip frontmatter)
    with open(system_prompt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Skip frontmatter (between --- lines)
    in_frontmatter = False
    content_lines = []
    for line in lines:
        if line.strip() == "---":
            if not in_frontmatter:
                in_frontmatter = True
                continue
            else:
                in_frontmatter = False
                continue
        if not in_frontmatter:
            content_lines.append(line)

    system_prompt = "".join(content_lines).strip()

    display = agent_display_name(agent)

    print_info(f"Launching {display} in learning coach mode...")
    print_dim("(Using FASTER framework system prompt)\n")

    if agent == "claude":
        cmd = ["claude", "--system-prompt", system_prompt]
        if auto_review:
            cmd.extend(["/review"])
    elif agent == "opencode":
        cmd = ["opencode", "--prompt", system_prompt]
        if auto_review:
            cmd.extend(["--message", "/review"])

    try:
        subprocess.run(cmd, check=False)
    except FileNotFoundError:
        binary = "claude" if agent == "claude" else "opencode"
        print_error(f"Error: '{binary}' command not found")
        print_dim(f"Make sure {display} CLI is installed and in your PATH")
        if agent == "claude":
            print_dim("Install from: https://claude.ai/download")
        else:
            print_dim("Install from: https://opencode.ai")
        sys.exit(1)


def parse_agent_arg(args: list[str]) -> tuple[str, list[str]]:
    """Extract --agent from args, return (agent, remaining_args).

    The --agent flag is required for all commands.
    """
    agent = None
    remaining = []
    i = 0
    while i < len(args):
        if args[i] == "--agent" and i + 1 < len(args):
            agent = args[i + 1]
            i += 2
        else:
            remaining.append(args[i])
            i += 1

    if agent is None:
        # Check if already initialized - use stored agent
        stored = get_configured_agent()
        if stored:
            return stored, remaining

        print_error("Missing required flag: --agent <claude|opencode>")
        print_dim("Example: learn-faster --agent claude")
        print_dim("Example: learn-faster init --agent opencode")
        sys.exit(1)

    if agent not in VALID_AGENTS:
        print_error(
            f"Invalid agent: '{agent}'. Must be one of: {', '.join(VALID_AGENTS)}"
        )
        sys.exit(1)

    return agent, remaining


def main() -> None:
    """Main CLI entry point."""
    raw_args = sys.argv[1:]

    # Handle version and help before requiring --agent
    if len(raw_args) >= 1 and raw_args[0] in ("version", "--version"):
        from learn_faster import __version__

        print(f"learn-faster version {__version__}")
        return

    if len(raw_args) >= 1 and raw_args[0] in ("help", "--help", "-h"):
        print("Learn FASTER - Accelerate learning with FASTER framework\n")
        print("Usage:")
        print(
            "  learn-faster --agent <claude|opencode>           Auto-init and launch in coach mode"
        )
        print(
            "  learn-faster init --agent <claude|opencode>      Force re-initialization"
        )
        print("  learn-faster version                             Show version")
        print()
        print("Options:")
        print("  --agent <claude|opencode>   Required. Choose AI agent backend.")
        print(
            "                              (Omit if already initialized - uses stored config)"
        )
        print()
        print("For more info: https://github.com/cheukyin175/learn-faster-kit")
        return

    agent, remaining = parse_agent_arg(raw_args)

    # Check for explicit commands
    if len(remaining) >= 1:
        command = remaining[0]

        if command == "init":
            init_project(agent)
            return
        else:
            print_error(f"Unknown command: {command}")
            print_dim("Run 'learn-faster --help' for usage")
            sys.exit(1)

    # Default behavior: check init, then launch
    display = agent_display_name(agent)
    if not check_initialization():
        print_info("First-time setup detected. Initializing...")
        print()
        init_project(agent)
        print()
        print_header(f"Launching {display} with FASTER framework...")
        print()
        launch_coach(agent, auto_review=False)
    else:
        # Verify agent matches what was initialized
        stored = get_configured_agent()
        if stored and stored != agent:
            print_warning(
                f"Project was initialized with {agent_display_name(stored)}, but --agent {agent} was given."
            )
            print_warning(
                f"Using {agent_display_name(agent)} as requested. Re-run 'learn-faster init --agent {agent}' to switch fully."
            )

        print_info(f"Launching {display} in learning coach mode...")
        print_dim("(Starting with /review to check for due reviews)\n")
        launch_coach(agent, auto_review=True)


if __name__ == "__main__":
    main()
