import asyncio
from pathlib import Path
import pygame

# Change these settings to give your game its own look and feel.
WIDTH, HEIGHT = 1450, 874
BASE_DIR = Path(__file__).parent
ASSET_DIR = BASE_DIR / "assets"
TEXT_DIR = BASE_DIR / "text"

iv = []
books = []

class NPC:
    def __init__(self, name, speech, value):
        self.name = name
        self.speech = speech
        self.value = value

class Guess:
    def __init__(self, name, value, speech=None):
        self.name = name
        self.value = value
        self.speech = speech

class Treasure:
    def __init__(self, name, description, value, status=None):
        self.name = name
        self.description = description
        self.value = value
        self.status = status

class Book:
    def __init__(self, name, description, value):
            self.name = name
            self.description = description

class Bell:
   def __init__(self, name, value):
            self.name = name
            self.value = value

class Item:
    def __init__(self, name, speech, value):
            self.name = name
            self.speech = speech
            self.value = value

class Color:
   def __init__(self, name, speech, value):
            self.name = name
            self.speech = speech
            self.value = value

class Food:
    def __init__(self, name):
        self.name = name

class Envlope:
    def __init__(self, name, speech, speech2, speech3):
        self.name = name
        self.speech = speech
        self.speech2 = speech2
        self.speech3 = speech3

class Fire:
    def __init__(self, name, speech):
        self.name = name
        self.speech = speech

class Room:
    def __init__(self, name, description, enter_sound=None):
        self.name = name
        self.description = description
        self.enter_sound = enter_sound
        self.neighbors = {}
        self.treasure = []
        self.monster = None
        self.weapon = None
        self.npc = []
        self.food = []
        self.book = []

    def add_neighbor(self, direction, room):
        self.neighbors[direction] = room

    def get_neighbor(self, direction):
        return self.neighbors.get(direction)

    def list_exits(self):
        return ", ".join(self.neighbors.keys())

