
''' laitetaan game classin sisään'''
def lataa(self):
    self.player_range = MAX_PLAYER_RANGE
    self.player_turns = self.player_turns + 1
    #consoleen ilmotus että akku ladattu täyteen

def supercharge(self):
    self.player_range = self.player_range + PLAYER_SUPERCHARGE_AMOUNT
    self.player_turns = self.player_turns + 1
    #consoleen ilmotus että superchargettu myös pitää saada nappi muuttumaan lataa tai supercharge

def throw_dice(self):
    """heittää noppaa 1-6."""
    self.player_turns = self.player_turns + 1
    throw_dice = random.randint(0, 5)
    if throw_dice == 0: #salaman isku consoleen viesti: Salama iski koneen akkuun, sait akun täyteen ja 200km ylimääräistä lentoa!
        self.player_range = MAX_PLAYER_RANGE + 200
    elif throw_dice == 1: #passi consoleen viesti: Jäit tullissa kiinni vanhasta passista, sinun on palattava takaisin lähtömaahan.
        self.current_airport = self.start_airport
    elif throw_dice == 2: #presidentti viesti consoleen: Tasavallan presidentti on huomioinut teidän kilpailun ja myönsi sinulle tuliterän lentokoneen!
        MAX_PLAYER_RANGE = MAX_PLAYER_RANGE + 100
        self.player_range = MAX_PLAYER_RANGE
    elif throw_dice == 3: #fatigue viesti:Olet väsynyt, nukut pommiin ja rangesi tippui nollaan.
        self.player_range = 0
    elif throw_dice == 4: #raffle viesti:Hävisit lentokoneesi pokerissa, onneksi löysit paikkaliselta kirppikseltä käytetyn lentokoneen
        MAX_PLAYER_RANGE = MAX_PLAYER_RANGE - 200
        self.player_range = MAX_PLAYER_RANGE
    elif throw_dice == 5: #kakka viesti:kakkasit huosuun xdd

# html napit
'''
<button type="noppa">Click Me!</button>
<button type="lataa">Click Me!</button>
<button type="möttösen sijainti">Click Me!</button>
'''