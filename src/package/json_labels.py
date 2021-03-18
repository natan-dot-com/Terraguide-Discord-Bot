# General labels
LABEL_ID = "ID"
LABEL_TYPE = "Type"
LABEL_ITEM_ID = "Item ID"
LABEL_NAME = "Name"
LABEL_RARITY = "Rarity"
LABEL_USE_TIME = "Use time"
LABEL_VELOCITY = "Velocity"
LABEL_TOOL_SPEED = "Tool speed"
LABEL_PICKAXE_POWER = "Pickaxe power"
LABEL_HAMMER_POWER = "Hammer power"
LABEL_AXE_POWER = "Axe power"
LABEL_FISHING_POWER = "Fishing Power"
LABEL_SET_ID = "Set ID"
LABEL_DEFENSE = "Defense"
LABEL_BODY_SLOT = "Body slot"
LABEL_TOOLTIP = "Tooltip"
LABEL_RESEARCH = "Research"
LABEL_USED_IN = "Used In"
LABEL_DAMAGE = "Damage"
LABEL_MULTIPLIER = "Multiplier"
LABEL_KNOCKBACK = "Knockback"
LABEL_AVAILABLE = "Available"
LABEL_AVAILABILITY = "Availability"
LABEL_EFFECT = "Effect"
LABEL_SOURCE = "Source"
LABEL_RADIUS = "Radius"
LABEL_DESTROY_TILES = "Destroy Tiles"
LABEL_PLACEABLE = "Placeable"
LABEL_SET_PIECES = "Set Pieces"
LABEL_SET_NAME = "Set Name"
LABEL_SET_BONUS = "Set Bonus"
LABEL_MANA = "Mana"
LABEL_CRITICAL_CHANCE = "Critical chance"
LABEL_REACH = "Reach"
LABEL_HOOKS = "Hooks"
LABEL_LATCHING = "Latching"
LABEL_ORE_TIER = "Ore Tier"
LABEL_MINIMUM_PICKAXE_POWER = "Minimum Pickaxe Power"
LABEL_CONSUMED = "Is Consumed"
LABEL_ANGLER_QUOTE = "Angler Quote"
LABEL_HEIGHT = "Height"
LABEL_BIOME = "Biome"
LABEL_SOURCE = "Sources"
LABEL_RARITY_ID = "Rarity ID"
LABEL_RARITY_TIER = "Rarity Tier"
LABEL_RARITY_DESC = "Rarity Description"
LABEL_MAX_LIFE = "Max Life"
LABEL_BUY = "Buy"
LABEL_SELL = "Sell"
LABEL_BASE_VELOCITY = "Base Velocity"
LABEL_VELOCITY_MULTIPLIER = "Velocity Multiplier"
LABEL_LIGHT_PET = "Light Pet"
LABEL_BRIGHTNESS = "Brightness"
LABEL_NOTES = "Notes"
LABEL_BUFF_IMAGE = "Buff Image"
LABEL_PET_IMAGE = "Light Pet Image"
LABEL_MASTER_MODE = "Master Mode Exclusive:"
LABEL_DESCRIPTION = "Description"
LABEL_TOOLTIP = "Tooltip"
LABEL_DESTROYED_BY_EXPLOSIVES = "Destroyed by Explosives"
LABEL_BONUS = "Bonus"
LABEL_USABLE = "Usable"
LABEL_MAX_STACK = "Max stack"
LABEL_CREATES = "Creates"
LABEL_PLANTED_IN = "Planted In"
LABEL_CATCH_QUALITY = "Catch Quality"
LABEL_EVENT = "Event"
LABEL_BAIT_POWER = "Bait Power"
LABEL_SUMMONS = "Summons"
LABEL_HOUSE = "House"
LABEL_MECHANISM = "Mechanism"
LABEL_WATERPROOF = "Waterproof"
LABEL_BAG_DROPS = "Bag Drops"
LABEL_SPAWN_REQUIREMENT = "Spawn Requirement"
LABEL_DURATION = "Duration"
LABEL_BUFF = "Buff"
LABEL_BUFF_TOOLTIP = "Buff tooltip"
LABEL_CONSUMABLE = "Consumable"
LABEL_DEBUFF = "Debuff"
LABEL_DEBUFF_TOOLTIP = "Debuff tooltip"
LABEL_ENVIRONMENT = "Environment"
LABEL_AI_TYPE = "AI Type"

# Image data
IMAGE_BRICK = "Brick Image"
IMAGE_IN_STONE = "In Stone"
IMAGE_PLACED = "Placed"
IMAGE_RARITY = "Rarity Image Path"

# Item source dict
SOURCE_RECIPES = "Crafting Recipes"
SOURCE_NPC = "NPC"
SOURCE_DROP = "Drop"
SOURCE_GRAB_BAG = "Grab Bag"
SOURCE_OTHER = "Other"

# Drop dict labels ('LABEL_SOURCE' subdict)
# About Drop Dict:
    # DROP_ID: ID identifier for each structure
    # DROP_ITEM: Which item can be dropped
    # DROP_PROBABILITY: Probability value to drop
    # DROP_QUANTITY: How many does it drop
    # DROP_NPC: From which NPC it can be dropped
DROP_ID = "Drop ID"
DROP_NPC = "NPC"
DROP_ITEM = "Item Dropped"
DROP_PROBABILITY = "Probability"

# Crafting recipe labels ('LABEL_SOURCE' subdict)
# From tables.json
TABLE_RECIPES_LIST = "Table Recipes List"

# From recipes.json
# About Recipe Crafting Dict:
    # RECIPE_CRAFT_ID: ID identifier for each structure
    # RECIPE_RESULT Which item is crafted
    # RECIPE_RESULT_QUANTITY: How many it's crafted
    # RECIPE_TABLE: In which table it can be crafted
    # RECIPE_IDENTITY: Every ingredient from that recipe,
    #  containing a list of ingredient dictionaries (as it
    #  can be seen below)
