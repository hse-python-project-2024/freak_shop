from ..model import Deck

import unittest


class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()

    def test_add_cards(self):
        self.assertEqual(self.deck.card_ids, [])
        self.assertEqual(self.deck.vals, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(self.deck.merch_vals, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(self.deck.cats, {"Items": 0, "Pets": 0, "Employees": 0})

        self.deck.add_cards([1, 10, 20])
        self.assertEqual(self.deck.card_ids, [1, 10, 20])
        self.assertEqual(self.deck.vals, [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1])
        self.assertEqual(self.deck.merch_vals, [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(self.deck.cats, {"Items": 1, "Pets": 1, "Employees": 1})

        self.deck.add_cards([5, 11])
        self.assertEqual(self.deck.card_ids, [1, 5, 10, 11, 20])
        self.assertEqual(self.deck.vals, [0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1])
        self.assertEqual(self.deck.merch_vals, [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0])
        self.assertEqual(self.deck.cats, {"Items": 2, "Pets": 2, "Employees": 1})

        self.deck.add_cards([10, 10, 10])
        self.assertEqual(self.deck.card_ids, [1, 5, 10, 10, 10, 10, 11, 20])
        self.assertEqual(self.deck.vals, [0, 1, 0, 1, 0, 4, 1, 0, 0, 0, 1])
        self.assertEqual(self.deck.merch_vals, [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0])
        self.assertEqual(self.deck.cats, {"Items": 2, "Pets": 5, "Employees": 1})

    def test_sell_cards(self):
        self.deck.add_cards([1, 5, 10, 10, 10, 10, 11, 20])

        self.deck.sell_cards([5, 10])
        self.assertEqual(self.deck.card_ids, [1, 10, 10, 10, 11, 20])
        self.assertEqual(self.deck.vals, [0, 1, 0, 0, 0, 3, 1, 0, 0, 0, 1])
        self.assertEqual(self.deck.merch_vals, [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0])
        self.assertEqual(self.deck.cats, {"Items": 1, "Pets": 4, "Employees": 1})

        self.deck.sell_cards([11, 10])
        self.assertEqual(self.deck.card_ids, [1, 10, 10, 20])
        self.assertEqual(self.deck.vals, [0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 1])
        self.assertEqual(self.deck.merch_vals, [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(self.deck.cats, {"Items": 1, "Pets": 2, "Employees": 1})

        self.deck.sell_cards([10, 10])
        self.assertEqual(self.deck.card_ids, [1, 20])
        self.assertEqual(self.deck.vals, [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1])
        self.assertEqual(self.deck.merch_vals, [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(self.deck.cats, {"Items": 1, "Pets": 0, "Employees": 1})

        self.deck.sell_cards([1, 20])
        self.assertEqual(self.deck.card_ids, [])
        self.assertEqual(self.deck.vals, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(self.deck.merch_vals, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(self.deck.cats, {"Items": 0, "Pets": 0, "Employees": 0})

    def test_check_a_tidy_mansion(self):
        self.assertEqual(self.deck.check_a_tidy_mansion(), 0)

        self.deck.add_cards([1, 3, 5])
        self.assertEqual(self.deck.check_a_tidy_mansion(), 3)
        self.deck.sell_cards([1, 3, 5])

        self.deck.add_cards([10, 11, 14])
        self.assertEqual(self.deck.check_a_tidy_mansion(), 5)
        self.deck.sell_cards([10, 11, 14])

        self.deck.add_cards([15, 17, 19])
        self.assertEqual(self.deck.check_a_tidy_mansion(), 7)
        self.deck.sell_cards([15, 17, 19])

        self.deck.add_cards([14, 15, 16])
        self.assertEqual(self.deck.check_a_tidy_mansion(), 0)
        self.deck.sell_cards([14, 15, 16])

        self.deck.add_cards([10, 11, 14, 15, 17, 19])
        self.assertEqual(self.deck.check_a_tidy_mansion(), 12)

    def test_check_obsessed_by_arrangement(self):
        self.assertEqual(self.deck.check_obsessed_by_arrangement(), 0)

        self.deck.add_cards([1, 5, 9, 13, 17])
        self.assertEqual(self.deck.check_obsessed_by_arrangement(), 3)
        self.deck.sell_cards([1, 5, 9, 13, 17])

        self.deck.add_cards([1, 1, 2])
        self.assertEqual(self.deck.check_obsessed_by_arrangement(), 3)
        self.deck.sell_cards([1, 1, 2])

        self.deck.add_cards([1, 3, 5, 15, 17, 19])
        self.assertEqual(self.deck.check_obsessed_by_arrangement(), 9)
        self.deck.sell_cards([1, 3, 5, 15, 17, 19])

        self.deck.add_cards([1, 3, 5, 7, 9, 11, 13, 15, 17, 19])
        self.assertEqual(self.deck.check_obsessed_by_arrangement(), 30)
        self.deck.sell_cards([1, 3, 5, 7, 9, 11, 13, 15, 17, 19])

    def test_check_gem_of_my_collection(self):
        self.assertEqual(self.deck.check_gem_of_my_collection(), 0)

        self.deck.add_cards([11, 11])
        self.assertEqual(self.deck.check_gem_of_my_collection(), 18)
        self.deck.sell_cards([11, 11])

        self.deck.add_cards([1, 1, 11, 11])
        self.assertEqual(self.deck.check_gem_of_my_collection(), 3)
        self.deck.sell_cards([1, 1, 11, 11])

    def test_collector(self):
        self.assertEqual(self.deck.check_collector(), 0)

        self.deck.add_cards([1])
        self.assertEqual(self.deck.check_collector(), 3)
        self.deck.sell_cards([1])

        self.deck.add_cards([1, 2])
        self.assertEqual(self.deck.check_collector(), 3)
        self.deck.sell_cards([1, 2])

        self.deck.add_cards([1, 2, 4])
        self.assertEqual(self.deck.check_collector(), 6)
        self.deck.sell_cards([1, 2, 4])

        self.deck.add_cards([1, 2, 4, 6])
        self.assertEqual(self.deck.check_collector(), 9)
        self.deck.sell_cards([1, 2, 4, 6])

        self.deck.add_cards([1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
        self.assertEqual(self.deck.check_collector(), 30)
        self.deck.sell_cards([1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20])


if __name__ == "__main__":
    print("\n")
    print(("=" * 20) + "\nTest Deck\n" + ("=" * 20))
    unittest.main()
