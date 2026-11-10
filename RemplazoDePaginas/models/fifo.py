from models.base_algorithm import BaseAlgorithm, SimulationResult


class FIFO(BaseAlgorithm):
    algorithm_name = "FIFO"

    def run(self) -> SimulationResult:
        next_victim = 0
        for time, reference in enumerate(self.references, start=1):
            if reference.page in self.memory:
                self.record_step(time, reference, fault=False)
                continue

            empty_frame = self.memory.index(None) if None in self.memory else None
            if empty_frame is not None:
                self.memory[empty_frame] = reference.page
            else:
                self.memory[next_victim] = reference.page
                next_victim = (next_victim + 1) % self.frame_count
            self.record_step(time, reference, fault=True)
        return self.result()