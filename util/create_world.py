from django.contrib.auth.models import User
from adventure.models import Player, Room
from util.sample_generator import World

world = World()
world.generate_rooms(5, 5, 25)
world.print_rooms()

rooms = []
Room.objects.all().delete()
starting_room = None
for column in world.grid:
    for room in column:
        if room and room != 'wall':
            r = Room(id=room.id, title=room.name,
                     description=room.description, x=room.x, y=room.y)
            r.save()
            rooms.append({'room': r, 'n_to': room.n_to, 's_to': room.s_to,
                          'e_to': room.e_to, 'w_to': room.w_to, })
            if room.id == 1:
                starting_room = room

players = Player.objects.all()
for p in players:
    p.currentRoom = starting_room.id
    p.save()

for room in rooms:
    if room['n_to']:
        room['room'].connectRooms(room['n_to'], 'n')
    if room['s_to']:
        room['room'].connectRooms(room['s_to'], 's')
    if room['e_to']:
        room['room'].connectRooms(room['e_to'], 'e')
    if room['w_to']:
        room['room'].connectRooms(room['w_to'], 'w')
