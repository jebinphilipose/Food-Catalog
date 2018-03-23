from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Item, User, Base

# Connect to database and create database session
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy user
user1 = User(name='Dummy User', email='dummyuser@mail.com',
             picture='https://goo.gl/bz22G2')
session.add(user1)
session.commit()

# Add Fruits Category and its items
category1 = Category(name='Fruits', user_id=1)
session.add(category1)
session.commit()

item1 = Item(name='Apple',
             description='Apple, (Malus domestica), fruit of the domesticated '
             'tree Malus domestica (family Rosaceae), one of the most widely '
             'cultivated tree fruits. The apple is a pome (fleshy) fruit, in '
             'which the ripened ovary and surrounding tissue both become '
             'fleshy and edible. The apple flower of most varieties requires '
             'cross-pollination for fertilization. When harvested, apples are '
             'usually roundish, 5-10 cm (2-4 inches) in diameter, and some '
             'shade of red, green, or yellow in colour; they vary in size, '
             'shape, and acidity depending on the variety. Apples provide '
             'vitamins A and C, are high in carbohydrates, and are an '
             'excellent source of dietary fibre. Apples are eaten fresh or '
             'cooked in a variety of ways and are frequently used as a pastry '
             'filling, apple pie being perhaps the archetypal American '
             'dessert.', category=category1, user_id=1)
session.add(item1)
session.commit()

item2 = Item(name='Banana',
             description='Banana, fruit of the genus Musa, of the family '
             'Musaceae, one of the most-important fruit crops of the world. '
             'The banana is grown in the tropics, and, though it is most '
             'widely consumed in those regions, it is valued worldwide for '
             'its flavour, nutritional value, and availability throughout the '
             'year. A ripe fruit contains as much as 22 percent of '
             'carbohydrate, mainly as sugar, and is high in dietary fibre, '
             'potassium, manganese, and vitamins B6 and C. Cavendish, or '
             'dessert, bananas are most commonly eaten fresh, though they may '
             'be fried or mashed and chilled in pies or puddings. They may '
             'also be used to flavour muffins, cakes, or breads. Cooking '
             'varieties, or plantains, are starchy rather than sweet and are '
             'grown extensively as a staple food source in tropical regions. '
             'Although Cavendish bananas are by far the most-common variety '
             'imported by nontropical countries, plantain varieties account '
             'for about 85 percent of all banana cultivation worldwide.',
             category=category1, user_id=1)
session.add(item2)
session.commit()

item3 = Item(name='Mango',
             description='Mango, (Mangifera indica), member of the cashew '
             'family (Anacardiaceae) and one of the most important and widely '
             'cultivated fruits of the tropical world. The mango tree is '
             'considered indigenous to eastern Asia, Myanmar (Burma), and '
             'Assam state of India. Mangoes are a rich source of vitamins A, '
             'C, and D. The fruit varies greatly in size and character. Its '
             'form is oval, round, heart-shaped, kidney-shaped, or long and '
             'slender. The smallest mangoes are no larger than plums, while '
             'others may weigh 1.8 to 2.3 kg (4 to 5 pounds). Some varieties '
             'are vividly coloured with shades of red and yellow, while '
             'others are dull green. The single large seed is flattened, and '
             'the flesh that surrounds it is yellow to orange in colour, '
             'juicy, and of distinctive sweet-spicy flavour.',
             category=category1, user_id=1)
session.add(item3)
session.commit()

# Add Vegetables category and its items
category2 = Category(name='Vegetables', user_id=1)
session.add(category2)
session.commit()

item1 = Item(name='Carrot',
             description='Carrot, (Daucus carota), herbaceous, generally '
             'biennial plant of the Apiaceae family that produces an edible '
             'taproot. Among common varieties root shapes range from globular '
             'to long, with lower ends blunt to pointed. Besides the orange-'
             'coloured roots, white-, yellow-, and purple-fleshed varieties '
             'are known. The plants require cool to moderate temperatures and '
             'are not grown in summer in the warmer regions. They require '
             'deep, rich, but loosely packed soil. Fresh carrots should be '
             'firm and crisp, with smooth and unblemished skin. Bright-orange '
             'colour indicates high carotene content; smaller types are the '
             'most tender. Carrots are used in salads and as relishes and are '
             'served as cooked vegetables and in stews and soups.',
             category=category2, user_id=1)
session.add(item1)
session.commit()

item2 = Item(name='Tomato',
             description='Tomato, (Solanum lycopersicum), flowering plant of '
             'the nightshade family (Solanaceae), cultivated extensively for '
             'its edible fruits. Labelled as a vegetable for nutritional '
             'purposes, tomatoes are a good source of vitamin C and the '
             'phytochemical lycopene. The fruits are commonly eaten raw in '
             'salads, served as a cooked vegetable, used as an ingredient of '
             'various prepared dishes, and pickled. Additionally, a large '
             "percentage of the World's tomato crop is used for processing, "
             'products include canned tomatoes, tomato juice, ketchup, puree, '
             'paste, and "sun-dried" tomatoes or dehydrated pulp. They are '
             'usually red, scarlet, or yellow, though green and purple '
             'varieties do exist, and they vary in shape from almost '
             'spherical to oval and elongate to pear-shaped.',
             category=category2, user_id=1)
