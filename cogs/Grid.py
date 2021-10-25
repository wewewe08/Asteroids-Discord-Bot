import discord
import datetime
import random
from discord.ext import commands

class Grid(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("grid is ready")

    async def makeGrid(self, size, icon):
        grid = [[[icon] * size] * size]
        arrRocket = [] #array for where the rocket is
        asteroid = self.client.get_cog("Asteroid")
        if asteroid is not None:
            asteroidSpawn = await asteroid.spawnAsteroid(size, icon)
            packageSpawn =  await asteroid.spawnCarePackage(size, icon)
            for item in grid[0][6]:
                arrRocket.append(item) #put the last row in grid into the arrRocket array
            arrRocket[3] = ":rocket:"
            grid[0][6] = arrRocket
            grid[0][0] = asteroidSpawn
            grid[0][3] = packageSpawn
            return grid, asteroidSpawn, arrRocket, packageSpawn

    #creating the starting grid
    async def gridToString(self, stringVal, gameboard): #take values from an array and convert it into a String value
        for row in gameboard:
            for col in row:
                for string in col:   
                    stringVal += string
                stringVal += "\n"
        return stringVal

def setup(client):
    client.add_cog(Grid(client))