class TextAdventure:
    def __init__(self):
        self.messages = []
        self.current_input = ""
        self.score = 0
        self.best_weapon_damage = 3
        self.game_over = False

        self.sounds = {
            "Open": pygame.mixer.Sound(ASSET_DIR / "move.ogg"),
            "move": pygame.mixer.Sound(ASSET_DIR / "move.ogg"),
            "pickup": pygame.mixer.Sound(ASSET_DIR / "pickup.ogg"),
            "danger": pygame.mixer.Sound(ASSET_DIR / "danger.ogg"),
            "win": pygame.mixer.Sound(ASSET_DIR / "win.ogg"),
            "organ": pygame.mixer.Sound(ASSET_DIR / "organ.ogg"),
            "bell": pygame.mixer.Sound(ASSET_DIR / "bell.ogg"),
            "door1": pygame.mixer.Sound(ASSET_DIR / "door1.ogg"),
            "door2": pygame.mixer.Sound(ASSET_DIR / "door2.ogg"),
            "fire": pygame.mixer.Sound(ASSET_DIR / "fire.ogg"),
            "birds": pygame.mixer.Sound(ASSET_DIR / "birds.ogg"),
            "flame": pygame.mixer.Sound(ASSET_DIR / "flame.ogg")
        }

        #add Rooms
        chaple = Room(
            "All Saints Chapel",
            "The sheer scale of the gothic architecture presses in: soaring stone archways stretch upward, gorgeous stained glass glows as the sun hits the windows at the right angle, and the ambient scent of old hymnals and polished wood fills your lungs. Your attention fades from the building towards the organist.")
        quad = Room(
            "The Quad",
            "You step onto the Quad, a wide grassy space surrounded by Sewanee’s stone buildings. With the campus empty, the paths and benches are completely still, making the Quad feel peaceful but a little strange. A few benches sit beneath the trees, and academic buildings surround the open lawn. On one bench, you notice a professor with a notebook beside a small sign that reads “Riddle of the Day“.")
        library = Room(
            "DuPont Library",
            "Walking up to the library you see a stone building with complex architecture, as you walk inside you see piles of colored books everywhere, they are sprawled all over the floor and tables. There is a very flustered Librarian trying to sort through everything.")
        breslin = Room(
            "Breslin Tower",
            "As you walk up to the front door, you quickly realize the door handles have a chain around them with a lock that has a number key pad. HINT: what year was The University of the South founded")
        clurg = Room(
            "McClurg Dining Hall",
            "The smell of fresh food and the view of rows of completely empty tables, and the usual sounds of conversation and dishes are gone. The food stations are still up around the room, making the silence feel even stranger. Near the entrance, one person sits at a desk with computers and an ID scanner, waiting he adons a name tag stating his name is Jack.")
        svfd = Room(
            "Sewanee Volunteer Fire Department Station 1",
            "As you approach the Sewanee Volunteer Fire Department, you hear the sound of an alarm echoing through the station. Firefighters are rushing around, preparing to respond to an emergency. Before you can take a closer look, someone calls out to you, it's the Fire Chief. “Well, look what we have here! We could use an extra set of hands. We’ve just received a call about a fire at Johnson Hall. Head over there quick!")
        bishop = Room(
            "Bishop's Common",
            "You approach Bishop Commons and briskly walk inside, excited to see what dorm you will be living in! As you walk inside you follow the signs directing you to talk to the reslife office.")
        benny = Room(
            "Benedict Hall",
            "You arrive at Benny Hall and reach for the main door but its locked. You are prompted to use your key", "door1")
        alley = Room(
            "Abo's Alley",
            "Hidden in the mountains of Sewanee, Abo’s Ally is a narrow passageway surrounded by thick trees and old stone walls. Locals say strange noises echo through the alley after dark, and students who enter sometimes disappear for hours. As you walk down the path you notice a birdwatcher enjoying the view.", "birds")
        cross = Room(
            "The War Memorial Cross",
            "Welcome to the War Memorial Cross! This is the most beautiful place on the domain, so beautiful in fact it is said that angels dwell here, and a great place to watch the sunset overlooking the valley. There is no achievement here but remember this place you might want to come back!")
        homestyle = Room(
            "the Homestyle line today we are serving, Halal Baked Chicken, Jerk Pork Chops, Basmati Rice, Steamed Green Beans, and Local Sauteed Squash. Take one item by typing take and then the name of the item! Make sure you go check out the Pasta line!", "")
        pasta = Room(
            "the Pasta line today we are serving, Daily Pasta, Halal Chicken, Meatballs, Alfredo Sauce, and Marinara Sauce. Make sure you go check out the Vegan line!", "")
        vegan = Room(
            "the Vegan line today we are serving, Fried Rice, Coconut Curry Plant Based Meatballs, Agave Roasted Carrots, Fingerling Potatoes, Roasted Chickpeas, Rice noodles, and Vegetable Broth. Make sure you go check out the soup line!", "")
        soup = Room(
            "the Soup line today we are serving, Thai Curry Pork and Cowboy Chili. one you are done go talk to Jack, he always loves to see what people put together!", "")
        desk = Room(
            "the reception desk. As you walk over to the reception desk you realize you might have bitten off more than you could chew. There is a huge pile that completely covers the desk. The only reason you can see it is the correct spot is because it says 'Reception Desk' in big letters above the pile. There is a mixed array of red, orange, and yellow books. Start off my sorting the books.", "") 
        room = Room(
            "Benny Room 102",
            "You approach a door marked 102 and are prompted to use your key again", "door2")
        johnson = Room(
            "Johnson Hall",
            "Flames are pouring from the windows of the 100 year old residence hall. A group of students has gathered outside, watching anxiously as smoke rises above the building. The fire engine is ready, and someone hands you hose. Go in and fight the fire!", "flame")

        #add Map
        chaple.add_neighbor("west", quad)
        chaple.add_neighbor("east", clurg)
        chaple.add_neighbor("south", alley)
        chaple.add_neighbor("north", svfd)
        clurg.add_neighbor("west", chaple)
        clurg.add_neighbor("southwest", alley)
        clurg.add_neighbor("southeast", cross)
        quad.add_neighbor("east", chaple)
        quad.add_neighbor("west", breslin)
        quad.add_neighbor("north", library)
        quad.add_neighbor("south", alley)
        breslin.add_neighbor("north", bishop)
        breslin.add_neighbor("east", quad)
        breslin.add_neighbor("southeast", alley)
        library.add_neighbor("south", quad)
        library.add_neighbor("west", bishop)
        library.add_neighbor("east", svfd)
        bishop.add_neighbor("west", benny)
        bishop.add_neighbor("south", breslin)
        bishop.add_neighbor("east", library)
        benny.add_neighbor("east", bishop)
        svfd.add_neighbor("west", library)
        svfd.add_neighbor("south", chaple)
        alley.add_neighbor("north", chaple)
        alley.add_neighbor("northwest", quad)
        alley.add_neighbor("west", breslin)
        alley.add_neighbor("northeast", clurg)
        cross.add_neighbor("northwest", clurg)
        clurg.add_neighbor("homestyle", homestyle)
        homestyle.add_neighbor("pasta", pasta)
        pasta.add_neighbor("vegan", vegan)
        vegan.add_neighbor("soup", soup)
        soup.add_neighbor("west", chaple)
        soup.add_neighbor("southwest", alley)
        soup.add_neighbor("southeast", cross)
        library.add_neighbor("desk", desk)
        desk.add_neighbor("west", bishop)
        desk.add_neighbor("south", quad)
        desk.add_neighbor("east", svfd)
        benny.add_neighbor("102", room)
        room.add_neighbor("east", bishop)
        svfd.add_neighbor("johnson", johnson)
        johnson.add_neighbor("firestation", svfd)

        #add NPCs
        chaple.npc.append(NPC("organist", "You’re finally awake. You’re in All Saints’ Chapel at Sewanee: the University of the South! This Chapel sits near the center of campus, so it’s a good place to get your bearings. There are four exits out of here: McClurg to the east, the Quad to the west, Abo's Ally to the south, and the firestation to the north; each place has a task for you to complete and you must complete all of the tasks.", 1))
        clurg.npc.append(NPC("jack", "Welcome to McClurg. This is Sewanee’s main dining hall. Campus is empty right now. Usually this place is packed. Since you’re here, I’ve got a challenge for you I’ll give you a meal to put together. You’ll need to find each station that has each part of the meal take one item from Homestyle, Pasta, Salad, and Vegan. Come back and talk to me when you have your meal and your McClurg task is complete. Heres a tip, always start at homestyle.", 0))
        soup.npc.append(NPC("jack", "Would you look at that! That’s quite the spread!! I love the variety from each line! To continue on your adventure head west to get back to All Saints Chapel, southwest to Abo's Alley or southeast to get to the cross", 1))
        quad.npc.append(NPC("professor", "Welcome to the Quad. People usually come out here to study, relax, or just take a break between classes. Your Quad task is simple. Slow down for a minute and solve the riddle of the day: What has many keys but can’t open a single lock? HINT: type guess and then your answer", 0))
        quad.npc.append(NPC("painter", "Hey there, welcome to the Quad. I’ve been here for a few hours working on my painting of Breslin Tower. Have you explored inside yet? If not, go have a look. It's an interesting place to the west. What dorm are you in? If you haven’t been to reslife go to bishops commons which is in the west of the library and north of Breslin.", 0))
        breslin.npc.append(NPC("bellman", "Welcome to Breslin Tower, trust me the stairs are not going to break. They may look like they are a thousand years old but they’ve been holding me up for the past 20 years. To get your achievement you have to ring the bell! ", 0))
        bishop.npc.append(NPC("reslife", "Welcome to Sewanee! You are Alex Grant right? I've got your room key and student id right here! you will be living in Benedict Hall, or as most students call it Benny! First take your key and then head west to get to Benedict Hall!", 0))
        alley.npc.append(NPC("birdwatcher", "Hi there my name is Abby and I am a birdwatcher want to hear a riddle? I have wings but I’m not a plane. I can repeat what you say, but I am not a person. What am I?", 0))
        library.npc.append(NPC("librarian", "Hey there, welcome to the DuPont Library. I am so sorry this place looks like a tornado just came through here! Everyone had their midterm so everyone was studying here for either their exams or writing their papers! Do you mind helping me sort these by color? Everything is organized by color so no need to worry about the subject or content, you just need to know the rainbow! Why don’t you work on the pile on the reception desk? The way this works: Red: Basement, Orange: 1st Floor, and Yellow: 2nd Floor. Just bring the correct colored book to the right floor and once you're done check in with me. Head over to the desk to get started.", 0))
        desk.npc.append(NPC("librarian", "You did it and the Reception Desk looks so nice and clean now! Bishops Commons is to the West of the Library, and the Quad is South and the Fire Station is east.", 1))
        cross.npc.append(NPC("angels", "Congratulations on completing all your achievements! There is a small envelope resting at the base of the cross with your name written across the front. Go ahead, open it!", 1))
        svfd.npc.append(NPC("chief", "Now that’s what I call a successful first call! You’ve handled yourself incredibly well. I think you’ve got what it takes to join the Sewanee Volunteer Fire Department, one of the only student-run fire departments in the country! Head west from here to check out the library or south to get to All Saints Chapel.", 1))

        #add book
        quad.book = Book("notebook", "Your Quad task is simple. Slow down for a minute and solve the riddle of the day: What has many keys but can’t open a single lock?", 0)
        desk.book = Book("books", "Well done! Now that you have sorted all the books by colors you need to take them to their respective floors. HINT: type the floor (basement, first or second) followed by the color of the books you must take there (red, orange or yellow)", 0)

        #add bell
        breslin.bell = Bell("bell", 1)

        #add floor
        desk.color = Color("red", "Correct! Make sure you brought books up to the fist floor and the second floor. If you have finished all 3 go tell the librarian!", 1)
        desk.color = Color("orange", "Correct! Make sure you brought books up to the second floor and down to the basement. If you have finished all 3 go tell the librarian!", 1)
        desk.color = Color("yellow", "Correct! Make sure you brought books up to the fist floor and down to the basement. If you have finished all 3 go tell the librarian!", 1)
        
        #add item
        benny.item = Item("key", "You walk through the front door into to the court yard surrounded by about 50 doors. You look at the key you were given and see your room number is 102. You spot a door marked with this number a little ways away.", 0)
        room.item = Item("key", "You open the door and step in to your home for the next year! In the first room there are 2 desks and a bathroom which leads to your suitmate's room. You walk farther into your room and see a second room with 2 bed and 2 closets. You drop off your bags and head out for your next adventure. Go east to get back to Bishop's Common and get back to central campus!", 1)

        #add fire
        johnson.fire = Fire("fire", "The water rushes through the hose, spraying across the building. Slowly, the flames begin to disappear until the last bit of smoke clears. The students outside cheer as the emergency comes to an end. Head back to the firestation, the chief want to talk to you!")

        #add envlope
        cross.envlope = Envlope("envelope", "You rip open the envelope and open the letter inside which reveals this letter:", "Dear Alex,", "Congratulations! we are pleased to welcome you to the University of the South! We hope your journey across campus has given you a glimpse of what makes Sewanee so special. We look forward to welcoming you to the mountain and seeing all that you accomplish here. Welcome to Sewanee!")
        #add food
        homestyle.food.extend([
            Food("chicken"),
            Food("pork"),
            Food("rice"),
            Food("beans"),
            Food("squash"),
            Food("halal"),
            Food("baked"),
            Food("jerk"),
            Food("basmati"),
            Food("green"),
            Food("local"),
            Food("sauteed"),
            Food("steamed")])

        pasta.food.extend([
            Food("pasta"),
            Food("chicken"),
            Food("meatballs"),
            Food("alfredo"),
            Food("marinara"),
            Food("daily"),
            Food("halal"),
            Food("sauce")])

        vegan.food.extend([
            Food("rice"),
            Food("curry"),
            Food("meatballs"),
            Food("broth"),
            Food("noodles"),
            Food("potatoes"),
            Food("chickpeas"),
            Food("carrots"),
            Food("fried"),
            Food("coconut"),
            Food("plant"),
            Food("agave"),
            Food("roasted"),
            Food("fingerling"),
            Food("vegtable"),])

        soup.food.extend([
            Food("curry"),
            Food("port"),
            Food("thai"),
            Food("cowboy"),
            Food("soup"),
            Food("pork"),
            Food("chili")])

        quad.treasure.extend([
            Treasure("diamond", "text here", 1),
            Treasure("coin", "Text here", 1),])
        bishop.treasure.append(Treasure("key", "", 0,))

        #add guess
        quad.guess = Guess("piano", 1, "Well done! If you havent yet go talk to my painter friend she'll help you find out where to go next")
        alley.guess = Guess("parrot", 1, "You got it! Enjoy Abo’s Alley! When you are ready to head out Breslin tower is to the west, the quad is northwest, All Saints Chapel is north and McClurg Dining hall is northeast.")
        breslin.guess = Guess("1857", 0, "The doors creak open as you step foot inside the tower. You see an ornate spiral staircase that looks like it is going to break as soon as you put one foot on the first stair rung. The stairs look like they lead to a trapped door. You also see a bellman standing in the tower.")
        chaple.guess = Guess("cross", 1, "Correct! Now head to the cross and talk to the angels!")
        clurg.guess = Guess("cross", 1, "Correct! Now head to the cross and talk to the angels!")
        homestyle.guess = Guess("cross", 1, "Correct! Now head to the cross and talk to the angels!")
        benny.guess = Guess("cross", 1, "Correct! Now head to the cross and talk to the angels!")
        room.guess = Guess("cross", 1, "Correct! Now head to the cross and talk to the angels!")
        svfd.guess = Guess("cross", 1, "Correct! Now head to the cross and talk to the angels!")
        bishop.guess = Guess("cross", 1, "Correct! Now head to the cross and talk to the angels!")
        library.guess = Guess("cross", 1, "Correct! Now head to the cross and talk to the angels!")
        desk.guess = Guess("cross", 1, "Correct! Now head to the cross and talk to the angels!")


        self.current_room = chaple
        self.play_sound("organ")
        self.say("You wake up gasping against the polished oak of a front pew, the crisp, mountain air tasting faintly of aged candle wax and old books. The silence of the chapel is absolute, broken only by the rhythmic sounds of the organ. As you sit up, your hand brushes against a paper name tag stuck to your jacket, revealing the name you had previously forgotten, Alex Grant.")
        self.say("")
        self.say("Try typing look or help")
        self.say("it is helpful to draw a map as you play to keep track of locations")

    def say(self, message):
        self.messages.append(message)

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def announce_room(self):
        self.say(f"Welcome to {self.current_room.name}")
        room = self.current_room.name
        self.say(f"Exits: {self.current_room.list_exits()}")
        self.play_sound(self.current_room.enter_sound)

    def look(self):
        self.say(f"{self.current_room.description}")
        room = self.current_room.name
        if self.current_room.description == "As you approach the Sewanee Volunteer Fire Department, you hear the sound of an alarm echoing through the station. Firefighters are rushing around, preparing to respond to an emergency. Before you can take a closer look, someone calls out to you, it's the Fire Chief. “Well, look what we have here! We could use an extra set of hands. We’ve just received a call about a fire at Johnson Hall. Head over there quick!":
            self.play_sound("fire")
        if self.score >= 8 and self.current_room.description == "Welcome to the War Memorial Cross! This is the most beautiful place on the domain, so beautiful in fact it is said that angels dwell here, and a great place to watch the sunset overlooking the valley. There is no achievement here but remember this place you might want to come back!":
            self.say("You made it! The Sewanee Angels are waiting, go talk to them!")
    def go(self, direction):
        destination = self.current_room.get_neighbor(direction)
        if destination is None:
            self.say("You can't go that way from here.")
            return
        self.current_room = destination
        self.play_sound("move")
        self.announce_room()

    def talk(self, name):
        npc = self.current_room.npc
        for npc in self.current_room.npc:
            if npc is not None and npc.name == name:
                for npc in self.current_room.npc:
                    if npc is not None and npc.name == name:
                        self.say(f"{npc.speech}")
                    if npc is not None and npc.name == name:
                        self.score += npc.value
                    if npc.value > 0:
                        self.play_sound("pickup")
                        self.say(f"Your score is now {self.score} out of 8.")
                        npc.value = 0
                    if self.score == 8:
                        self.say("Congratulation on completing all of the achievements!")
                        self.say("The Sewanee Angels have a message for you. Solve their riddle and find the spot. Once there you will be able to talk to them again!")
                        self.say("Where angels watch from above, seek the towering symbol of faith overlooking the valley.")
                        self.play_sound("win")
            else:
                self.say(f"There is no one with that name to talk to here.")
                

    def take(self, name):
        for treasure in self.current_room.treasure:
            if treasure.name == name:
                self.current_room.treasure.remove(treasure)
                self.score += treasure.value
                self.play_sound("pickup")
                self.say(f"You take the {treasure.name}.")
            if name == "key":
                iv.append("key")
                return


        for food in self.current_room.food:
            if food.name == name:
                self.say(f"Great Choice!")

    def use(self, name):
        item = self.current_room.item
        if item is not None and name == "key":
            if "key" in iv:
                if self.current_room.enter_sound is not None:
                    self.play_sound(self.current_room.enter_sound)
                self.say(f"{self.current_room.item.speech}")
                if item.value > 0:
                    self.score += item.value
                    self.play_sound("pickup")
                    self.say(f"Your score is now {self.score} out of 8.")
                    if self.score == 8:
                        self.say("Congratulation on completing all of the achievements!")
                        self.say("The Sewanee Angels have a message for you. Solve their riddle and find the spot. Once there you will be able to talk to them again!")
                        self.say("Where angels watch from above, seek the towering symbol of faith overlooking the valley.")
                        self.play_sound("win")
            else:
                self.say(f"You can't get in yet. Make sure to pick up your key from Bishop's Common! HINT: Its east from here.")

    def fight(self, name):
        fire = self.current_room.fire
        if fire is not None and name == "fire":  
            self.say(f"{self.current_room.fire.speech}")
            self.play_sound("pickup")

        else:
            self.say(f"There is no fire here.")

    def basement(self, name):
        color = self.current_room.color
        if color is not None and name == "red":
            self.play_sound("pickup")
            books.append("1")
            if "3" in books and "2" in books and "1" in books:
                self.say("You did it and the Reception Desk looks so nice and clean now!! No go tell the librarian!")
            if "2" in books and "3" not in books:
                self.say("Correct! Now bring the right color to the second floor.")
            if "3" in books and "3" not in books:
                self.say("Correct! Now bring the right color to the first floor.")
            if "2" not in books and "3" not in books:
                self.say("Correct! Now bring the right color to the first floor and the second floor.")
        else:
            self.say(f"Wrong color for this floor. try again.")

    def first(self, name):
        color = self.current_room.color
        if color is not None and name == "orange":
            self.play_sound("pickup")
            books.append("2")
            if "3" in books and "2" in books and "1" in books:
                self.say("You did it and the Reception Desk looks so nice and clean now!! No go tell the librarian!")
            if "1" in books and "3" not in books:
                self.say("Correct! Now bring the right color to the seccond floor.")
            if "3" in books and "1" not in books:
                self.say("Correct! Now bring the right color to the basement.")
            if "1" not in books and "3" not in books:
                self.say("Correct! Now bring the right color to the second floor and the basement.")
        else:
            self.say(f"Wrong color for this floor. try again.")

    def second(self, name):
        color = self.current_room.color
        if color is not None and name == "yellow":
            self.play_sound("pickup")
            books.append("3")
            if "3" in books and "2" in books and "1" in books:
                self.say("You did it and the Reception Desk looks so nice and clean now!! No go tell the librarian!")
            if "1" in books and "2" not in books:
                self.say("Correct! Now bring the right color to the first floor.")
            if "2" in books and "1" not in books:
                self.say("Correct! Now bring the right color to the basement.")
            if "1" not in books and "2" not in books:
                self.say("Correct! Now bring the right color to the first floor and the basement.")
        else:
            self.say(f"Wrong color for this floor. try again.")

    def read(self, name):
        book = self.current_room.book
        if book is not None and book.name == name:
            self.say(f"{self.current_room.book.description}")
        else:
            self.say(f"I dont see that type of book here!")

    def ring(self, name):
       bell = self.current_room.bell
       if bell is not None and bell.name == name:
            self.say("You scramble up the spiral stairs, even though they are supposedly safe they still wiggle as you walk up them. You see skinnier ropes and then one bigger one that looks like it connects to a huge bell so you give it a good tug. Once you are done taking in the view from up here, head north to get to bishop commons, southeast to get to Abo's Alley or east for the quad!")
            self.play_sound("bell")
            self.score += bell.value
            if self.current_room.bell.value > 0:
                self.play_sound("pickup")
                self.say(f"Your score is now {self.score} out of 8.")
                bell.value = 0
            if self.score == 8:
                self.say("Congratulation on completing all of the achievements!")
                self.say("The Sewanee Angels have a message for you. Solve their riddle and find the spot. Once there you will be able to talk to them again!")
                self.say("Where angels watch from above, seek the towering symbol of faith overlooking the valley.")
                self.play_sound("win")
            return self.current_room.bell == True
       else:
            self.say(f"There is no bell to ring here.")

    def guess(self, name):
       guess = self.current_room.guess
       if guess is not None and guess.name == name:
            self.score += guess.value
            self.say(self.current_room.guess.speech)
            if self.current_room.guess.value > 0:
                self.play_sound("pickup")
                self.say(f"Your score is now {self.score} out of 8.")
                guess.value = 0
            if self.score == 8:
                self.say("Congratulation on completing all of the achievements!")
                self.say("The Sewanee Angels have a message for you. Solve their riddle and find the spot. Once there you will be able to talk to them again!")
                self.say("Where angels watch from above, seek the towering symbol of faith overlooking the valley.")
                self.play_sound("win")
            return self.current_room.guess == True
       else:
            self.say(f"That guess is incorrect.")

    def sort(self, name):
       book = self.current_room.book
       if book is not None and book.name == name:
            self.say(f"{self.current_room.book.description}")
       else:
            self.say(f"There is nothing to sort here!")

    def open(self, name):
       envlope = self.current_room.envlope
       if envlope is not None and envlope.name == name and self.score == 9:
            self.say(f"{self.current_room.envlope.speech}")
            self.say(f"{self.current_room.envlope.speech2}")
            self.say(f"{self.current_room.envlope.speech3}")
            self.say("")
            self.say("CREDITS")
            self.say("Story By: Virginia Arnold")
            self.say("Code By: Bryant Gunnels")
            self.say("Sound By: Sydney Thaxton")
            self.say("Thank you so much for playing our game we hope you enjoyed and got a look into this beautiful place we call home!")
            self.say("YSR!")
       else:
            self.say(f"There is nothing to open here")

    def handle_command(self, line):
        self.say(f"> {line}")
        words = line.lower().split()

        if not words:
            return

        command = words[0]

        if command == "look":
            self.look()
        elif command == "go" and len(words) > 1:
            self.go(words[1])
        elif command == "attack" and len(words) > 1:
            self.attack(words[1])
        elif command == "take" and len(words) > 1:
            self.take(words[1])
        elif command == "help":
            self.say("You can type this command at anytime and this menu will show up")
            self.say('Commands: "look" (you will use this in every room), "go DIRECTION", "talk CHARACTER", "read notebook", "ring bell", "take key", "use key", "fight fire", "sort books", "open envelope"') 
            self.say("To talk to a character type talk followed by their name ex: talk organist")
            self.say("When given a riddle to solve type guess and then enter your 'guess'")
            self.say("You will also use the go command to navigate McClurg, respond to the fire, get to the desk in the library and get to your dorm room")
            self.say("Each time you enter a room you will see the name of the room and the key word Exits: after you will find a list of directions. Using the go command with any of these directions will allow you to go to a new room.")
            self.say("Any exit that is not a direction (ex: homestyle, johnson, desk, firestation) is a part of the challange for that room and is also used with the go command.")
        elif command == "talk" and len(words) > 1:
            self.talk(words[1])
        elif command == "visit" and len(words) > 1:
            self.visit(words[1])
        elif command == "read" and len(words) > 1:
            self.read(words[1])
        elif command == "guess" and len(words) > 1:
            self.guess(words[1])
        elif command == "1857":
            self.say("The doors creak open as you step foot inside the tower. You see an ornate spiral staircase that looks like it is going to break as soon as you put on foot on the first stair rung. The stairs look like they lead to a trapped door. You also see a bellman standing in the tower.")
        elif command == "ring" and len(words) > 1:
            self.ring(words[1])
        elif command == "sort" and len(words) > 1:
            self.sort(words[1])
        elif command == "basement" and len(words) > 1:
            self.basement(words[1])
        elif command == "first" and len(words) > 1:
            self.first(words[1])
        elif command == "second" and len(words) > 1:
            self.second(words[1])
        elif command == "use" and len(words) > 1:
            self.use(words[1])
        elif command == "fight" and len(words) > 1:
            self.fight(words[1])
        elif command == "open" and len(words) > 1:
            self.open(words[1])
        else:
            self.say("I don't understand that.")

def wrap_text(text, font, max_width):
    if not text:
        return [""]
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = word if not current else current + " " + word
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def draw_game(screen, font, small_font, game):
    screen.fill((88, 44, 131))
    screen.blit(font.render("Discovering The Domain", True, (235, 235, 240)), (30, 20))

    lines = []
    for message in game.messages:
        lines.extend(wrap_text(message, small_font, WIDTH - 60))
    lines = lines[-20:]

    y = 70
    for line in lines:
        screen.blit(small_font.render(line, True, (206, 184, 136)), (30, y))
        y += 23

    pygame.draw.line(screen, (100, 100, 110), (30, HEIGHT - 70), (WIDTH - 30, HEIGHT - 70), 2)
    screen.blit(small_font.render("> " + game.current_input, True, (255, 255, 255)), (30, HEIGHT - 50))

async def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Discovering the Domain")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 22)

    game = TextAdventure()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    if not game.game_over:
                        command = game.current_input.strip()
                        game.current_input = ""
                        game.handle_command(command)
                elif event.key == pygame.K_BACKSPACE:
                    game.current_input = game.current_input[:-1]
                elif event.unicode and event.unicode.isprintable():
                    game.current_input += event.unicode

        draw_game(screen, font, small_font, game)
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())