from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PageReference:
    page: int
    operation: str = "R"


@dataclass(frozen=True)
class SimulationStep:
    time: int
    reference: PageReference
    memory: tuple[Optional[int], ...]
    fault: bool
    reference_bits: tuple[int, ...] = ()
    modified_bits: tuple[int, ...] = ()
    hand: int = 0


@dataclass(frozen=True)
class SimulationResult:
    references: tuple[PageReference, ...]
    frame_count: int
    steps: tuple[SimulationStep, ...]

    @property
    def page_faults(self) -> int:
        return sum(step.fault for step in self.steps)

    @property
    def fault_times(self) -> tuple[int, ...]:
        return tuple(step.time for step in self.steps if step.fault)


class BaseAlgorithm(ABC):
    """Common input and result handling for page-replacement algorithms."""

    algorithm_name = "Algoritmo"

    def __init__(self, references: list[PageReference], frame_count: int) -> None:
        if frame_count < 1:
            raise ValueError("El número de marcos debe ser mayor que cero.")
        if not references:
            raise ValueError("La cadena de referencia no puede estar vacía.")
        self.references = tuple(references)
        self.frame_count = frame_count
        self.memory: list[Optional[int]] = [None] * frame_count
        self.steps: list[SimulationStep] = []

    @abstractmethod
    def run(self) -> SimulationResult:
        """Run the algorithm and return a snapshot for each reference."""

    def record_step(
        self,
        time: int,
        reference: PageReference,
        fault: bool,
        reference_bits: list[int] | None = None,
        modified_bits: list[int] | None = None,
        hand: int = 0,
    ) -> None:
        self.steps.append(
            SimulationStep(
                time=time,
                reference=reference,
                memory=tuple(self.memory),
                fault=fault,
                reference_bits=tuple(reference_bits or ()),
                modified_bits=tuple(modified_bits or ()),
                hand=hand,
            )
        )

    def result(self) -> SimulationResult:
        return SimulationResult(
            references=self.references,
            frame_count=self.frame_count,
            steps=tuple(self.steps),
        )