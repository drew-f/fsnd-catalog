from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dbsetup import Base, Category, Book, User

engine = create_engine('postgresql://catalog:cat123@127.0.0.1/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine, autoflush=True)
db = DBSession()

thriller = Category(name='Thriller')
romance = Category(name='Romance')
literature = Category(name='Literature')

db.add(thriller)
db.add(romance)
db.add(literature)
db.commit()

user = User(email="d@dkf.id.au",
            name="Drew")
db.add(user)
db.commit()

book1 = Book(title="Off the Grid",
            isbn="0399176608",
            author="C.J. Box",
            description="Nate Romanowski is off the grid, recuperating from wounds and trying to deal with past crimes, when he is suddenly surrounded by a small team of elite professional special operators. They're not there to threaten him, but to make a deal. They need help destroying a domestic terror cell in Wyoming's Red Desert, and in return they'll make Nate's criminal record disappear.\r\n\r\nBut they are not what they seem, as Nate's friend Joe Pickett discovers. They have a much different plan in mind, and it just may be something that takes them all down-including Nate and Joe.",
            image="http://ecx.images-amazon.com/images/I/51tLt%2BogLSL._SX329_BO1,204,203,200_.jpg",
            category_id=thriller.id,
            owner_id = 1
            )

book2 = Book(title="After You",
            isbn="0525426590",
            author="Jojo Moyes",
            description="How do you move on after losing the person you loved? How do you build a life worth living?\r\n\r\nLouisa Clark is no longer just an ordinary girl living an ordinary life. After the transformative six months spent with Will Traynor, she is struggling without him. When an extraordinary accident forces Lou to return home to her family, she can't help but feel she's right back where she started.\r\n\r\nHer body heals, but Lou herself knows that she needs to be kick-started back to life. Which is how she ends up in a church basement with the members of the Moving On support group, who share insights, laughter, frustrations, and terrible cookies. They will also lead her to the strong, capable Sam Fielding-the paramedic, whose business is life and death, and the one man who might be able to understand her. Then a figure from Will's past appears and hijacks all her plans, propelling her into a very different future. . . .\r\n\r\nFor Lou Clark, life after Will Traynor means learning to fall in love again, with all the risks that brings. But here Jojo Moyes gives us two families, as real as our own, whose joys and sorrows will touch you deeply, and where both changes and surprises await.",
            image="http://ecx.images-amazon.com/images/I/51-Uk8hOQNL._SX329_BO1,204,203,200_.jpg",
            category_id=romance.id,
            owner_id = 1
            )

book3 = Book(title="The Little Red Chairs",
            isbn="0316378232",
            author="Edna O'Brien",
            description="One night, in the dead of winter, a mysterious stranger arrives in the small Irish town of Cloonoila. Broodingly handsome, worldly, and charismatic, Dr. Vladimir Dragan is a poet, a self-proclaimed holistic healer, and a welcome disruption to the monotony of village life. Before long, the beautiful black-haired Fidelma McBride falls under his spell and, defying the shackles of wedlock and convention, turns to him to cure her of her deepest pains.\r\n\r\nThen, one morning, the illusion is abruptly shattered. While en route to pay tribute at Yeats's grave, Dr. Vlad is arrested and revealed to be a notorious war criminal and mass murderer. The Cloonoila community is devastated by this revelation, and no one more than Fidelma, who is made to pay for her deviance and desire. In disgrace and utterly alone, she embarks on a journey that will bring both profound hardship and, ultimately, the prospect of redemption.\r\n\r\nMoving from Ireland to London and then to The Hague, THE LITTLE RED CHAIRS is Edna O'Brien's first novel in ten years -- a vivid and unflinching exploration of humanity's capacity for evil and artifice as well as the bravest kind of love.",
            image="http://ecx.images-amazon.com/images/I/510g%2ByfHtnL._SX320_BO1,204,203,200_.jpg",
            category_id=literature.id,
            owner_id = 1
            )

book4 = Book(title="Private Paris",
            isbn="0316407054",
            author="James Patterson",
            description="When Jack Morgan stops by Private's Paris office, he envisions a quick hello during an otherwise relaxing trip. But Jack is quickly pressed into duty after getting a call from his client Sherman Wilkerson, asking Jack to track down his young granddaughter, who is on the run from a brutal drug dealer. Before Jack can locate her, several members of France's cultural elite are found dead-murdered in stunning, symbolic fashion. The only link between the crimes is a mysterious graffiti tag. As religious and ethnic tensions simmer in the City of Lights, only Jack and his Private team can connect the dots before the smoldering powder keg explodes.",
            image="http://ecx.images-amazon.com/images/I/51PlosBPiiL._SX319_BO1,204,203,200_.jpg",
            category_id=thriller.id,
            owner_id = 1
            )

book5 = Book(title="The Girl on the Train",
            isbn="1594633665",
            author="Paula Hawkins",
            description="EVERY DAY THE SAME\r\nRachel takes the same commuter train every morning and night. Every day she rattles down the track, flashes past a stretch of cozy suburban homes, and stops at the signal that allows her to daily watch the same couple breakfasting on their deck. She's even started to feel like she knows them. Jess and Jason, she calls them. Their life-as she sees it-is perfect. Not unlike the life she recently lost.\r\n\r\nUNTIL TODAY\r\nAnd then she sees something shocking. It's only a minute until the train moves on, but it's enough. Now everything's changed. Unable to keep it to herself, Rachel goes to the police. But is she really as unreliable as they say? Soon she is deeply entangled not only in the investigation but in the lives of everyone involved. Has she done more harm than good?",
            image="http://ecx.images-amazon.com/images/I/51kf7XbQ2lL._SX336_BO1,204,203,200_.jpg",
            category_id=thriller.id,
            owner_id = 1
            )

book6 = Book(title="All the Light We Cannot See",
            isbn="1476746583",
            author="Anthony Doerr",
            description="Marie-Laure lives with her father in Paris near the Museum of Natural History, where he works as the master of its thousands of locks. When she is six, Marie-Laure goes blind and her father builds a perfect miniature of their neighborhood so she can memorize it by touch and navigate her way home. When she is twelve, the Nazis occupy Paris and father and daughter flee to the walled citadel of Saint-Malo, where Marie-Laure's reclusive great-uncle lives in a tall house by the sea. With them they carry what might be the museum's most valuable and dangerous jewel.\r\n\r\nIn a mining town in Germany, the orphan Werner grows up with his younger sister, enchanted by a crude radio they find. Werner becomes an expert at building and fixing these crucial new instruments, a talent that wins him a place at a brutal academy for Hitler Youth, then a special assignment to track the resistance. More and more aware of the human cost of his intelligence, Werner travels through the heart of the war and, finally, into Saint-Malo, where his story and Marie-Laure's converge.",
            image="http://ecx.images-amazon.com/images/I/51mFEb5%2BieL._SX331_BO1,204,203,200_.jpg",
            category_id=literature.id,
            owner_id = 1
            )

book7 = Book(title="Fool Me Once",
            isbn="0525955097",
            author="Harlan Coben",
            description="Former special ops pilot Maya, home from the war, sees an unthinkable image captured by her nanny cam while she is at work: her two-year-old daughter playing with Maya's husband, Joe-who was brutally murdered two weeks earlier. The provocative question at the heart of the mystery: Can you believe everything you see with your own eyes, even when you desperately want to? To find the answer, Maya must finally come to terms with deep secrets and deceit in her own past before she can face the unbelievable truth about her husband-and herself.",
            image="http://ecx.images-amazon.com/images/I/5163%2BSkUKBL._SX329_BO1,204,203,200_.jpg",
            category_id=thriller.id,
            owner_id = 1
            )

db.add(book1)
db.add(book2)
db.add(book3)
db.add(book4)
db.add(book5)
db.add(book6)
db.add(book7)
db.commit()
