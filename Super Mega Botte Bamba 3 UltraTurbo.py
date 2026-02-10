import arcade
import random

SCREENWIDTH = 1272
SCREENHEIGHT = 636

class Giochino(arcade.Window):
    def __init__(self):
        super().__init__(SCREENWIDTH,SCREENHEIGHT,"Super Mega Botte&Bamba 3 Ultra Turbo")
    
        self.lista_Gabibbo= arcade.SpriteList()
        self.lista_Adrian= arcade.SpriteList()
        self.background_image = arcade.load_texture("./Sanremo.jpg")
        self.sprite = None
        self.playerSpriteList = arcade.SpriteList()
        self.setup()
        self.muovi_destra = False
        self.muovi_sinistra = False
        self.punch = False



    def setup(self):

        self.sprite=arcade.Sprite("Gabibbo.png")

        self.sprite.center_x = 1150
        self.sprite.center_y = 195
        self.sprite.scale = 0.6

        self.lista_Gabibbo.append(self.sprite)

        self.sprite=arcade.Sprite("Adrian.png")

        self.sprite.center_x = 200
        self.sprite.center_y = 225
        self.sprite.scale = 0.5

        self.lista_Adrian.append(self.sprite)


    def on_update(self, delta_time: float) -> bool | None:
        if self.muovi_destra:
            self.sprite.center_x += 10
        if self.muovi_sinistra:
            self.sprite.center_x -= 10

        
    def on_draw(self):
        self.clear()
        print(self.background_image)
        arcade.draw_texture_rect(
            self.background_image,
            arcade.LBWH(0,0,SCREENWIDTH,SCREENHEIGHT)
        )

        self.lista_Gabibbo.draw()
        self.lista_Adrian.draw()

        

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.sprite.center_y +=50
        if key == arcade.key.S:
            self.sprite.center_y -=50
        if key == arcade.key.D:
            self.muovi_destra = True
        if key == arcade.key.A:
            self.muovi_sinistra = True
        if key == arcade.key.P:
            self.punch = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.D:
            self.muovi_destra = False
        if key == arcade.key.A:
            self.muovi_sinistra = False
        if key == arcade.key.P:
            self.punch = False

        



def main():
    gioco = Giochino()
    arcade.run()


if __name__ == "__main__":
    main()