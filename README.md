# Learn FASTER

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

> AI-powered learning coach that accelerates mastery through spaced repetition, personalized syllabi, and active practice.

**Works with [Claude Code](https://claude.com/claude-code) and [OpenCode](https://opencode.ai)** - Integrates AI coaching directly into your development environment.

## Why Learn FASTER?

Master any technical skill with science-backed learning principles:

-   **Personalized syllabi** generated for your skill level and learning goals
-   **Spaced repetition** system that schedules reviews at optimal intervals
-   **Four learning modes** - choose Balanced, Exam-Prep, Theory-Focused, or Practical
-   **Active practice** with auto-generated exercises and projects
-   **Progress tracking** to visualize your learning journey

## The FASTER Framework

-   **F**orget: Beginner's mindset - approach topics with fresh perspective
-   **A**ct: Learn by doing - hands-on practice over passive reading
-   **S**tate: Optimize focus - create ideal learning conditions
-   **T**each: Explain to retain - teaching reinforces understanding
-   **E**nter: Consistent sessions - regular practice builds momentum
-   **R**eview: Spaced repetition - review at intervals for long-term retention

## Installation

**Prerequisites:** [uv](https://docs.astral.sh/uv/) package manager

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Option 1: Persistent Installation (Recommended)

Install once and use across all projects:

```bash
uv tool install learn-faster --from git+https://github.com/cheukyin175/learn-faster-kit.git
```

Then in any project directory, simply run:

```bash
# For Claude Code
learn-faster --agent claude

# For OpenCode
learn-faster --agent opencode
```

This will auto-initialize on first run and launch the chosen AI agent with FASTER coaching mode.

### Option 2: One-Time Use

Run directly without installation:

```bash
# For Claude Code
uvx --from git+https://github.com/cheukyin175/learn-faster-kit.git learn-faster --agent claude

# For OpenCode
uvx --from git+https://github.com/cheukyin175/learn-faster-kit.git learn-faster --agent opencode
```

### What Gets Installed

On first run, learn-faster creates agent-specific config directories:

**For Claude Code (`--agent claude`):**
```
your-project/
├── .claude/
│   ├── agents/practice-creator.md
│   ├── commands/
│   │   ├── learn.md
│   │   ├── review.md
│   │   └── progress.md
│   └── settings.local.json
├── .learning/
│   ├── config.json
│   ├── scripts/
│   │   ├── init_learning.py
│   │   ├── log_progress.py
│   │   ├── review_scheduler.py
│   │   └── generate_syllabus.py
│   └── references/faster_framework.md
└── CLAUDE.md
```

**For OpenCode (`--agent opencode`):**
```
your-project/
├── .opencode/
│   ├── agents/practice-creator.md
│   ├── commands/
│   │   ├── learn.md
│   │   ├── review.md
│   │   └── progress.md
├── opencode.json
├── .learning/
│   ├── config.json
│   ├── scripts/
│   │   ├── init_learning.py
│   │   ├── log_progress.py
│   │   ├── review_scheduler.py
│   │   └── generate_syllabus.py
│   └── references/faster_framework.md
└── INSTRUCTIONS.md
```

## Quick Start

1. **Install the tool**

    ```bash
    uv tool install learn-faster --from git+https://github.com/cheukyin175/learn-faster-kit.git
    ```

2. **Launch in any project directory**

    ```bash
    cd your-learning-project
    learn-faster --agent claude    # or --agent opencode
    ```

    First run will:

    - Prompt you to select a learning mode
    - Initialize the project structure
    - Launch the AI agent with FASTER coaching enabled

    After initialization, the `--agent` flag is optional (stored in config):

    ```bash
    learn-faster    # uses the agent from initialization
    ```

3. **Start learning**

    ```bash
    /learn "Golang fundamentals"
    ```

    The AI coach will generate a personalized syllabus and guide your learning session.

## Demo: Teach-Back in Action

The "T" in FASTER—teaching to retain—is the key differentiator. Here's how it works:

```bash
mkdir learn-go && cd learn-go
learn-faster --agent claude     # Select "Balanced" mode
/learn "Go error handling"      # In your AI agent
```

```
Coach: You've just learned about error wrapping. Ready to teach it back?
       ┌ Teach Back
       │ ● Yes, let me explain
       │ ○ Need review first
       │ ○ Not sure yet
       └

You:   So when you wrap an error with fmt.Errorf and %w, you're adding
       context like "failed to open config" while keeping the original
       error inside. Then errors.Is can still match the root cause.

Coach: Great explanation! You nailed the key insight—wrapped errors
       preserve the chain for inspection. Adding "error wrapping" to
       your review schedule. First review tomorrow.
```

**Why this works:** Explaining concepts in your own words forces active recall—proven to boost retention 2-3x vs passive reading. The coach won't just tell you answers; it guides you to construct understanding yourself.

## Usage

### CLI Commands

-   `learn-faster --agent <claude|opencode>` - Launch AI agent with FASTER coaching (auto-initializes on first run)
-   `learn-faster init --agent <claude|opencode>` - Force re-initialization or switch learning modes
-   `learn-faster version` - Show current version

The `--agent` flag is required on first run. After initialization, it's optional (the stored agent is used).

### Slash Commands

Once your AI agent is running, use these commands:

-   `/learn [topic]` - Start or continue learning a topic with personalized syllabus
-   `/review` - Spaced repetition review session for topics you've learned
-   `/progress` - View detailed progress report and learning statistics

## Learning Modes

Choose the mode that fits your learning style:

-   **Balanced** - Mix of theory, practice, and real-world application (recommended for most learners)
-   **Exam-Prep** - Focused on recall, practice tests, and certification preparation
-   **Theory-Focused** - Deep conceptual understanding with mental models and first principles
-   **Practical** - Project-based learning with immediate application

Each mode provides a tailored coaching experience with mode-specific syllabi and exercises.

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/cheukyin175/learn-faster-kit.git
cd learn-faster-kit

# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

## Use Cases

Learn FASTER is ideal for:

-   Learning new programming languages (Go, Rust, Python, TypeScript, etc.)
-   Preparing for technical certifications and exams
-   Mastering frameworks and libraries (React, Next.js, Django, etc.)
-   Building structured self-study programs
-   Onboarding to new codebases or technologies

## Requirements

-   Python 3.12+
-   [Claude Code](https://claude.com/claude-code) or [OpenCode](https://opencode.ai)
-   [uv](https://docs.astral.sh/uv/) package manager

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

MIT License - See LICENSE file for details
