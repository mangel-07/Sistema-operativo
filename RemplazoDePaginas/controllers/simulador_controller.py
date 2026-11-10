from collections.abc import Callable

from models import Clock, FIFO, LRU, Optimo, SecondChance, SimulationResult
from utils.parser import parse_frame_count, parse_references


ALGORITHMS = {
    "FIFO": FIFO,
    "LRU": LRU,
    "Óptimo": Optimo,
    "Clock": Clock,
    "Segunda oportunidad (R/M)": SecondChance,
}


class SimuladorController:
    def __init__(
        self,
        get_inputs: Callable[[], tuple[str, str, str]],
        show_result: Callable[[SimulationResult, str], None],
        show_error: Callable[[str], None],
        clear_view: Callable[[], None],
    ) -> None:
        self.get_inputs = get_inputs
        self.show_result = show_result
        self.show_error = show_error
        self.clear_view = clear_view

    def simulate(self) -> None:
        references_raw, frame_count_raw, algorithm_name = self.get_inputs()
        try:
            references = parse_references(references_raw)
            frame_count = parse_frame_count(frame_count_raw)
            algorithm_type = ALGORITHMS[algorithm_name]
            result = algorithm_type(references, frame_count).run()
        except ValueError as error:
            self.show_error(str(error))
            return
        self.show_result(result, algorithm_name)

    def clear(self) -> None:
        self.clear_view()