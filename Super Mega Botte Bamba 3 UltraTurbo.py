import arcade
import random

SCREENWIDTH = 1272
SCREENHEIGHT = 636
GRAVITY = 1
PLAYER_JUMP_SPEED1 = 25
PLAYER_JUMP_SPEED2 =18.8

class Vita1(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.center_x = 10
        self.center_y = 600
        self.width = 300
        self.height = 25
        self.MaxVita = 1000
        self.VitaAttuale = self.MaxVita

    def draw(self):
        Vita_Width = (self.VitaAttuale / self.MaxVita) *self.width
        arcade.draw_lbwh_rectangle_filled(self.center_x,self.center_y,self.width,self.height,arcade.color.BLACK)
        x_offset = (self.width - Vita_Width) / 2
        arcade.draw_lbwh_rectangle_filled(self.center_x - x_offset,self.center_y,Vita_Width,self.height,arcade.color.GREEN)


class Vita2(arcade.Sprite):
    def __init__ (self):
        super().__init__()
        self.center_x = 952
        self.center_y = 600
        self.width = 300
        self.height = 25
        self.MaxVita = 1000
        self.VitaAttuale = self.MaxVita

    def draw(self):
        Vita_Width = (self.VitaAttuale / self.MaxVita) *self.width
        arcade.draw_lbwh_rectangle_filled(self.center_x,self.center_y,self.width,self.height,arcade.color.BLACK)
        x_offset = (self.width - Vita_Width) / 2
        arcade.draw_lbwh_rectangle_filled(self.center_x - x_offset,self.center_y,Vita_Width,self.height,arcade.color.GREEN)


class Attacco1(arcade.Sprite):
    def __init__(self,player):
        super().__init__("./pugno.png",scale= 0.1)
        self.center_x = player.center_x
        self.center_y = player.center_y
        self.distanza_percorsa = 0
        self.distanza_massima = 250
        self.speed = 15
    

    def update(self,delta_time):
        self.center_x += self.speed
        self.distanza_percorsa += self.speed
        if self.distanza_percorsa >= self.distanza_massima:
            self.remove_from_sprite_lists()


class Attacco2(arcade.Sprite):
    def __init__(self,player):
        super().__init__("./pugno.png",scale= 0.1)
        self.center_x = player.center_x
        self.center_y = player.center_y
        self.distanza_percorsa = 250
        self.distanza_massima = 0
        self.speed = 15
        

    def update(self,delta_time):
        self.center_x -= self.speed
        self.distanza_percorsa -= self.speed
        if self.distanza_percorsa <= self.distanza_massima:
            self.remove_from_sprite_lists()


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
        self.lista_potere = arcade.SpriteList()
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
        self.sprite_gabibbo.center_y = 200
        self.sprite_gabibbo.scale = 0.6
        self.lista_Gabibbo.append(self.sprite_gabibbo)


        self.sprite_adrian=arcade.Sprite("Adrian.png")
        self.sprite_adrian.center_x = 200
        self.sprite_adrian.center_y = 250
        self.sprite_adrian.scale = 0.5
        self.lista_Adrian.append(self.sprite_adrian)


        self.physics_engine_gabibbo = arcade.PhysicsEnginePlatformer(self.sprite_gabibbo, walls=self.wall_list, gravity_constant=GRAVITY)
        self.physics_engine_adrian = arcade.PhysicsEnginePlatformer(self.sprite_adrian, walls=self.wall_list, gravity_constant=GRAVITY)


        self.BarraVitaAdrian = Vita1()
        self.BarraVitaGabibbo = Vita2()


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
        self.lista_potere.update()


        for attacco in self.lista_potere:
            if isinstance(attacco,Attacco1):
                collisione = arcade.check_for_collision(attacco,self.sprite_gabibbo)
                if collisione:
                    attacco.remove_from_sprite_lists()
                    self.BarraVitaGabibbo.VitaAttuale -= 20
                if self.BarraVitaGabibbo.VitaAttuale <= 0:
                    self.BarraVitaGabibbo.VitaAttuale = 0
                if self.guardGabibbo:
                    self.BarraVitaGabibbo.VitaAttuale += 20
                    if self.BarraVitaGabibbo.VitaAttuale > self.BarraVitaGabibbo.MaxVita:
                        self.BarraVitaGabibbo.VitaAttuale = self.BarraVitaGabibbo.MaxVita

        for attacco in self.lista_potere:
            if isinstance(attacco,Attacco2):
                collisione = arcade.check_for_collision(attacco,self.sprite_adrian)
                if collisione:
                    attacco.remove_from_sprite_lists()
                    self.BarraVitaAdrian.VitaAttuale -= 20
        if self.BarraVitaAdrian.VitaAttuale <= 0:
            self.BarraVitaAdrian.VitaAttuale = 0
        if self.guardAdrian:
            self.BarraVitaAdrian.VitaAttuale += 20
            if self.BarraVitaAdrian.VitaAttuale > self.BarraVitaAdrian.MaxVita:
                self.BarraVitaAdrian.VitaAttuale = self.BarraVitaAdrian.MaxVita


        
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background_image,
            arcade.LBWH(0,0,SCREENWIDTH,SCREENHEIGHT)
        )

        self.lista_Gabibbo.draw()
        self.lista_Adrian.draw()
        #self.wall_list.draw()
        self.lista_potere.draw()
        self.BarraVitaAdrian.draw()
        self.BarraVitaGabibbo.draw()
 

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            if self.physics_engine_adrian.can_jump():
                self.sprite_adrian.change_y = PLAYER_JUMP_SPEED1
        if key == arcade.key.D:
            self.muovi_destraAdrian = True
        if key == arcade.key.A:
            self.muovi_sinistraAdrian = True
        if key == arcade.key.UP:
            if self.physics_engine_gabibbo.can_jump():
                self.sprite_gabibbo.change_y = PLAYER_JUMP_SPEED2
        if key == arcade.key.RIGHT:
            self.muovi_destraGabibbo = True
        if key == arcade.key.LEFT:
            self.muovi_sinistraGabibbo = True
        if key == arcade.key.X:
            self.attackAdrian = True
            attacco = Attacco1(self.sprite_adrian)
            self.lista_potere.append(attacco)
        if key == arcade.key.C:
            self.guardAdrian = True
        if key == arcade.key.N:
            self.attackGabibbo = True
            attacco = Attacco2(self.sprite_gabibbo)
            self.lista_potere.append(attacco)
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
        if key == arcade.key.X:
            self.attackAdrian =False
        if key == arcade.key.C:
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