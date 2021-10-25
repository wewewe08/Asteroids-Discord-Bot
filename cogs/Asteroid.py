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

    async def spawnCarePackage(self, size, icon):
        arrPackages = [] #ammo package array
        grid = [[[icon] * size] * size]
        packagePos =  random.randint(0, len(grid[0][3]))
        for item in grid[0][3]:
            arrPackages.append(item)
        arrPackages[packagePos] = ":package:"
        return arrPackages

    async def shootAsteroid(self, gameboard, arrRocket, arrAsteroid, arrPackage, missles, isRock):
        for index in range(len(arrRocket)):
            if arrRocket[index] == ":rocket:":
                rocketIndex = index
                if arrAsteroid[rocketIndex] == ":rock:" and arrPackage[index] != ":package:":
                    arrAsteroid[rocketIndex] = ":boom:"
                    gameboard[0][0] = arrAsteroid
                    isRock = True
                    break
                elif arrPackage[rocketIndex]  == ":package:":
                    arrPackage[rocketIndex] = ":up:"
                    missles += 1
                    gameboard[0][3] = arrPackage
                    isRock = False
                    break
                else:
                    missles -= 1
                    break
        return gameboard, isRock, missles

    async def resetBoard(self, gameboard, arrAsteroid, arrRocket, arrPackage, size, icon, asteroidShot):
        if asteroidShot:
            for index in range(len(arrAsteroid)):
                if arrAsteroid[index] == ":boom:" and arrAsteroid[index] != ":package:" and arrRocket[index] == ":rocket:":
                    #respawning asteroids
                    arrAsteroid = await self.spawnAsteroid(size, icon)
                    gameboard[0][0] = arrAsteroid 
                    #respawning care packages
                    package_spawn_rate = random.randrange(10)
                    print(package_spawn_rate)
                    for item in arrPackage:
                        if item != ":package:" and package_spawn_rate == 0:
                            arrPackage =  await self.spawnCarePackage(size, icon)
                            gameboard[0][3] = arrPackage
                            break
                    break
                elif arrPackage[index] == ":up:" and arrRocket[index] == ":rocket:":
                    package_spawn_rate = random.randrange(10)
                    print(package_spawn_rate)
                    for item in arrPackage:
                        if item != ":package:" and package_spawn_rate == 0:
                            arrPackage =  await self.spawnCarePackage(size, icon)
                            gameboard[0][3] = arrPackage
                            break
                    else:
                        gameboard[0][3] = [':black_large_square:', ':black_large_square:', ':black_large_square:', ':black_large_square:', ':black_large_square:', ':black_large_square:', ':black_large_square:']
                        break
        return gameboard, arrAsteroid, arrPackage

def setup(client):
    client.add_cog(Asteroid(client))
