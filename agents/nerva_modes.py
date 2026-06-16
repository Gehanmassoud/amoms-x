"""NERVA operating mode definitions.

Shared architecture component for the NERVA Autonomous Enterprise Nervous System.
This module centralizes operating mode constants and helper accessors so that
voice, immune, and future system components can reference modes without
hard-coded strings.

Architecture context:
- Reactive Mode: Voice Agent -> Context Agent -> Reasoning Agent -> Consequence Cascade Engine -> Future Trajectory Engine -> Risk Response Agent
- Immune Mode: Immune Agent -> Context Agent -> Reasoning Agent -> Consequence Cascade Engine -> Future Trajectory Engine -> Risk Response Agent

This module contains no database access, no business logic, no reasoning logic,
no AI calls, and no agent or engine behavior.
"""

from __future__ import annotations

from typing import ClassVar, Tuple


class NervaMode:
    """Centralized NERVA operating mode definitions.

    This component provides a consistent source of truth for supported NERVA
    operating modes across the platform. It is intentionally minimal and
    architecture-focused: only constants and mode helper methods are exposed.
    """

    REACTIVE: ClassVar[str] = "Reactive"
    IMMUNE: ClassVar[str] = "Immune"

    @classmethod
    def get_all_modes(cls) -> Tuple[str, str]:
        """Return all supported NERVA operating modes."""
        return (cls.REACTIVE, cls.IMMUNE)

    @classmethod
    def is_reactive(cls, mode: str) -> bool:
        """Return True when the supplied mode is the reactive mode."""
        return mode == cls.REACTIVE

    @classmethod
    def is_immune(cls, mode: str) -> bool:
        """Return True when the supplied mode is the immune mode."""
        return mode == cls.IMMUNE
