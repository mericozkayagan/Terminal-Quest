from .boss import Boss, BossRequirement
from .effects.item_effects import VoidShieldEffect, HopesCorruptionEffect
from .items.sets import VOID_SENTINEL_SET, HOPES_BANE_SET
from .effects.status_effects import CORRUPTED_HOPE, VOID_EMPOWERED
from .skills import Skill

# Boss ASCII Art
BOSS_ART = {
    "The Void Sentinel": """
╔══════════════════════════════════════╗
║          ▄████████████████▄          ║
║        ▄█▓▒░══════════░▒▓█▄         ║
║       ██▓█▀▀╔════════╗▀▀█▓██        ║
║      ███╔═▓░▄██████▄░▓═╗███         ║
║     ███║░▒▓███▀▀▀███▓▒░║███        ║
║     ███╚═▓▓██◆██◆██▓▓═╝███        ║
║     ██▓█╔═▒▀██████▀▒═╗█▓██        ║
║     ██░█║◆░══════░░◆║█░██         ║
║     ██░█▒██████▒▓╝█░██         ║
║      ██▄║░▓▀████▀▓░║▄██          ║
║       ██╚═▓██████▓═╝██           ║
║        █▄▄▀▀═══▀▀▄▄█            ║
║         ▀████████████▀            ║
╚══════════════════════════════════════╝""",
    "The Corrupted Prophet": """
╔══════════════════════════════════════╗
║          ▄▄████████████▄▄           ║
║        ▄█▓░╱╲██████╱╲░▓█▄          ║
║       ██▓█▀◆╚════╝◆▀█▓██          ║
║      ███╔═▓▄▄░██░▄▄▓═╗███         ║
║      ███║░▒▓█▀▀▀▀█▓▒░║███         ║
║      ▀██╚═▓▓░◆◆░▓▓▓═╝██▀         ║
║       ██║░▒▓▄▄▄▄▓▒░║██           ║
║       ██╚═░╱╲██╱╲░═╝██           ║
║       █▄▄░░░████░░░▄▄█           ║
║      ██╱▓▓▓▀▀▀▀▓▓▓╲██            ║
║     ██▌║▓▓▓░██░▓▓▓║▐██           ║
║     ██▌║▓▓▓░██░▓▓▓║▐██           ║
║      ██╲▓▓▓▄██▄▓▓╱██            ║
╚══════════════════════════════════════╝""",
}

# Boss Skills with cooldown considerations
VOID_SENTINEL_SKILLS = [
    Skill(
        name="Void Collapse",
        damage=65,
        mana_cost=40,
        description="Collapses space around targets, dealing heavy void damage",
        cooldown=2,
    ),
    Skill(
        name="Abyssal Ward",
        damage=30,
        mana_cost=25,
        description="Creates a shield that absorbs damage and reflects it",
        cooldown=3,
    ),
    Skill(
        name="Eternal Darkness",
        damage=85,
        mana_cost=60,
        description="Unleashes pure void energy in a devastating blast",
        cooldown=4,  # Longer cooldown for rage skill
    ),
]

CORRUPTED_PROPHET_SKILLS = [
    Skill(
        name="False Promise",
        damage=55,
        mana_cost=35,
        description="Inflicts mind-shattering visions of false hope",
        cooldown=2,
    ),
    Skill(
        name="Hope's Corruption",
        damage=40,
        mana_cost=30,
        description="Corrupts the target with twisted light, dealing DoT",
        cooldown=3,
    ),
    Skill(
        name="Prophecy of Doom",
        damage=75,
        mana_cost=50,
        description="Channels pure corruption in a devastating beam",
        cooldown=4,  # Rage skill with longer cooldown
    ),
]

BOSS_ENEMIES = [
    Boss(
        name="Void Sentinel",
        level=10,
        health=200,
        mana=150,
        attack=25,
        defense=15,
        title="Guardian of the Abyss",
        description="An ancient guardian corrupted by the void, wielding devastating dark powers.",
        associated_set=VOID_SENTINEL_SET,
        requirements=BossRequirement(min_player_level=1),
        special_effects=[VOID_EMPOWERED],
        skills=VOID_SENTINEL_SKILLS,
        exp_reward=2000,
        art=BOSS_ART["The Void Sentinel"],
    ),
    Boss(
        name="Corrupted Prophet",
        level=15,
        health=250,
        mana=200,
        attack=30,
        defense=12,
        title="Herald of False Hope",
        description="Once a beacon of light, now twisted by corruption into a harbinger of despair.",
        associated_set=HOPES_BANE_SET,
        requirements=BossRequirement(min_player_level=10),
        special_effects=[CORRUPTED_HOPE],
        skills=CORRUPTED_PROPHET_SKILLS,
        exp_reward=3000,
        art=BOSS_ART["The Corrupted Prophet"],
    ),
]
