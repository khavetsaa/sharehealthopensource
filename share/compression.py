"""Safety interlocks for the belt's compression pad (external uterine massage).

Compression may only run when ALL of these are true:
  * staff have confirmed PPH and pressed start (the device never starts itself)
  * the fundal tone sensor or the midwife reports a soft (atonic) uterus
Pressure is capped, the pad deflates on stop, fault or power loss, and one
button stops everything. This is controller logic for simulation and testing;
real firmware must be developed under IEC 62304 and bench-tested under IEC 60601-1.
"""
from __future__ import annotations

from dataclasses import dataclass

MAX_PRESSURE_MMHG = 60  # illustrative cap, to be set during bench testing


@dataclass
class CompressionController:
    pressure_mmhg: float = 0.0
    running: bool = False
    pph_confirmed_by_staff: bool = False

    def confirm_pph(self) -> None:
        self.pph_confirmed_by_staff = True

    def start(self, uterus_soft: bool) -> str:
        if not self.pph_confirmed_by_staff:
            return "Blocked: staff must confirm PPH first"
        if not uterus_soft:
            return "Blocked: uterus is firm, examine for other causes (tears, retained tissue)"
        self.running = True
        return "Compression cycles started"

    def set_pressure(self, requested_mmhg: float) -> float:
        if not self.running:
            self.pressure_mmhg = 0.0
            return 0.0
        self.pressure_mmhg = max(0.0, min(MAX_PRESSURE_MMHG, requested_mmhg))
        return self.pressure_mmhg

    def stop(self, reason: str = "staff stop") -> str:
        self.running = False
        self.pressure_mmhg = 0.0
        return f"Stopped and deflated ({reason})"

    def on_fault(self, fault: str) -> str:
        return self.stop(reason=f"fault: {fault}")
