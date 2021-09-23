import random

from discord.ext import commands

class Grid(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("grid is ready")

    async def makeGrid(self, size, icon):
        #print("test")
        grid = [[[icon] * size] * size]
        arrAsteroid = [] #array for asteroids
        arrRocket = [] #array for where the rocket is

        def spawnAsteroid():
            asteroidPos = random.randint(0, len(grid[0][0]))
            for item in grid[0][0]:
                arrAsteroid.append(item)
            arrAsteroid[asteroidPos] = ":rock:"
            return arrAsteroid

        for item in grid[0][6]:
            arrRocket.append(item)
        arrRocket[3] = ":rocket:"
        grid[0][6] = arrRocket
        grid[0][0] = spawnAsteroid()
        return grid, arrAsteroid, arrRocket    

def setup(client):
    client.add_cog(Grid(client))