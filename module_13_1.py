import asyncio


async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')
    for ball_number in range(1, 6):
        await asyncio.sleep(1 / power)
        print(f'Силач {name} поднял {ball_number} шар.')
        if ball_number == 5:
            print(f'Силач {name} закончил соревнования.')


async def start_tournament():
    strongman1 = asyncio.create_task(start_strongman('John', 5))
    strongman2 = asyncio.create_task(start_strongman('Hercules', 10))
    strongman3 = asyncio.create_task(start_strongman('Diablo', 15))
    await strongman1
    await strongman2
    await strongman3


asyncio.run(start_tournament())
