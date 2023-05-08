from PIL import Image


def edit_ninja_adventure_assets():
    # nature rock 32x32 (2x2 tiles)
    with Image.open('data/NinjaAdventure/TilesetNature.png') as im:
        rock_box = (64, 192, 64 + 32, 192 + 32)
        rock32 = im.crop(rock_box)
        rock64 = rock32.resize((64, 64), Image.Resampling.NEAREST)
        rock64.save('data/rock.png')

    # dungeon stone
    with Image.open('data/NinjaAdventure/TilesetDungeon.png') as im:
        # print(im.format, im.size, im.mode)
        # stone rect: 128 48 16 16
        stone_box = (128, 48, 128 + 16, 48 + 16)
        stone16 = im.crop(stone_box)
        # stone16.save('data/stone_16px.png')
        stone64 = stone16.resize((64, 64), Image.Resampling.NEAREST)
        stone64.save('data/stone.png')

    # NOTE: anim key
    # down:x=0
    # up:x=16
    # left:x=32
    # right:x=48
    # idle:y=0
    # walk:0<=y<=48 (4 frames)
    # attack:y=64
    # jump:y=80
    # dead:(0,96) 
    # item:(16,96) 
    # special1:(32,96) 
    # special2:(48,96)

    # green ninja player
    with Image.open('data/NinjaAdventure/GreenNinjaSpriteSheet.png') as im:
        player_box = (0, 0, 16, 16)
        player16 = im.crop(player_box)
        player64 = player16.resize((64, 64), Image.Resampling.NEAREST)
        player64.save('data/player.png')

    print('data.py: Ninja Adventure assets edited and saved.')