# Architecture Overview

This document describes the high-level architecture of the Office Microservices ecosystem.

## Design Goals

- Local-first execution
- Read-only by default
- No hidden state
- Graceful failure
- Human-in-the-loop decision making

## System Layers

The system is composed of strictly decoupled layers:

1. Report Generation
2. Evidence Archiving
3. Task Scheduling
4. Advisory (AI Liaison)

Each layer operates independently and communicates only through human-readable artifacts.

## Non-Goals

- No auto-remediation
- No closed-loop automation
- No AI-driven decisions
