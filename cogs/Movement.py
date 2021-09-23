from discord.ext import commands

class Movement(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("movement is ready")
    
    async def moveLeft(self, gameboard, arr):
        for i in range(0, len(arr)):
            if arr[i] == ":rocket:":
                if i == 0:
                    pass
                else:
                    arr[i] = ":black_large_square:"
                    arr[i-1] = ":rocket:"
                break
        gameboard[0][6] = arr
        return gameboard

    async def moveRight(self, gameboard, arr):
        for i in range(0, len(arr)):
            if arr[i] == ":rocket:":
                if i == 6:
                    pass
                else:
                    arr[i] = ":black_large_square:"
                    arr[i+1] = ":rocket:"
                break
        gameboard[0][6] = arr
        return gameboard

    async def moveAsteroid(self, gameboard, arr):
        rows = len(gameboard)
        cols = len(gameboard[0])
        grid_length = rows*cols
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
    client.add_cog(Movement(client))