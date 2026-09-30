from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


def geometric_yield(step_yields: list[float]) -> float:
    result = 1.0
    for value in step_yields:
        if not 0.0 <= value <= 1.0:
            raise ValueError("yield outside [0,1]")
        result *= value
    return result


@dataclass(frozen=True, slots=True)
class StepYield:
    step: str
    input_units: int
    good_units: int

    def __post_init__(self) -> None:
        if self.input_units <= 0 or not 0 <= self.good_units <= self.input_units:
            raise ValueError("invalid step quantities")

    @property
    def fraction(self) -> float:
        return self.good_units / self.input_units


def duplicate_steps(steps: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for step in steps:
        if step in seen:
            duplicates.add(step)
        seen.add(step)
    return sorted(duplicates)


def ordered_route_steps(steps: list[StepYield], expected_steps: list[str]) -> list[StepYield]:
    repeated = duplicate_steps(step.step for step in steps)
    if repeated:
        raise ValueError(f"duplicate route step measurements: {repeated}")
    repeated_route = duplicate_steps(expected_steps)
    if repeated_route:
        raise ValueError(f"duplicate route steps: {repeated_route}")
    by_step = {step.step: step for step in steps}
    missing = [step for step in expected_steps if step not in by_step]
    extra = sorted(set(by_step) - set(expected_steps))
    if missing or extra:
        raise ValueError(f"route step mismatch: missing={missing}, extra={extra}")
    return [by_step[step] for step in expected_steps]


def route_yield(steps: list[StepYield], expected_steps: list[str]) -> float:
    ordered = ordered_route_steps(steps, expected_steps)
    return geometric_yield([step.fraction for step in ordered])
