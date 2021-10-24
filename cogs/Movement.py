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

def setup(client):
    client.add_cog(Movement(client))