session.add(item2)
session.commit()

item3 = Item(name='Broccoli',
             description='Broccoli, Brassica oleracea, variety italica, form '
             'of cabbage, of the mustard family (Brassicaceae), grown for its '
             'edible flower buds and stalk. Native to the eastern '
             'Mediterranean and Asia Minor, sprouting broccoli was cultivated '
             'in Italy in ancient Roman times and was introduced to England '
             'and America in the 1700s. High in dietary fibre and a number of '
             'vitamins and minerals, including potassium, folic acid, and '
             'vitamins A, C, and K, broccoli is a nutritious vegetable and '
             'can be eaten fresh or cooked.Fresh broccoli should be dark '
             'green in colour, with firm stalks and compact bud clusters.',
             category=category2, user_id=1)
session.add(item3)
session.commit()

# Add Protein Category and its items
category3 = Category(name='Protein', user_id=1)
session.add(category3)
session.commit()

item1 = Item(name='Egg',
             description='Egg, the content of the hard-shelled reproductive '
             'body produced by a bird, considered as food. While the primary '
             'role of the egg obviously is to reproduce the species, most '
             'eggs laid by domestic fowl, except those specifically set aside '
             'for hatching, are not fertilized but are sold mainly for human '
             'consumption. Eggs produced in quantity come from chickens, '
             'ducks, geese, turkeys, guinea fowl, pigeons, pheasants, and '
             'quail.The whole egg is a source of high-quality protein (i.e., '
             'proteins that contain all the amino acids needed in the human '
             'diet). In addition, it is an excellent source of all vitamins '
             '(except vitamin C) and contains many essential minerals, '
             'including phosphorus and zinc.', category=category3, user_id=1)
session.add(item1)
session.commit()

item2 = Item(name='Turkey Meat', user_id=1,
             description='Turkey meat, commonly referred to as just turkey, '
             'is the meat from turkeys, typically domesticated turkeys. It is '
             'a popular poultry product, especially in North America where it '
             'is traditionally consumed as part of culturally significant '
             'events such as Thanksgiving and Christmas as well as in '
             'standard cuisine. Turkey meat, commonly referred to as just '
             'turkey, is the meat from turkeys, typically domesticated '
             'turkeys. It is a popular poultry product, especially in North '
             'America where it is traditionally consumed as part of '
             'culturally significant events such as Thanksgiving and '
             'Christmas as well as in standard cuisine. Turkey contains more '
             'protein per ounce than other meats i.e. 100 grams/4 oz of '
             'roasted turkey breast contains 21 grams of protein. Turkey '
             'contains less fat and is slightly higher in amino acids - '
             'including tryptophan, which aids sleep.', category=category3)
session.add(item2)
session.commit()

item3 = Item(name='Almond',
             description='Almonds are the seeds of the fruits cultivated from '
             'the almond tree. The scientific name of these dry fruits is '
             'Prunus dulcis. The taste of almonds ranges from sweet to bitter '
             'and both are readily available in markets.Sweet almonds are '
             'edible, while bitter ones are used for making oil, a common oil '
             'that is used to add flavor to the food. They are usually eaten '
             'raw, but many people also add them as ingredients in salads, '
             'casseroles, and other dishes. Almond milk is also a delicious '
             "beverage and is an alternative to less nutritious cow's milk. "
             'You can eat almonds directly, preferably on an empty stomach to '
             'increase and speed up the absorption of their nutrients. You '
             'can soak them in water overnight so you can eat them the next '
             'morning. Crushed almonds are also a wonderful garnish for a '
             'number of dishes.Almonds contain significant levels of copper, '
             'iron, magnesium, calcium, protein, fiber, manganese, riboflavin,'
             ' phosphorus, and quite a few healthy fats as well. A single cup '
             'of almonds has approximately 11.5 grams of fat and 5% grams of '
             'protein. Eating a whole cup of almonds also delivers 529 '
             'calories.', category=category3, user_id=1)
session.add(item3)
session.commit()

# Add Dairy Category and its items
category4 = Category(name='Dairy', user_id=1)
session.add(category4)
session.commit()

