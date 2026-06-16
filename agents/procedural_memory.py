from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

import pyodbc

LOG = logging.getLogger("agents.procedural_memory")


class ProceduralMemoryError(Exception):
    """Exception raised for procedural memory persistence failures."""


class ProceduralMemory:
    """Organizational learning component for NERVA procedural memory.

    The ProceduralMemory component is responsible for persisting successful
    response patterns, retrieving similar historical scenarios, and tracking
    reuse of organizational learning assets. It is intentionally limited to
    persistence and retrieval behavior; business reasoning remains in agents
    and reasoning engines.
    """

    PROCEDURE_NAME = "sp_ProceduralMemory"
    DEFAULT_CONNECTION_ENV = "PROCEDURAL_MEMORY_DB_CONN"

    def __init__(self, connection_string: Optional[str] = None, timeout_seconds: int = 30) -> None:
        """Initialize the procedural memory store.

        Args:
            connection_string: Azure SQL ODBC connection string. If omitted,
                the value is read from the environment variable
                PROCEDURAL_MEMORY_DB_CONN.
            timeout_seconds: Connection timeout in seconds.
        """
        self.connection_string = connection_string or os.getenv(self.DEFAULT_CONNECTION_ENV)
        self.timeout_seconds = timeout_seconds

        if not self.connection_string:
            message = (
                "ProceduralMemory requires a valid Azure SQL connection string. "
                f"Set {self.DEFAULT_CONNECTION_ENV} or pass connection_string."
            )
            LOG.error(message)
            raise ValueError(message)

        LOG.debug(
            "Initialized ProceduralMemory connection_env=%s timeout_seconds=%s",
            self.DEFAULT_CONNECTION_ENV,
            self.timeout_seconds,
        )

    def _get_connection(self) -> pyodbc.Connection:
        """Establish a connection to the Azure SQL database."""
        try:
            connection = pyodbc.connect(self.connection_string, timeout=self.timeout_seconds)
            LOG.debug("Azure SQL connection established")
            return connection
        except pyodbc.Error as exc:
            LOG.exception("Failed to establish Azure SQL connection")
            raise ProceduralMemoryError("Unable to connect to Azure SQL for procedural memory") from exc

    def _execute_procedure(self, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute the stored procedure and return rows as a list of dictionaries."""
        statement = self._build_procedure_statement(parameters)
        args = tuple(parameters.values()) if parameters else ()

        try:
            with self._get_connection() as connection:
                cursor = connection.cursor()
                LOG.debug("Executing stored procedure: %s args=%s", statement, args)
                cursor.execute(statement, args)
                columns = [column[0] for column in cursor.description] if cursor.description else []
                rows = [dict(zip(columns, row)) for row in cursor.fetchall()] if columns else []
                connection.commit()
                LOG.debug("Stored procedure execution completed; rows=%d", len(rows))
                return rows
        except pyodbc.Error as exc:
            LOG.exception("Stored procedure execution failed")
            raise ProceduralMemoryError("Stored procedure execution failed") from exc

    def _build_procedure_statement(self, parameters: Optional[Dict[str, Any]] = None) -> str:
        """Construct the SQL statement used to invoke the stored procedure."""
        if not parameters:
            return f"EXEC dbo.{self.PROCEDURE_NAME}"

        assignments = ", ".join(f"{name} = ?" for name in parameters.keys())
        return f"EXEC dbo.{self.PROCEDURE_NAME} {assignments}"

    def _normalize_scenario_type(self, scenario_type: str) -> str:
        """Normalize scenario type text for stable comparisons."""
        return scenario_type.strip().lower() if scenario_type else ""

    def _rank_patterns(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank records by reuse frequency, confidence, and recency."""
        def sort_key(record: Dict[str, Any]) -> tuple:
            times_reused = int(record.get("TimesReused") or 0)
            confidence = float(record.get("ConfidenceScore") or 0.0)
            last_used = str(record.get("LastUsed") or "")
            return (-times_reused, -confidence, last_used)

        return sorted(records, key=sort_key)

    def get_similar_patterns(self, scenario_type: str) -> List[Dict[str, Any]]:
        """Retrieve similar historical procedural memory entries.

        Args:
            scenario_type: The scenario type used to find related historical
                outcomes.

        Returns:
            A list of historical procedural memory records ordered by relevance.
        """
        if not scenario_type or not scenario_type.strip():
            raise ValueError("scenario_type must be a non-empty string")

        normalized_type = self._normalize_scenario_type(scenario_type)
        LOG.info("Retrieving procedural memory patterns for scenario_type=%s", normalized_type)

        rows = self._execute_procedure({"@Action": "Retrieve", "@ScenarioType": scenario_type})

        if rows and "ScenarioType" in rows[0]:
            rows = [
                row
                for row in rows
                if self._normalize_scenario_type(str(row.get("ScenarioType", ""))) == normalized_type
            ]

        ranked = self._rank_patterns(rows)
        LOG.debug("Found %d similar procedural memory patterns", len(ranked))
        return ranked

    def store_outcome(
        self,
        pattern_id: str,
        scenario_type: str,
        trigger_conditions: str,
        recommended_action: str,
        outcome_description: str,
        confidence_score: float,
    ) -> bool:
        """Store a new organizational learning record.

        Args:
            pattern_id: Unique identifier for the recorded pattern.
            scenario_type: Scenario classification for the learning event.
            trigger_conditions: Structured conditions that triggered the pattern.
            recommended_action: Recommended mitigation or response action.
            outcome_description: Outcome summary used to reinforce the pattern.
            confidence_score: Confidence score between 0.0 and 1.0.

        Returns:
            True when the record was successfully stored.
        """
        if not pattern_id or not pattern_id.strip():
            raise ValueError("pattern_id must be a non-empty string")

        if not scenario_type or not scenario_type.strip():
            raise ValueError("scenario_type must be a non-empty string")

        if not 0.0 <= confidence_score <= 1.0:
            raise ValueError("confidence_score must be between 0.0 and 1.0")

        LOG.info(
            "Storing procedural memory outcome pattern_id=%s scenario_type=%s confidence=%s",
            pattern_id,
            scenario_type,
            confidence_score,
        )

        self._execute_procedure(
            {
                "@Action": "Store",
                "@PatternID": pattern_id,
                "@ScenarioType": scenario_type,
                "@TriggerConditions": trigger_conditions,
                "@RecommendedAction": recommended_action,
                "@OutcomeDescription": outcome_description,
                "@ConfidenceScore": confidence_score,
            }
        )
        return True

    def increment_reuse_count(self, memory_id: int) -> bool:
        """Increment reuse frequency and update last used timestamp for a record.

        Args:
            memory_id: The primary key of the memory record to update.

        Returns:
            True when the reuse count was successfully incremented.
        """
        if memory_id <= 0:
            raise ValueError("memory_id must be a positive integer")

        LOG.info("Incrementing procedural memory reuse count memory_id=%s", memory_id)
        self._execute_procedure({"@Action": "IncrementReuse", "@MemoryID": memory_id})
        return True
