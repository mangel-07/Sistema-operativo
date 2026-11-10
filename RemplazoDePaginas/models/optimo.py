from models.base_algorithm import BaseAlgorithm, SimulationResult


class Optimo(BaseAlgorithm):
    algorithm_name = "Óptimo"

    def run(self) -> SimulationResult:
        for index, reference in enumerate(self.references):
            if reference.page in self.memory:
                self.record_step(index + 1, reference, fault=False)
                continue

            empty_frame = self.memory.index(None) if None in self.memory else None
            if empty_frame is not None:
                self.memory[empty_frame] = reference.page
            else:
                future = [item.page for item in self.references[index + 1 :]]
                next_use = {
                    page: future.index(page) if page in future else float("inf")
                    for page in self.memory
                }
                victim = max(self.memory, key=lambda page: next_use[page])
                self.memory[self.memory.index(victim)] = reference.page
            self.record_step(index + 1, reference, fault=True)
        return self.result()