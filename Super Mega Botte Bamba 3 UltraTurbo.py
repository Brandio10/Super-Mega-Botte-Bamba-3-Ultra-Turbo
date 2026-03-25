import arcade
import random

SCREENWIDTH = 1272
SCREENHEIGHT = 636
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

class Giochino(arcade.Window):
    
    def __init__(self):
        super().__init__(SCREENWIDTH,SCREENHEIGHT,"Super Mega Botte&Bamba 3 Ultra Turbo")
    
        self.lista_Gabibbo= arcade.SpriteList()
        self.lista_Adrian= arcade.SpriteList()
        self.wall_list= arcade.SpriteList()
        self.background_image = arcade.load_texture("./Sanremo.jpg")
        self.sprite = None
        self.playerSpriteList = arcade.SpriteList()
        self.muovi_destraAdrian = False
        self.muovi_destraGabibbo= False
        self.muovi_sinistraAdrian = False
        self.muovi_sinistraGabibbo= False
        self.attackAdrian = False
        self.guardAdrian = False
        self.attackGabibbo =False
        self.guardGabibbo = False
        self.setup()



    def setup(self):

        self.pavimento =arcade.Sprite("./Pavimento1.jpg")

        self.wall_list.append(self.pavimento)
        self.pavimento.center_x = 625
        self.pavimento.center_y= 0
        self.pavimento.scale_x = 100
        self.pavimento.scale_y =0.5

        self.sprite_gabibbo=arcade.Sprite("Gabibbo.png")

        self.sprite_gabibbo.center_x = 1150
        self.sprite_gabibbo.center_y = 195
        self.sprite_gabibbo.scale = 0.6



        self.sprite_gabibbo.center_x = 1150
        self.sprite_gabibbo.center_y = 195
        self.sprite_gabibbo.scale = 0.6

        self.lista_Gabibbo.append(self.sprite_gabibbo)

        self.sprite_adrian=arcade.Sprite("Adrian.png")

        self.sprite_adrian.center_x = 200
        self.sprite_adrian.center_y = 250
        self.sprite_adrian.scale = 0.5

        self.lista_Adrian.append(self.sprite_adrian)
        self.physics_engine_gabibbo = arcade.PhysicsEnginePlatformer(self.sprite_gabibbo, walls=self.wall_list, gravity_constant=GRAVITY)
        self.physics_engine_adrian = arcade.PhysicsEnginePlatformer(self.sprite_adrian, walls=self.wall_list, gravity_constant=GRAVITY)


    def on_update(self, delta_time: float) -> bool | None:
        if self.muovi_destraAdrian:
            self.sprite_adrian.center_x += 10
        if self.muovi_sinistraAdrian:
            self.sprite_adrian.center_x -= 10
        if self.sprite_adrian.center_x <= 0:
            self.sprite_adrian.center_x = 1
        if self.sprite_gabibbo.center_x <= 0:
            self.sprite_gabibbo.center_x = 1
        if self.sprite_adrian.center_x >= 1272:
            self.sprite_adrian.center_x = 1271
        if self.sprite_gabibbo.center_x >= 1272:
            self.sprite_gabibbo.center_x = 1271
        if self.muovi_destraGabibbo:
            self.sprite_gabibbo.center_x += 10
        if self.muovi_sinistraGabibbo:
            self.sprite_gabibbo.center_x -=10
        if self.sprite_adrian.center_y >= 600:
            self.sprite_adrian.center_y = 600
        if self.sprite_gabibbo.center_y >= 600:
            self.sprite_gabibbo.center_y = 600

        self.physics_engine_adrian.update()
        self.physics_engine_gabibbo.update()


        
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background_image,
            arcade.LBWH(0,0,SCREENWIDTH,SCREENHEIGHT)
        )

        self.lista_Gabibbo.draw()
        self.lista_Adrian.draw()
        #self.wall_list.draw()
 

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            if self.physics_engine_adrian.can_jump():
                self.sprite_adrian.change_y = PLAYER_JUMP_SPEED
        if key == arcade.key.D:
            self.muovi_destraAdrian = True
        if key == arcade.key.A:
            self.muovi_sinistraAdrian = True
        if key == arcade.key.UP:
            if self.physics_engine_gabibbo.can_jump():
                self.sprite_gabibbo.change_y = PLAYER_JUMP_SPEED
        if key == arcade.key.RIGHT:
            self.muovi_destraGabibbo = True
        if key == arcade.key.LEFT:
            self.muovi_sinistraGabibbo = True
        if key == arcade.key.Q:
            self.attackAdrian = True
        if key == arcade.key.E:
            self.guardAdrian = True
        if key == arcade.key.N:
            self.attackGabibbo = True
        if key == arcade.key.M:
            self.guardGabibbo = True



    def on_key_release(self, key, modifiers):
        if key == arcade.key.D:
            self.muovi_destraAdrian = False
        if key == arcade.key.RIGHT:
            self.muovi_destraGabibbo = False
        if key == arcade.key.LEFT:
           self.muovi_sinistraGabibbo = False 
        if key == arcade.key.A:
            self.muovi_sinistraAdrian = False
        if key == arcade.key.Q:
            self.attackAdrian =False
        if key == arcade.key.E:
            self.guardAdrian = False
        if key == arcade.key.N:
            self.attackGabibbo = False
        if key == arcade.key.M:
            self.guardGabibbo = False
        

        



def main():
    gioco = Giochino()
    arcade.run()


if __name__ == "__main__":
    main()