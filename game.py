from geopy import distance
import mysql.connector
import random
from pprint import pprint as ppp
from dotenv import load_dotenv
import os

load_dotenv()

NPC_NUBER_OF_OPTIONS = 6
GAME_AIRPORT_LIMIT = 100
NPC_RANGE = 600
MAX_PLAYER_RANGE = 600
NPC_SUPERCHARGE_AMOUNT = 300
PLAYER_SUPERCHARGE_AMOUNT = 150




connection = mysql.connector.connect(
         host=os.environ.get('DB_HOST'),
         port= 3306,
         database=os.environ.get('DB_NAME'),
         user=os.environ.get('DB_USER'),
         password=os.environ.get('DB_PASS'),
         autocommit=True)


def airports():
    haku = f"SELECT iso_country, ident, name, type, latitude_deg, longitude_deg FROM airport WHERE continent = 'EU' AND iso_country NOT IN ('ES', 'PT', 'RU', 'ISL', 'IS') AND type = 'large_airport' limit {GAME_AIRPORT_LIMIT};"
    sql = (haku)
    """Hakee tietokannasta haltuut lentokentät ja niistä kaikki oleelliset tiedot."""
    cursor = connection.cursor(dictionary = True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result




def distance_from_airport_distance(x): 
    """Palauttaa toisen alkion."""
    return x[1]

def get_npc_connective_flight_options(in_range_ports,npc_currentport, goal):
    """Etsii npc:lle N parasta vaihtoehtoa kaikista kentistä jotka rangessa"""
    airport_distances = []
    for airport in in_range_ports:
        plane_range = calculate_distance(airport[0], goal)  
        current_distance_to_goal = calculate_distance(npc_currentport, goal)
        if plane_range < current_distance_to_goal:
            airport_distances.append([airport[0], plane_range])
    result_connective_flights = sorted(airport_distances, key=distance_from_airport_distance)[:NPC_NUBER_OF_OPTIONS]   
    return result_connective_flights

def get_npc_destination_icao(npc_flight_options, goal):
    """Tää funktio palauttaa npc-pelaajan lehtovaihtoehdoista satunnaisesti yhden kentän icao-koodin"""
    if len(npc_flight_options) == 0:
        return None
    for airport in npc_flight_options:
        if airport[0] == goal:
            return goal
    if len(npc_flight_options)> 1:
        random_index =random.randint(0,len(npc_flight_options)-1)
    else:
        random_index = 0

    return npc_flight_options[random_index][0]

def calculate_distance(current, target):
    """Laskee etäisyyden nykyisen ja mahdollisen seuraavan kentän väliltä."""
    start = airport_data(current)
    end = airport_data(target)
    return distance.distance([start['latitude_deg'], start['longitude_deg']], [end['latitude_deg'], end['longitude_deg']]).kilometers


"""def update_location(icao, p_range):
    sql = ("UPDATE game SET location = %s, player_range = %s")
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (icao, p_range))"""

def player_airport_range_calc(icao, airport_list, player_range):
    """Kertoo mitkä kentät ovat pelaajan rangen sisällä."""
    in_range = []
    for airport in airport_list:
        range = calculate_distance(icao, airport['ident'])
        if range <= player_range and range != 0:
            in_range.append([airport['name'], airport['ident'], int(range)])
    return in_range


def npc_airport_range_calc(npc_icao, airport_list, npc_range, NPC_visited_ports):
    """Kertoo mitkä kentät ovat npc:n rangen sisällä."""
    in_range = []
    for airport in airport_list:
        if airport['ident'] in NPC_visited_ports:
            continue
        range = calculate_distance(npc_icao, airport['ident'])
        if range <= npc_range and range != 0:
            in_range.append([airport['ident'], int(range)])

    return in_range

def get_airport_name(icao):
    """Etsii halutun kentän nimen käyttäen icaota."""
    sql = (f"SELECT name FROM airport WHERE ident = '{icao}'")
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchone()
    return result ['name']

def get_list_function(x):   
    """Syötetään x paikalle nopan saatu silmäluku ja funktio kertoo mikä tapahtuuma siitä tulee."""
    penalties = ["Salamanisku", "Passi", "President", "Fatigue", "Raffle", "Kakka"]
    funktion = penalties[x]
    return funktion

def throw_dice():
    """heittää noppaa 1-6."""
    throw_dice = random.randint(0, 5)
    return throw_dice


def airport_data(icao):
    """Hakee tietokannasta kaikki tiedot identillä."""
    sql = ("SELECT iso_country, ident, name, latitude_deg, longitude_deg FROM airport WHERE ident = %s")
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return result

def print_player_in_range_ports(in_range_ports):
    """Antaa tulostuksen vaihtoehdoista mihin voi lentää."""
    print_content = []
    for airport in in_range_ports:
        port_name = airport_data(airport[0])['name']
        print_content.append(f'Lentokentän koodi: {airport[0]}, Lentokentän nimi: {port_name}, Lentokentälle on {airport[1]} kilometriä matkaa.')
    print(print_content)

def main_npc_flight_fuunction(npc_icao,all_ports, npcrange, goalport, NPC_visited_ports):
    """Tärkein funktio laskee mille kentälle npc liikkuu seuraavaksi."""
    npc_airport_range = npc_airport_range_calc(npc_icao, all_ports, npcrange,NPC_visited_ports)
    npc_connective_flight_options = get_npc_connective_flight_options(npc_airport_range, npc_icao, goalport)
    destination = get_npc_destination_icao(npc_connective_flight_options, goalport)
    if destination != None:
        NPC_visited_ports.add(destination)
    return destination

def get_goal_airports(start,allports):
    """Funktio listaa kaikista kentistä kentät jotka ovat kauimpana maalista joka on generoitu."""
    goal_airport_options = []
    for airport in allports:
        range = calculate_distance(airport['ident'], start)  
        goal_airport_options.append([airport['ident'], range])
    goal_airport_options = sorted(goal_airport_options, key=distance_from_airport_distance, reverse=True)[:10]
    random_index =random.randint(0,len(goal_airport_options)-1)
    random_goal_port = goal_airport_options[random_index]
    goal = random_goal_port[0]
    return goal
    
class Game:
    
    def __init__(self, difficulty):
        self.all_airports = airports()
        self.goal_num = random.randint(0,len(self.all_airports)-1)
        self.start_num = random.randint(0,len(self.all_airports)-1)
        self.start_airport = self.all_airports[self.start_num]['ident']
        self.goal_airport =  get_goal_airports(self.start_airport, self.all_airports)
        self.current_airport = self.start_airport
        self.npc_current_airport = self.start_airport
        self.end_airport = airport_data(self.goal_airport)
        self.player_turns = 0
        self.npc_turns = 0
        self.player_range = MAX_PLAYER_RANGE
        self.npc_range_1 = NPC_RANGE
        self.difficulty = difficulty
        self.NPC_visited_ports = set()
        self.game_running = True
        self.npc_range_1 = NPC_RANGE
        
    def get_statistics(self):
        in_range = player_airport_range_calc(self.current_airport,self.all_airports,self.player_range)
        flight_options = []
        for i in in_range:
            target = {'icao': i[1], 'name': i[0], 'range': i[2]}
            flight_options.append(target)
        return {
            'location': self.current_airport,
            'player_range': self.player_range,
            'flight_options': flight_options,
            'goal_airport': self.goal_airport
        }    
        
        
    def do_fly (self, icao):
        """Tämä funktio suorittaa lentooperaation(myös npc) /game?action=fly tilanteessa"""
        selected_distance = calculate_distance(self.current_airport, icao)
        self.player_range -= selected_distance
        """update_location(icao, self.player_range)"""
        self.current_airport = icao
        self.npc_destination = main_npc_flight_fuunction(self.npc_current_airport,self.all_airports, self.npc_range_1, self.goal_airport, self.NPC_visited_ports)
        if self.npc_destination == None:
            self.npc_range_1 = self.npc_range_1 + NPC_SUPERCHARGE_AMOUNT
            do_run = False
        elif self.npc_range_1 >= NPC_RANGE/2 :
            npc_selected_distance = calculate_distance(self.npc_current_airport, self.npc_destination)
            self.npc_range_1  -= npc_selected_distance
            """update_location(self.npc_destination, npc_range_1)"""
            self.npc_current_airport = self.npc_destination
            do_run = False
        else:
            self.npc_range_1 = NPC_RANGE
        if self.current_airport == self.goal_airport or self.npc_current_airport == self.goal_airport:
            self.game_running == False
        return self.get_statistics()
    
    
    
"""
g = Game(0)
t = g.get_statistics()
pp(t)
icao = t['flight_options'][0]['icao']
g.do_fly(icao)
pp(g.get_statistics())

"""


