#import asyncio (used for moving asteroids)
import random

from discord.ext import commands

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

    #ARCHIVED
    #async def moveAsteroid(self, gameboard, arr):
    #    def asteroidGenerator(gameboard, arr):
    #        col_index = 0
    #        while col_index != 5:
    #            print(col_index)
    #           if gameboard[0][col_index] == arr:
    #                gameboard[0][col_index] = gameboard[0][col_index+1]
    #                gameboard[0][col_index+1] = arr
    #                col_index = col_index + 1
    #                yield gameboard
    #            else:
    #                break
    #    generator = asteroidGenerator(gameboard=gameboard, arr=arr)
    #    return generator
    
    async def shootAsteroid(self, gameboard, arrRocket, arrAsteroid):
            for index in range(len(arrRocket)):
                if arrRocket[index] == ":rocket:":
                    rocketIndex = index
                    if arrAsteroid[rocketIndex] == ":rock:":
                        arrAsteroid[rocketIndex] = ":boom:"
                    else:
                        print("something went wrong with shooting")
                    break
            return gameboard

    async def resetBoard(self, gameboard, arrAsteroid, arrRocket, size, icon, asteroidShot):
        if asteroidShot:
            for index in range(len(arrAsteroid)):
                if arrAsteroid[index] == ":boom:" and arrRocket[index] == ":rocket:":
                    arrAsteroid = await self.spawnAsteroid(size, icon)
                    gameboard[0][0] = arrAsteroid
                    break
        else:
            pass
        return gameboard, arrAsteroid

def setup(client):
    client.add_cog(Asteroid(client))
