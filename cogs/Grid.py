import discord
import datetime

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
        arrRocket = [] #array for where the rocket is

        asteroid = self.client.get_cog("Asteroid")
        if asteroid is not None:
            asteroidSpawn = await asteroid.spawnAsteroid(size, icon)
            for item in grid[0][6]:
                arrRocket.append(item) #put the last row in grid into the arrRocket array
            arrRocket[3] = ":rocket:"
            grid[0][6] = arrRocket
            grid[0][0] = asteroidSpawn
            return grid, asteroidSpawn, arrRocket    

    #creating the starting grid
    async def gridToString(self, stringVal, gameboard): #take data from the array and convert it into a String
        for row in gameboard:
            for col in row:
                for string in col:   
                    stringVal += string
                stringVal += "\n"
        return stringVal

def setup(client):
    client.add_cog(Grid(client))
