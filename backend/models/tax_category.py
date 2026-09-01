from enum import Enum

class TaxCategory(str, Enum):
    FRESH_PRODUCE = "fresh_produce"
    DAIRY_PRODUCTS = "dairy_products"
    BAKERY_ITEMS = "bakery_items"
    PACKAGED_SNACKS = "packaged_snacks"
    BOTTLED_WATER = "bottled_water"
    SOFT_DRINKS = "soft_drinks"
    COFFEE_TEA = "coffee_tea"
    FROZEN_MEALS = "frozen_meals"
    CANNED_GOODS = "canned_goods"
    CONDIMENTS_SAUCES = "condiments_sauces"
    MEAT_POULTRY = "meat_poultry"
    SEAFOOD = "seafood"
    ALCOHOLIC_BEVERAGES = "alcoholic_beverages"
    TOBACCO_PRODUCTS = "tobacco_products"
    OVER_THE_COUNTER_MEDICINE = "over_the_counter_medicine"
    VITAMINS_SUPPLEMENTS = "vitamins_supplements"
    CLEANING_SUPPLIES = "cleaning_supplies"
    LAUNDRY_DETERGENT = "laundry_detergent"
    DISH_SOAP = "dish_soap"
    PAPER_TOWELS = "paper_towels"
    TOILET_PAPER = "toilet_paper"
    TRASH_BAGS = "trash_bags"
    LIGHT_BULBS = "light_bulbs"
    BATTERIES = "batteries"
    SMALL_KITCHEN_APPLIANCES = "small_kitchen_appliances"
    COOKWARE_UTENSILS = "cookware_utensils"
    DINNERWARE = "dinnerware"
    BEDDING_LINENS = "bedding_linens"
    FURNITURE = "furniture"
    HOME_DECOR = "home_decor"
    TOOLS_HARDWARE = "tools_hardware"
    PAINT_FINISHES = "paint_finishes"
    ELECTRICAL_SUPPLIES = "electrical_supplies"
    PLUMBING_SUPPLIES = "plumbing_supplies"
    LAWN_GARDEN_EQUIPMENT = "lawn_garden_equipment"
    FERTILIZER_SOIL = "fertilizer_soil"
    PLANTS_SEEDS = "plants_seeds"
    AUTOMOTIVE_PARTS = "automotive_parts"
    MOTOR_OIL = "motor_oil"
    CAR_BATTERIES = "car_batteries"
    TIRES = "tires"
    PET_FOOD = "pet_food"
    PET_TOYS_ACCESSORIES = "pet_toys_accessories"
    CLOTHING = "clothing"
    FOOTWEAR = "footwear"
    JEWELRY = "jewelry"
    WATCHES = "watches"
    SPORTING_GOODS = "sporting_goods"
    TOYS_GAMES = "toys_games"
    BOOKS_PHYSICAL = "books_physical"


# Maybe This Would Be Stored in DynamoDB and versioned later
from pydantic import BaseModel


class TaxCategoryDetails(BaseModel):
    description: str
    tax_rate: float


