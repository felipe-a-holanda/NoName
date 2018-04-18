import json
import swisseph as swe
from collections import OrderedDict
swe.set_ephe_path('/usr/share/libswe/ephe/')

PLANET_CODES = ['sun',
                'moon',
                'mercury',
                'venus',
                'mars',
                'jupiter',
                'saturn',
                'uranus',
                'neptune',
                'pluto',
                'mean_node',
                'true_node',
                'mean_apog',
                'oscu_apog',
                'earth',
                'chiron',
                'pholus',
                'ceres',
                'pallas',
                'juno',
                'vesta',
                'intp_apog',
                'intp_perg']

PLANET_NAMES = ['Sun',
                'Moon',
                'Mercury',
                'Venus',
                'Mars',
                'Jupiter',
                'Saturn',
                'Uranus',
                'Neptune',
                'Pluto',
                'Mean Node',
                'True Node',
                'Mean Apogee',
                'Osculating Apogee',
                'Earth',
                'Chiron',
                'Pholus',
                'Ceres',
                'Pallas',
                'Juno',
                'Vesta',
                'Interpolated Apogee',
                'Interpolated Perigee']

SIGN_NAMES = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__

class BodyPos(object):
    def __init__(self, index, code, name, x, y, z, dx, dy, dz):
        self.index = index
        self.code = code
        self.name = name
        self.x = x
        self.dx = dx
        self.sign = SIGN_NAMES[int(self.x/30)]

    def round(self, f):
        return float("%.3f"% f)

    def toDict(self):
        return self.__dict__

    def toJSON(self):
        return {'index':self.index, 'code':self.code, 'name':self.name,'x':self.round(self.x), 'dx':self.round(self.dx)}


class AstroChart(object):
    def __init__(self, datetime_utc, latitude=None, longitude=None, name=""):
        self.name = name
        self.datetime_utc = datetime_utc
        self.datetime_julday = self.calc_julday(self.datetime_utc)
        self.latitude = latitude
        self.longitude = longitude

        self.houses = None
        self.planets_in_houses = None
        self.planets = self.calc_planets()
        self.asc = 0
        if self.latitude and self.longitude:
            self.houses = self.calc_houses()
    
    def __str__(self):        
        return "%s %s: %s" %(self.name, str(self.datetime_utc), str(self.planets['sun']['sign']))

    def calc_julday(self, datetime_utc):
        j = swe.julday(datetime_utc.year, datetime_utc.month, datetime_utc.day, datetime_utc.hour + datetime_utc.minute / 60.0)
        return j

    def calc_planets(self):
        planets = OrderedDict()
        for i in range(swe.NPLANETS):
            planets[PLANET_CODES[i]] = BodyPos(i, PLANET_CODES[i], PLANET_NAMES[i], *swe.calc_ut(self.datetime_julday, i)).toDict()
        return planets

    def calc_house(self, houses, angle):
        house = -1
        for i in range(12):
            if houses[i] < houses[(i + 1) % 12]:
                if houses[i] <= angle <= houses[(i + 1) % 12]:
                    house = i
                    break
            else:
                if houses[i] <= angle or angle <= houses[(i + 1) % 12]:
                    house = i
                    break
        return house

    def calc_houses(self):
        houses = swe.houses(self.datetime_julday, self.latitude, self.longitude)[0]
        planets_in_houses = []
        for planet_code, planet in self.planets.items():
            planet['house'] = self.calc_house(houses, planet['x'])
        self.asc = houses[0]
        self.asc_sign = SIGN_NAMES[int(houses[0]/30)]
        return houses#, planets_in_houses

    def generate_tags(self):
        for code, planet in self.planets.items():
            print("%s-in-%s"% (planet['name'].replace(' ','_'), planet['sign']))

    def get_chart(self):
        return {'planets':self.planets, 'houses':self.houses, 'asc':self.asc}

    def get_chart_json(self):
        return json.dumps(self.get_chart(), default=dumper, indent=2)


if __name__=='__main__':
    from datetime import datetime
    astro = AstroChart(datetime(1986,12,22,8,34), name="Darpan")
    print(astro)
    #print(astro.generate_tags())
