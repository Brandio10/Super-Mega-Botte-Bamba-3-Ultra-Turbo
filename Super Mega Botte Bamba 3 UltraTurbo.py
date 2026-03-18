import arcade
import random

SCREENWIDTH = 1272
SCREENHEIGHT = 636
GRAVITY = 1
PLAYER_JUMP_SPEED = 1

class Giochino(arcade.Window):
    
    def __init__(self):
        super().__init__(SCREENWIDTH,SCREENHEIGHT,"Super Mega Botte&Bamba 3 Ultra Turbo")
    
        self.lista_Gabibbo= arcade.SpriteList()
        self.lista_Adrian= arcade.SpriteList()
        self.wall_list= arcade.SpriteList()
        self.background_image = arcade.load_texture("./Sanremo.jpg")
        self.sprite = None
        self.playerSpriteList = arcade.SpriteList()
        self.setup()
        self.muovi_destra = False
        self.muovi_sinistra = False
        self.attack = False
        self.guard = False



    def setup(self):

        self.pavimento = "./Pavimento1.jpg" 

        self.wall_list.append(self.pavimento)

        self.sprite_gabibbo=arcade.Sprite("Gabibbo.png")

        self.sprite_gabibbo.center_x = 1150
        self.sprite_gabibbo.center_y = 195
        self.sprite_gabibbo.scale = 0.6

        self.lista_Gabibbo.append(self.sprite_gabibbo)

        self.sprite_adrian=arcade.Sprite("Adrian.png")

        self.sprite_adrian.center_x = 200
        self.sprite_adrian.center_y = 225
        self.sprite_adrian.scale = 0.5

        self.lista_Adrian.append(self.sprite_adrian)
        self.physics_engine_gabibbo = arcade.PhysicsEnginePlatformer(self.sprite_gabibbo, walls=self.wall_list, gravity_constant=GRAVITY)
        self.physics_engine_adrian = arcade.PhysicsEnginePlatformer(self.sprite_adrian, walls=self.wall_list, gravity_constant=GRAVITY)


    def on_update(self, delta_time: float) -> bool | None:
        if self.muovi_destra:
            self.sprite_adrian.center_x += 10
        if self.muovi_sinistra:
            self.sprite_adrian.center_x -= 10
        if self.sprite_adrian.center_x <= 0:
            self.sprite_adrian.center_x = 1
        if self.sprite_adrian.center_x >= 1272:
            self.sprite_adrian.center_x = 1271
        if self.sprite_adrian.center_y <= 226:
            self.sprite_adrian.center_y = 225
        if self.sprite_adrian.center_y >= 401:
            self.sprite_adrian.center_y = 400


        
    def on_draw(self):
        self.clear()
        print(self.background_image)
        arcade.draw_texture_rect(
            self.background_image,
            arcade.LBWH(0,0,SCREENWIDTH,SCREENHEIGHT)
        )

        self.lista_Gabibbo.draw()
        self.lista_Adrian.draw()
        self.wall_list.draw()
 

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            if self.physics_engine_adrian.can_jump():
                self.sprite_adrian.change_y = PLAYER_JUMP_SPEED
        if key == arcade.key.D:
            self.muovi_destra = True
        if key == arcade.key.A:
            self.muovi_sinistra = True
        if key == arcade.key.P:
            self.attack = True
        if key == arcade.key.L:
            self.guard = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.D:
            self.muovi_destra = False
        if key == arcade.key.A:
            self.muovi_sinistra = False
        if key == arcade.key.P:
            self.attack =False
        if key == arcade.key.L:
            self.guard = False

        



def main():
    gioco = Giochino()
    arcade.run()


if __name__ == "__main__":
    main()