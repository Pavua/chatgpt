# Project Roadmap

This roadmap outlines upcoming milestones for evolving the Telegram userbot toward the original goal of a fully featured macOS/iOS application with LLM integration and GUI management.

## v0.2 – Bot polish
- [x] Refine runtime commands: add `!tokens`, `!top_p` and other generation controls
- [x] Support environment variables for all key paths (logs, prompts)
- [x] Provide optional persistent conversation context per chat
- [x] Improve logging format with session IDs and metadata

## v0.3 – Desktop GUI
- [x] Create a minimal Electron frontend that communicates with the bot via a local HTTP API
- [x] Expose settings for model selection, prompt editing and history browsing
- [x] Implement theme switching and basic animations
- [x] Package the GUI for macOS and Windows

## v0.4 – SwiftUI client
- [x] Build a native SwiftUI application for macOS/iOS sharing the same API
- [x] Support push notifications and background start on macOS
- [x] Allow editing of whitelist/blacklist and prompt files directly in the GUI

## v0.5 – Fine-tuning tools
- [x] Interactive log review and dataset curation inside the GUI
- [x] Launch local fine-tuning jobs using the exported dataset
- [x] Switch models automatically once fine-tuning completes

## v1.0 – Release
- [ ] Stable cross-platform packages
- [ ] Automatic updates and configuration sync
- [ ] Plugin system for custom commands and integrations

This plan will evolve as we gather feedback.
