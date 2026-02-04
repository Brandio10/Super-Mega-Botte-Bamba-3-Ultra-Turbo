import arcade
import random

x = 100
SCREENWIDTH = 1272
SCREENHEIGHT = 636

class Giochino(arcade.Window):
    def __init__(self):
        super().__init__(SCREENWIDTH,SCREENHEIGHT,"Super Mega Botte&Bamba 3 Ultra Turbo")
    
        self.lista_Gabibbo= arcade.SpriteList()
        self.lista_Adrian= arcade.SpriteList()
        self.background_image = arcade.load_texture("./Sanremo.jpg")

    def on_draw(self):
        self.clear()
        print(self.background_image)
        arcade.draw_texture_rect(
            self.background_image,
            arcade.LBWH(0,0,SCREENWIDTH,SCREENHEIGHT)
        )
    def setup(self):

        self.sprite=arcade.Sprite("Gabibbo.png")

        self.sprite.center_x = 100
        self.sprite.center_y = 525
        self.sprite.scale = 100

        self.playerSpriteList.append(self.sprite)

    def on_update(self, delta_time: float) -> bool | None:
        return super().on_update(delta_time)




def main():
    gioco = Giochino()
    arcade.run()


if __name__ == "__main__":
    main()