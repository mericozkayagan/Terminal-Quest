import unittest
from src.utils.ascii_art import convert_pixel_art_to_ascii, load_ascii_art, display_ascii_art
from src.services.combat import calculate_damage, process_status_effects
from src.models.character import Player, Enemy
from src.models.character_classes import CharacterClass
from src.models.skills import Skill
from src.models.status_effects import BLEEDING, POISONED, WEAKENED, BURNING, CURSED

class TestAsciiArt(unittest.TestCase):

    def test_convert_pixel_art_to_ascii(self):
        pixel_art = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]
        ]
        expected_ascii_art = " # \n###\n # \n"
        ascii_art = convert_pixel_art_to_ascii(pixel_art)
        self.assertEqual(ascii_art, expected_ascii_art)

    def test_load_ascii_art(self):
        filename = "test_art.txt"
        with open(filename, "w") as file:
            file.write("Test ASCII Art")
        loaded_art = load_ascii_art(filename)
        self.assertEqual(loaded_art, "Test ASCII Art")
        os.remove(filename)

    def test_display_ascii_art(self):
        ascii_art = "Test ASCII Art"
        display_ascii_art(ascii_art)  # This function just prints the art, so no assertion needed

class TestEnvironmentalEffects(unittest.TestCase):

    def setUp(self):
        self.player = Player("Hero", CharacterClass(
            name="Test Class",
            description="A class for testing",
            base_health=100,
            base_attack=10,
            base_defense=5,
            base_mana=50,
            skills=[Skill(name="Test Skill", damage=20, mana_cost=10, description="A test skill")]
        ))
        self.enemy = Enemy("Test Enemy", 50, 8, 3, 20, 10)

    def test_calculate_damage(self):
        damage = calculate_damage(self.player, self.enemy, 0)
        self.assertTrue(10 <= damage <= 16)  # Considering randomness range

    def test_process_status_effects(self):
        self.player.status_effects = {
            "Bleeding": BLEEDING,
            "Poisoned": POISONED
        }
        messages = process_status_effects(self.player)
        self.assertIn("Hero is affected by Bleeding", messages)
        self.assertIn("Hero is affected by Poisoned", messages)

if __name__ == '__main__':
    unittest.main()
