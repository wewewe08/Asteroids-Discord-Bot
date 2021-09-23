import asyncio
import random

from discord.ext import commands, tasks

class Asteroid(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("asteroid is ready")  

    async def spawnAsteroid(self, size, icon):
        arrAsteroid = [] #array for asteroids
        grid = [[[icon] * size] * size]
        asteroidPos = random.randint(0, len(grid[0][0]))
        for item in grid[0][0]:
            arrAsteroid.append(item)
        arrAsteroid[asteroidPos] = ":rock:"
        return arrAsteroid

    async def moveAsteroid(self, gameboard, arr):
        rows = len(gameboard)
        cols = len(gameboard[0])
        grid_length = rows*cols
        num = 0
        for row in range(0, grid_length):
            for col in range(0, row):
                if gameboard[0][col] == arr:
                    if col != 6:
                        gameboard[0][col] = gameboard[0][col+1]
                        gameboard[0][col+1] = arr
                    else:
                        print("something went wrong with the asteroid")
                        pass
                break
        return gameboard  

    async def shootAsteroid(self, gameboard, arrRocket, arrAsteroid):
        for index in range(len(arrRocket)):
            if arrRocket[index] == ":rocket:":
                rocketIndex = index
                if arrAsteroid[rocketIndex] == ":rock:":
                    arrAsteroid[rocketIndex] = ":boom:"
                else:
                    print("something went wrong with shooting")
                    pass
                break
        return gameboard

    async def resetBoard(self, gameboard, arrAsteroid):
        for index in range(len(arrAsteroid)):
            if arrAsteroid[index] == ":boom:":
                arrAsteroid[index] = ":black_large_square:"
                break
        return gameboard 

def setup(client):
    client.add_cog(Asteroid(client))