item1 = Item(name='Milk', user_id=1,
             description='Milk, liquid secreted by the mammary glands of '
             'female mammals to nourish their young for a period beginning '
             'immediately after birth. The milk of domesticated animals is '
             'also an important food source for humans, either as a fresh '
             'fluid or processed into a number of dairy products such as '
             'butter and cheese. Milk is essentially an emulsion of fat and '
             'protein in water, along with dissolved sugar (carbohydrate), '
             'minerals, and vitamins. Milk protein is of high nutritional '
             'value because it contains all the essential amino acids-i.e., '
             'those which infants cannot synthesize in the necessary '
             "quantities. Milk's mineral content includes calcium and "
             'phosphorus in quantities sufficient for normal skeletal '
             'development, but little iron. Milk contains B vitamins as well '
             'as small amounts of vitamins C and D.', category=category4)
session.add(item1)
session.commit()

item2 = Item(name='Cheese', user_id=1,
             description='Cheese, nutritious food consisting primarily of the '
             'curd, the semisolid substance formed when milk curdles, or '
             'coagulates. Curdling occurs naturally if milk is not used '
             'promptly: it sours, forming an acid curd, which releases whey, '
             'a watery fluid containing the soluble constituents; and it '
             'leaves semisolid curd, or fresh cheese. In some areas, cheese '
             'is still made simply by allowing milk to curdle naturally, or '
             'by mixing milk with juices or extracts that reduce it to curds '
             'and whey. In modern factories, cheese is mass-produced '
             'according to standardized recipes and techniques that result in '
             'a more uniform product. It is not necessarily of higher '
             'quality, and there are fewer varieties.', category=category4)
session.add(item2)
session.commit()

# Add Grains Category and its items
category5 = Category(name='Grains', user_id=1)
session.add(category5)
session.commit()

item1 = Item(name='Oats',
             description='Oats, (Avena sativa), domesticated cereal grass '
             '(family Poaceae) grown primarily for its edible starchy grains. '
             'Oats are widely cultivated in the temperate regions of the '
             'world and are second only to rye in their ability to survive in '
             'poor soils. Although oats are used chiefly as livestock feed, '
             'some are processed for human consumption, especially as '
             'breakfast foods. The plants provide good hay and, under proper '
             'conditions, furnish excellent grazing and make good silage '
             '(stalk feed preserved by fermentation). The grains are high in '
             'carbohydrates and contain about 13 percent protein and 7.5 '
             'percent fat. They are a source of calcium, iron, vitamin B1, '
             'and niacin.', category=category5, user_id=1)
session.add(item1)
session.commit()

item2 = Item(name='Rice',
             description='Rice, edible starchy cereal grain and the plant by '
             'which it is produced. Roughly one-half of the world population, '
             'including virtually all of East and Southeast Asia, is wholly '
             "dependent upon rice as a staple food; 95 percent of the world's "
             'rice crop is eaten by humans. The cultivated rice plant, Oryza '
             'sativa, is an annual grass of the Gramineae family. It grows to '
             'about 1.2 metres (4 feet) in height. The leaves are long and '
             'flattened, and its panicle, or inflorescence, is made up of '
             'spikelets bearing flowers that produce the fruit, or grain. '
             'Rice that is processed to remove only the husks, called brown '
             'rice, contains about 8 percent protein and small amounts of '
             'fats and is a source of thiamine, niacin, riboflavin, iron, and '
             'calcium. Rice that is milled to remove the bran as well is '
             'called white rice and is greatly diminished in nutrients.',
             category=category5, user_id=1)
session.add(item2)
session.commit()

# Add Oils Category and its items
category6 = Category(name='Oils', user_id=1)
session.add(category6)
session.commit()

item1 = Item(name='Avocado',
             description='Avocado, also called alligator pear, fruit of '
             'Persea americana of the family Lauraceae, a tree native to the '
             'Western Hemisphere from Mexico south to the Andean regions. '
             'Avocado fruits have greenish or yellowish flesh with a buttery '
             'consistency and a rich, nutty flavour. They are often eaten in '
             'salads, and in many parts of the world they are eaten as a '
             'dessert. Mashed avocado is the principal ingredient of '
             'guacamole, a characteristic sauce in Mexican cuisine. Avocados '
             'provide thiamin, riboflavin, and vitamin A, and in some '
             'varieties the flesh contains as much as 25 percent unsaturated '
             'oil.', category=category6, user_id=1)
session.add(item1)
session.commit()

item2 = Item(name='Olive',
             description='Olive, (Olea europaea), subtropical broad-leaved '
             'evergreen tree and its edible fruit (family Oleaceae). The tree '
             'ranges in height from 3 to 12 metres (10 to 40 feet) or more '
             'and has numerous branches. Its leaves, leathery and lance-'
             'shaped, are dark green above and silvery on the underside and '
             'are paired opposite each other on the twig. The wood is '
             'resistant to decay. If the top dies back, a new trunk '
             'will often arise from the roots. Olives tend to have maximum '
             'oil content (about 20-30 percent of fresh weight) and greatest '
             'weight six to eight months after the blossoms appear. Olives '
             'are grown mainly for the production of olive oil.',
             category=category6, user_id=1)
session.add(item2)
session.commit()

print("Categories and Items Added!")
