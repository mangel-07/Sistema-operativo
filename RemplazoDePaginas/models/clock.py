from models.base_algorithm import BaseAlgorithm, SimulationResult


class Clock(BaseAlgorithm):
    algorithm_name = "Clock"

    def run(self) -> SimulationResult:
        reference_bits = [0] * self.frame_count
        hand = 0
        for time, reference in enumerate(self.references, start=1):
            if reference.page in self.memory:
                reference_bits[self.memory.index(reference.page)] = 1
                self.record_step(time, reference, fault=False, reference_bits=reference_bits, hand=hand)
                continue

            if None in self.memory:
                frame = self.memory.index(None)
                self.memory[frame] = reference.page
                reference_bits[frame] = 1
                hand = (frame + 1) % self.frame_count
            else:
                while reference_bits[hand] == 1:
                    reference_bits[hand] = 0
                    hand = (hand + 1) % self.frame_count
                self.memory[hand] = reference.page
                reference_bits[hand] = 1
                hand = (hand + 1) % self.frame_count
            self.record_step(time, reference, fault=True, reference_bits=reference_bits, hand=hand)
        return self.result()