TAX_CATEGORY_DETAILS: dict[TaxCategory, TaxCategoryDetails] = {
    TaxCategory.FRESH_PRODUCE: TaxCategoryDetails(
        description="Fresh, unprocessed fruits and vegetables.",
        tax_rate=float("0"),
    ),
    TaxCategory.DAIRY_PRODUCTS: TaxCategoryDetails(
        description="Milk, cheese, yogurt, butter, cream, and other dairy products.",
        tax_rate=float("0"),
    ),
    TaxCategory.BAKERY_ITEMS: TaxCategoryDetails(
        description="Bread, rolls, pastries, cakes, cookies, and other baked goods.",
        tax_rate=float("0"),
    ),
    TaxCategory.PACKAGED_SNACKS: TaxCategoryDetails(
        description="Packaged snack foods such as chips, crackers, pretzels, popcorn, and snack bars.",
        tax_rate=float("0.04"),
    ),
    TaxCategory.BOTTLED_WATER: TaxCategoryDetails(
        description="Plain bottled or packaged drinking water, including still and sparkling water without sweeteners.",
        tax_rate=float("0"),
    ),
    TaxCategory.SOFT_DRINKS: TaxCategoryDetails(
        description="Sodas and other sweetened, carbonated, or flavored non-alcoholic beverages.",
        tax_rate=float("0.065"),
    ),
    TaxCategory.COFFEE_TEA: TaxCategoryDetails(
        description="Coffee, tea, coffee beans, ground coffee, tea bags, and packaged coffee or tea beverages.",
        tax_rate=float("0.04"),
    ),
    TaxCategory.FROZEN_MEALS: TaxCategoryDetails(
        description="Prepared frozen meals and entrees intended to be heated before consumption.",
        tax_rate=float("0.04"),
    ),
    TaxCategory.CANNED_GOODS: TaxCategoryDetails(
        description="Shelf-stable foods packaged in cans or jars, such as vegetables, beans, soups, and fruits.",
        tax_rate=float("0.04"),
    ),
    TaxCategory.CONDIMENTS_SAUCES: TaxCategoryDetails(
        description="Condiments, dressings, marinades, cooking sauces, and table sauces.",
        tax_rate=float("0.06"),
    ),
    TaxCategory.MEAT_POULTRY: TaxCategoryDetails(
        description="Fresh or minimally processed beef, pork, chicken, turkey, and other meat or poultry products.",
        tax_rate=float("0"),
    ),
    TaxCategory.SEAFOOD: TaxCategoryDetails(
        description="Fresh or minimally processed fish, shellfish, and other seafood.",
        tax_rate=float("0"),
    ),
    TaxCategory.ALCOHOLIC_BEVERAGES: TaxCategoryDetails(
        description="Beer, wine, spirits, and other beverages containing alcohol.",
        tax_rate=float("0.10"),
    ),
    TaxCategory.TOBACCO_PRODUCTS: TaxCategoryDetails(
        description="Cigarettes, cigars, loose tobacco, and other tobacco products.",
        tax_rate=float("0.12"),
    ),
    TaxCategory.OVER_THE_COUNTER_MEDICINE: TaxCategoryDetails(
        description="Non-prescription medicines such as pain relievers, cold medicine, allergy medicine, and antacids.",
        tax_rate=float("0.04"),
    ),
    TaxCategory.VITAMINS_SUPPLEMENTS: TaxCategoryDetails(
        description="Vitamins, minerals, nutritional supplements, and similar dietary supplement products.",
        tax_rate=float("0.04"),
    ),
    TaxCategory.CLEANING_SUPPLIES: TaxCategoryDetails(
        description="General household cleaning products such as cleaners, disinfectants, sponges, and cleaning accessories.",
        tax_rate=float("0.07"),
    ),
    TaxCategory.LAUNDRY_DETERGENT: TaxCategoryDetails(
        description="Laundry detergent, laundry pods, fabric softener, stain remover, and related laundry cleaning products.",
        tax_rate=float("0.07"),
    ),
    TaxCategory.DISH_SOAP: TaxCategoryDetails(
        description="Dishwashing liquid, dishwasher detergent, dishwasher pods, and related dish-cleaning products.",
        tax_rate=float("0.07"),
    ),
    TaxCategory.PAPER_TOWELS: TaxCategoryDetails(
        description="Disposable paper towels and similar absorbent household paper products.",
        tax_rate=float("0.07"),
    ),
    TaxCategory.TOILET_PAPER: TaxCategoryDetails(
        description="Bathroom tissue and toilet paper products.",
        tax_rate=float("0.07"),
    ),
    TaxCategory.TRASH_BAGS: TaxCategoryDetails(
        description="Disposable garbage, trash, recycling, and waste disposal bags.",
        tax_rate=float("0.07"),
    ),
    TaxCategory.LIGHT_BULBS: TaxCategoryDetails(
        description="LED, incandescent, fluorescent, and other replacement light bulbs.",
        tax_rate=float("0.07"),
    ),
    TaxCategory.BATTERIES: TaxCategoryDetails(
        description="General-purpose disposable or rechargeable batteries, excluding automotive batteries.",
        tax_rate=float("0.07"),
    ),
    TaxCategory.SMALL_KITCHEN_APPLIANCES: TaxCategoryDetails(
        description="Small powered kitchen appliances such as blenders, coffee makers, toasters, mixers, and air fryers.",
        tax_rate=float("0.085"),
    ),
    TaxCategory.COOKWARE_UTENSILS: TaxCategoryDetails(
        description="Pots, pans, baking equipment, knives, cooking utensils, and other food preparation tools.",
        tax_rate=float("0.075"),
    ),
    TaxCategory.DINNERWARE: TaxCategoryDetails(
        description="Plates, bowls, cups, glasses, flatware, and other items used to serve or consume food.",
        tax_rate=float("0.075"),
    ),
    TaxCategory.BEDDING_LINENS: TaxCategoryDetails(
        description="Sheets, blankets, comforters, pillows, towels, and other household linens.",
        tax_rate=float("0.075"),
    ),
    TaxCategory.FURNITURE: TaxCategoryDetails(
        description="Indoor or outdoor furniture such as tables, chairs, desks, sofas, beds, and shelving.",
        tax_rate=float("0.08"),
    ),
    TaxCategory.HOME_DECOR: TaxCategoryDetails(
        description="Decorative household items such as artwork, mirrors, decorative pillows, vases, and ornaments.",
        tax_rate=float("0.075"),
    ),
    TaxCategory.TOOLS_HARDWARE: TaxCategoryDetails(
        description="Hand tools, power tools, fasteners, hardware, and general construction or repair equipment.",
        tax_rate=float("0.07"),
    ),
    TaxCategory.PAINT_FINISHES: TaxCategoryDetails(
        description="Paint, primer, stain, varnish, sealant, and other surface finishing products.",
        tax_rate=float("0.07"),
    ),
    TaxCategory.ELECTRICAL_SUPPLIES: TaxCategoryDetails(
        description="Electrical wiring, outlets, switches, connectors, breakers, and related electrical installation supplies.",
        tax_rate=float("0.07"),
    ),
    TaxCategory.PLUMBING_SUPPLIES: TaxCategoryDetails(
        description="Pipes, fittings, valves, faucets, plumbing connectors, and other plumbing installation or repair supplies.",
        tax_rate=float("0.07"),
    ),
    TaxCategory.LAWN_GARDEN_EQUIPMENT: TaxCategoryDetails(
        description="Lawn and garden tools or equipment such as mowers, trimmers, hoses, rakes, and gardening tools.",
        tax_rate=float("0.07"),
    ),
    TaxCategory.FERTILIZER_SOIL: TaxCategoryDetails(
        description="Fertilizer, plant food, potting soil, topsoil, mulch, compost, and related growing materials.",
        tax_rate=float("0.07"),
    ),
    TaxCategory.PLANTS_SEEDS: TaxCategoryDetails(
        description="Live plants, flowers, shrubs, trees, bulbs, and seeds intended for planting.",
        tax_rate=float("0.07"),
    ),
    TaxCategory.AUTOMOTIVE_PARTS: TaxCategoryDetails(
        description="Replacement, repair, and maintenance parts for cars and other motor vehicles, excluding separately categorized automotive products.",
        tax_rate=float("0.08"),
    ),
    TaxCategory.MOTOR_OIL: TaxCategoryDetails(
        description="Motor oil, engine oil, and similar automotive engine lubricants.",
        tax_rate=float("0.08"),
    ),
    TaxCategory.CAR_BATTERIES: TaxCategoryDetails(
        description="Automotive starter batteries and other batteries specifically intended for motor vehicles.",
        tax_rate=float("0.08"),
    ),
    TaxCategory.TIRES: TaxCategoryDetails(
        description="New or replacement tires for cars, trucks, and other motor vehicles.",
        tax_rate=float("0.08"),
    ),
    TaxCategory.PET_FOOD: TaxCategoryDetails(
        description="Food, treats, and edible nutritional products intended for household pets.",
        tax_rate=float("0.06"),
    ),
    TaxCategory.PET_TOYS_ACCESSORIES: TaxCategoryDetails(
        description="Non-food pet products such as toys, collars, leashes, beds, bowls, litter accessories, and grooming accessories.",
        tax_rate=float("0.06"),
    ),
    TaxCategory.CLOTHING: TaxCategoryDetails(
        description="Garments and apparel such as shirts, pants, dresses, jackets, underwear, and other clothing.",
        tax_rate=float("0.07"),
    ),
    TaxCategory.FOOTWEAR: TaxCategoryDetails(
        description="Shoes, boots, sandals, slippers, and other wearable footwear.",
        tax_rate=float("0.07"),
    ),
    TaxCategory.JEWELRY: TaxCategoryDetails(
        description="Rings, necklaces, bracelets, earrings, and other decorative personal jewelry, excluding watches.",
        tax_rate=float("0.07"),
    ),
    TaxCategory.WATCHES: TaxCategoryDetails(
        description="Wristwatches, pocket watches, and other wearable timepieces.",
        tax_rate=float("0.07"),
    ),
    TaxCategory.SPORTING_GOODS: TaxCategoryDetails(
        description="Sports, exercise, fitness, and outdoor recreational equipment and accessories.",
        tax_rate=float("0.07"),
    ),
    TaxCategory.TOYS_GAMES: TaxCategoryDetails(
        description="Children's toys, board games, puzzles, dolls, action figures, and other recreational games.",
        tax_rate=float("0.065"),
    ),
    TaxCategory.BOOKS_PHYSICAL: TaxCategoryDetails(
        description="Printed physical books, including hardcover and paperback books.",
        tax_rate=float("0.04"),
    ),
}