RECIPE_CRAFT_ID = "Craft ID"
RECIPE_RESULT = "Result ID"
RECIPE_RESULT_QUANTITY = "Result Quantity"
RECIPE_TABLE = "Table ID"
RECIPE_IDENTITY = "Recipe"
DROP_QUANTITY = "Quantity"

# Recipe ingredient labels ('RECIPE_IDENTITY' subdict)
INGREDIENT_NAME = "Ingredient ID"
INGREDIENT_QUANTITY = "Quantity"

# Grab bag dict labels ('LABEL_SOURCE' subdict)
# From grab_bags.json
GRAB_BAGS_LOOT_LIST = "Grab Bag Loot List"

# From bag_drops.json
# About Bag Drops Dict:
    # BAG_DROP_ID: ID identifier for each structure
    # BAG_DROP_RESULT: Which item is dropped
    # BAG_DROP_PROBABILITY: Probability value to drop
    # BAG_DROP_QUANTITY: How much it can drop
    # BAG_ID: From which bag it can be dropped
BAG_DROP_ID = "Bag Drop ID"
BAG_ID = "Bag ID"
BAG_DROP_RESULT = "Drop Result"
BAG_DROP_PROBABILITY = "Probability"
BAG_DROP_QUANTITY = "Quantity"

# NPC related labels
NPC_SELL_LIST = "Selling List"

# ABout Sell Structure:
    # NPC_SELL_ID: ID identifier for each structure
    # NPC_ID: Which NPC sells
    # NPC_SELL_ITEM: Which item it sells
    # NPC_ITEM_COST: How much does it cost
    # NPC_SELL_CONDITION: In what condition does that NPC sell
NPC_SELL_ID = "Sell ID"
NPC_ID = "NPC ID"
NPC_SELL_ITEM = "Selling Item"
NPC_ITEM_COST = "Item Cost"
NPC_SELL_CONDITION = "Sell Condition"

# Table files data
BAGS_DROP_NAME_FILE = "grab_bags_drops"
BAGS_NAME_FILE = "grab_bags"
JSON_EXT = ".json"
MAIN_NAME_FILE = "items"
NPC_NAME_FILE = "npc"
RARITY_NAME_FILE = "rarity"
RECIPE_NAME_FILE = "recipes"
SELLING_LIST_NAME_FILE = "selling_list"
SET_NAME_FILE = "set"
TABLE_NAME_FILE = "crafting_stations"

# Items subfiles
MAIN_ITEM_SUBFILE_PREFIX = "items_"
ACCESSORY_NAME_FILE = "items_accessory"
AMMUNITION_NAME_FILE = "items_ammunition"
ARMOR_NAME_FILE = "items_armor"
BACKGROUND_NAME_FILE = "items_background"
BAIT_NAME_FILE = "items_bait"
BLOCK_NAME_FILE = "items_block"
BOSS_SUMMON_NAME_FILE = "items_boss_summon"
BRICK_NAME_FILE = "items_brick"
CONSUMABLE_NAME_FILE = "items_consumable"
CRAFTING_MATERIAL_NAME_FILE = "items_crafting_material"
CRITTER_NAME_FILE = "items_critter"
DYE_NAME_FILE = "items_dye"
EVENT_SUMMON_NAME_FILE = "items_event_summon"
FISHING_CATCHES_NAME_FILE = "items_fishing_catches"
FOOD_NAME_FILE = "items_food"
FURNITURE_NAME_FILE = "items_furniture"
GEM_NAME_FILE = "items_gem"
GRAB_BAG_NAME_FILE = "items_grab_bag"
HOOK_NAME_FILE = "items_hook"
KEY_NAME_FILE = "items_key"
LIGHT_PET_NAME_FILE = "items_light_pet"
LIGHT_SOURCE_NAME_FILE = "items_light_source"
ORE_NAME_FILE = "items_ore"
PAINTING_NAME_FILE = "items_painting"
POTION_NAME_FILE = "items_potion"
PYLON_NAME_FILE = "items_pylon"
QUEST_FISH_NAME_FILE = "items_quest_fish"
SEEDS_NAME_FILE = "items_seeds"
SHIELD_NAME_FILE = "items_shield"
STORAGE_NAME_FILE = "items_storage"
TOOL_NAME_FILE = "items_tool"
VANITY_NAME_FILE = "items_vanity"
WEAPON_NAME_FILE = "items_weapon"

# NPC subfiles
MAIN_NPC_SUBFILE_PREFIX = "npc_"
NPC_ENEMIES_NAME_FILE = "npc_enemy"
NPC_CRITTERS_NAME_FILE = "npc_critter"
NPC_TOWN_NAME_FILE = "npc_town"
NPC_BOSSES_NAME_FILE = "npc_boss"

# Image directories inside json folder
STATIC_IMAGE_EXT = ".png"
DYNAMIC_IMAGE_EXT = ".gif"

# Emoji files
EMOJI_NAME_FILE = "emoji_id"

IMAGE_DIR_BRICKS = "bricks_sprites/"
IMAGE_DIR_GEMS = "gems_sprites/"
IMAGE_DIR_LIGHT_PETS = "light_pets_sprites/"
IMAGE_DIR_ORES = "ores_sprites/"
IMAGE_DIR_PAINTINGS = "paintings_sprites/"
IMAGE_DIR_PYLON = "pylon_sprites/"
IMAGE_DIR_RARITY = "rarity_sprites/"
IMAGE_DIR_NPC = "npc_sprites/"

EMOJI_DIR = "terraria_emojis/"
