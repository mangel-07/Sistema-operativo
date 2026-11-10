from models.base_algorithm import BaseAlgorithm, SimulationResult


class SecondChance(BaseAlgorithm):
    """Enhanced second chance using reference and modified bits."""

    algorithm_name = "Segunda oportunidad (R/M)"

    def run(self) -> SimulationResult:
        reference_bits = [0] * self.frame_count
        modified_bits = [0] * self.frame_count
        hand = 0

        for time, reference in enumerate(self.references, start=1):
            if reference.page in self.memory:
                frame = self.memory.index(reference.page)
                reference_bits[frame] = 1
                if reference.operation == "W":
                    modified_bits[frame] = 1
                self.record_step(
                    time, reference, fault=False,
                    reference_bits=reference_bits, modified_bits=modified_bits, hand=hand,
                )
                continue

            if None in self.memory:
                frame = self.memory.index(None)
                self.memory[frame] = reference.page
                reference_bits[frame] = 1
                modified_bits[frame] = int(reference.operation == "W")
                hand = (frame + 1) % self.frame_count
            else:
                victim = self._find_victim(reference_bits, modified_bits, hand)
                self.memory[victim] = reference.page
                reference_bits[victim] = 1
                modified_bits[victim] = int(reference.operation == "W")
                hand = (victim + 1) % self.frame_count

            self.record_step(
                time, reference, fault=True,
                reference_bits=reference_bits, modified_bits=modified_bits, hand=hand,
            )

        return self.result()

    def _find_victim(
        self, reference_bits: list[int], modified_bits: list[int], hand: int
    ) -> int:
        candidate_modified: int | None = None
        for offset in range(self.frame_count):
            frame = (hand + offset) % self.frame_count
            if reference_bits[frame] == 0:
                if modified_bits[frame] == 0:
                    return frame
                if candidate_modified is None:
                    candidate_modified = frame
            else:
                reference_bits[frame] = 0

        if candidate_modified is not None:
            return candidate_modified

        for offset in range(self.frame_count):
            frame = (hand + offset) % self.frame_count
            if modified_bits[frame] == 0:
                return frame
        return hand