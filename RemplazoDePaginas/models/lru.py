from models.base_algorithm import BaseAlgorithm, SimulationResult


class LRU(BaseAlgorithm):
    algorithm_name = "LRU"

    def run(self) -> SimulationResult:
        last_used: dict[int, int] = {}
        for time, reference in enumerate(self.references, start=1):
            if reference.page in self.memory:
                last_used[reference.page] = time
                self.record_step(time, reference, fault=False)
                continue

            empty_frame = self.memory.index(None) if None in self.memory else None
            if empty_frame is not None:
                self.memory[empty_frame] = reference.page
            else:
                least_recent_page = min(self.memory, key=lambda page: last_used[page])
                self.memory[self.memory.index(least_recent_page)] = reference.page
            last_used[reference.page] = time
            self.record_step(time, reference, fault=True)
        return self.result()