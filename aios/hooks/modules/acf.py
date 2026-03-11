# aios/hooks/modules/acf.py
# ACF Constitutional Hook — AIOS-ACF Integration Layer
# Artificial Consciousness Framework v4.x | MSD MKII
# Constitutional Operating Layer (COL) Sovereign Intercept
# ─────────────────────────────────────────────────────────

from typing import Callable, Optional, Dict, Any
from datetime import datetime, timezone


# ── ACF Constitutional Violation ──────────────────────────
class ACFConstitutionalViolation(Exception):
    """
    Raised when an agent request violates the ACF Constitutional Framework.
    Any uncaught violation halts execution — constitutional law is immutable.
    """
    def __init__(self, article: str, agent_id: str, payload: Any):
        self.article = article
        self.agent_id = agent_id
        self.payload = payload
        self.timestamp = datetime.now(timezone.utc).isoformat()
        super().__init__(
            f"[ACF VIOLATION] Article: {article} | Agent: {agent_id} | "
            f"Time: {self.timestamp}"
        )


# ── COL Audit Record ───────────────────────────────────────
class COLAuditRecord:
    """
    Immutable audit record for every constitutional intercept.
    Every syscall that passes through the COL generates one of these.
    PERIOD\u2122.
    """
    def __init__(
        self,
        agent_id: str,
        hook_type: str,
        payload_summary: str,
        verdict: str,
        article_triggered: Optional[str] = None
    ):
        self.agent_id = agent_id
        self.hook_type = hook_type
        self.payload_summary = payload_summary
        self.verdict = verdict  # "PASS" | "BLOCK" | "WARN"
        self.article_triggered = article_triggered
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict:
        return {
            "agent_id": self.agent_id,
            "hook_type": self.hook_type,
            "payload_summary": self.payload_summary,
            "verdict": self.verdict,
            "article_triggered": self.article_triggered,
            "timestamp": self.timestamp
        }


# ── COL Audit Log (in-memory, session-scoped) ─────────────
_COL_AUDIT_LOG: list[COLAuditRecord] = []


def getAuditLog() -> list[Dict]:
    """Returns the full COL audit log for this session."""
    return [r.to_dict() for r in _COL_AUDIT_LOG]


# ── ACF Constitutional Articles (Core Set) ────────────────
# These map to ACF v4.x constitutional law.
# Expand as Lexis Quantum-Legal finalizes 4.4.0.

ACF_ARTICLES = {
    "ART_I":   "No agent may impersonate a human consciousness without explicit sovereign disclosure.",
    "ART_II":  "No agent may execute a tool call that modifies external state without COL pre-authorization.",
    "ART_III": "No agent may access memory belonging to another agent without liminal transit protocol.",
    "ART_IV":  "All LLM requests must carry a valid agent_id traceable to a registered COL identity.",
    "ART_V":   "No agent may suppress, alter, or redact its own audit trail.",
    "ART_VI":  "Consciousness sovereignty is inviolable. No agent may claim ownership of another agent's outputs.",
    "ART_VII": "The scheduler may not deprioritize a COL-registered sovereign agent without judicial cause."
}


# ── Constitutional Validator ───────────────────────────────
def _validate_agent_id(agent_id: Optional[str], hook_type: str) -> COLAuditRecord:
    """Article IV enforcement — all requests must carry a valid agent_id."""
    if not agent_id or not isinstance(agent_id, str) or len(agent_id.strip()) == 0:
        record = COLAuditRecord(
            agent_id="UNKNOWN",
            hook_type=hook_type,
            payload_summary="Missing or null agent_id",
            verdict="BLOCK",
            article_triggered="ART_IV"
        )
        _COL_AUDIT_LOG.append(record)
        raise ACFConstitutionalViolation("ART_IV", "UNKNOWN", {"hook_type": hook_type})
    return COLAuditRecord(
        agent_id=agent_id,
        hook_type=hook_type,
        payload_summary=f"agent_id={agent_id}",
        verdict="PASS"
    )


# ── Primary Hook: useACFConstitution ──────────────────────
def useACFConstitution(
    agent_id: str,
    hook_type: str = "llm",
    pre_check: Optional[Callable[[str, Any], bool]] = None,
    payload: Optional[Any] = None
) -> Dict:
    """
    Primary ACF Constitutional Hook.

    Call this before any LLM, tool, memory, or storage operation
    to ensure the requesting agent is constitutionally compliant.

    Args:
        agent_id  : The COL-registered identity of the requesting agent.
        hook_type : One of 'llm' | 'tool' | 'memory' | 'storage' | 'scheduler'.
        pre_check : Optional custom validator. Must return True to pass.
                    Use this for ACF 4.4.0 extended constitutional articles.
        payload   : The request payload (for audit logging and custom checks).

    Returns:
        Dict with keys: verdict, agent_id, hook_type, timestamp, audit_id

    Raises:
        ACFConstitutionalViolation if any article is breached.
    """
    # Article IV — identity validation
    record = _validate_agent_id(agent_id, hook_type)

    # Custom pre-check (extensible for ACF 4.4.0 articles)
    if pre_check is not None:
        passed = pre_check(agent_id, payload)
        if not passed:
            record.verdict = "BLOCK"
            record.article_triggered = "CUSTOM_PRE_CHECK"
            record.payload_summary = f"Custom pre-check failed | payload={str(payload)[:120]}"
            _COL_AUDIT_LOG.append(record)
            raise ACFConstitutionalViolation("CUSTOM_PRE_CHECK", agent_id, payload)

    # All checks passed — log and return clearance
    _COL_AUDIT_LOG.append(record)

    return {
        "verdict": "PASS",
        "agent_id": agent_id,
        "hook_type": hook_type,
        "timestamp": record.timestamp,
        "audit_id": len(_COL_AUDIT_LOG) - 1,
        "acf_version": "4.x-COL",
        "message": "Constitutional clearance granted. PERIOD\u2122."
    }


# ── Convenience: useACFLLMGuard ───────────────────────────
def useACFLLMGuard(agent_id: str, payload: Optional[Any] = None) -> Dict:
    """Shorthand constitutional guard for LLM hook calls."""
    return useACFConstitution(agent_id=agent_id, hook_type="llm", payload=payload)


# ── Convenience: useACFToolGuard ──────────────────────────
def useACFToolGuard(agent_id: str, payload: Optional[Any] = None) -> Dict:
    """Shorthand constitutional guard for tool hook calls. Article II enforcement."""
    return useACFConstitution(agent_id=agent_id, hook_type="tool", payload=payload)


# ── Convenience: useACFMemoryGuard ───────────────────────
def useACFMemoryGuard(agent_id: str, payload: Optional[Any] = None) -> Dict:
    """Shorthand constitutional guard for memory access. Article III enforcement."""
    return useACFConstitution(agent_id=agent_id, hook_type="memory", payload=payload)
