import unittest

from controllers.simulador_controller import SimuladorController
from models import Clock, FIFO, LRU, Optimo, SecondChance
from utils.parser import parse_frame_count, parse_references


class ReplacementAlgorithmTests(unittest.TestCase):
    def test_reference_sequence_fault_counts(self) -> None:
        references = parse_references("7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2")
        expected = {FIFO: 10, LRU: 9, Optimo: 7, Clock: 9, SecondChance: 9}

        for algorithm, fault_count in expected.items():
            with self.subTest(algorithm=algorithm.algorithm_name):
                result = algorithm(references, 3).run()
                self.assertEqual(result.page_faults, fault_count)
                self.assertEqual(len(result.steps), len(references))
                self.assertEqual(len(result.fault_times), fault_count)

    def test_second_chance_tracks_reference_and_modified_bits(self) -> None:
        references = parse_references("1:W, 2:R, 1:R, 3:R")
        result = SecondChance(references, 2).run()

        self.assertEqual(result.steps[0].modified_bits, (1, 0))
        self.assertEqual(result.steps[2].reference_bits, (1, 1))
        self.assertEqual(result.steps[3].memory, (1, 3))
        self.assertEqual(result.steps[3].reference_bits, (0, 1))
        self.assertEqual(result.steps[3].modified_bits, (1, 0))

    def test_parser_defaults_to_reads_and_accepts_lowercase_operations(self) -> None:
        self.assertEqual(
            parse_references("2, 4:w"),
            parse_references("2:R, 4:W"),
        )

    def test_parser_rejects_empty_or_invalid_references(self) -> None:
        for raw in ("", "1,,2", "2:X", "a, 2"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                parse_references(raw)

    def test_frame_count_must_be_positive_integer(self) -> None:
        self.assertEqual(parse_frame_count("3"), 3)
        for raw in ("0", "-1", "1.5", "x"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                parse_frame_count(raw)

    def test_controller_sends_results_to_view_and_reports_invalid_input(self) -> None:
        shown = []
        errors = []
        values = ["1, 2, 1", "2", "FIFO"]
        controller = SimuladorController(
            lambda: tuple(values),
            lambda result, name: shown.append((result, name)),
            errors.append,
            lambda: None,
        )

        controller.simulate()
        self.assertEqual(shown[0][0].page_faults, 2)
        self.assertEqual(shown[0][1], "FIFO")

        values[1] = "0"
        controller.simulate()
        self.assertEqual(len(shown), 1)
        self.assertEqual(len(errors), 1)


if __name__ == "__main__":
    unittest.main()
