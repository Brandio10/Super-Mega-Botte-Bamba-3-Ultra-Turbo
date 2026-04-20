import arcade
import random


SCREENWIDTH = 1272
SCREENHEIGHT = 636
GRAVITY = 1
PLAYER_JUMP_SPEED1 = 25
PLAYER_JUMP_SPEED2 =18.8


class SpriteAnimato(arcade.Sprite):
    def __init__(self, scala: float = 1.0):
        super().__init__(scale=scala)
        self.animazioni = {}          # nome -> dizionario con textures, durata_frame, loop
        self.animazione_corrente = None
        self.animazione_default = None
        self.tempo_frame = 0.0
        self.indice_frame = 0

    def aggiungi_animazione(
        self,
        nome: str,
        percorso: str,
        frame_width: int,
        frame_height: int,
        num_frame: int,
        colonne: int,
        durata: float,
        loop: bool = True,
        default: bool = False,
        riga: int = 0,
    ):
        """
        Carica uno spritesheet e registra l'animazione con il nome dato.

        loop    : se True l'animazione riparte dall'inizio quando finisce
        default : se True questa è l'animazione di riposo (quella a cui si
                  torna automaticamente quando una animazione non in loop finisce)
        riga    : riga dello spritesheet da cui estrarre i frame (0 = prima riga)
        """
        sheet = arcade.load_spritesheet(percorso)
        offset = riga * colonne
        tutti = sheet.get_texture_grid(
            size=(frame_width, frame_height),
            columns=colonne,
            count=offset + num_frame,
        )
        self._registra(nome, tutti[offset:], durata, loop, default)

    def _registra(self, nome, textures, durata, loop, default=False):
        """Usato internamente per registrare texture già caricate."""
        self.animazioni[nome] = {
            "textures": textures,
            "durata_frame": durata / len(textures),
            "loop": loop,
        }
        if default or self.animazione_default is None:
            self.animazione_default = nome
        if self.animazione_corrente is None:
            self._vai(nome)

    def imposta_animazione(self, nome: str):
        """Cambia animazione (ignorata se è già quella attiva, evita reset del frame)."""
        if nome != self.animazione_corrente:
            self._vai(nome)

    def _vai(self, nome: str):
        self.animazione_corrente = nome
        self.indice_frame = 0
        self.tempo_frame = 0.0
        self.texture = self.animazioni[nome]["textures"][0]

    def update_animation(self, delta_time: float = 1 / 60):
        anim = self.animazioni[self.animazione_corrente]
        self.tempo_frame += delta_time

        if self.tempo_frame < anim["durata_frame"]:
            return  # non è ancora il momento di cambiare frame

        self.tempo_frame -= anim["durata_frame"]
        prossimo = self.indice_frame + 1

        if prossimo < len(anim["textures"]):
            # Frame successivo nello stesso ciclo
            self.indice_frame = prossimo
        elif anim["loop"]:
            # Fine ciclo: ricominciamo da capo
            self.indice_frame = 0
        else:
            # Animazione finita e non looppa: torna alla default
            self._vai(self.animazione_default)
            return

        self.texture = anim["textures"][self.indice_frame]


class AdrianAnimation(SpriteAnimato):
    def __init__(self):
        # Usiamo scala 0.1 o simile se 680x1000 è troppo grande per lo schermo
        super().__init__(scala=0.3) 
        
        sheet = arcade.load_spritesheet("./AdrianCalcioSpriteSheet.png")
# Carichiamo la griglia 5x5
        tutti_i_frame = sheet.get_texture_grid(size=(256, 256), columns=5, count=25)

# Selezioniamo solo l'ultimo (indice 24 per una griglia da 25)
        frame_singolo = [tutti_i_frame[24]] 

# Usiamo il metodo interno _registra che hai già nel tuo codice
        self._registra(
            nome="idle",
            textures=frame_singolo,
        durata=1.0,
        loop=True,
        default=True
        )

        # WALK (Camminata/Calcio)
        # Qui mantieni i dati dello spritesheet (256x256)
        self.aggiungi_animazione(
            nome="walk1",
            percorso="./AdrianCamminata1.png",
            frame_width=256,
            frame_height=256,
            num_frame=25,
            colonne=5,
            durata=0.5,
            loop=True,
        )
        self.aggiungi_animazione(
            nome="walk2",
            percorso="./AdrianCamminata2.png",
            frame_width=256,
            frame_height=256,
            num_frame=25,
            colonne=5,
            durata=0.5,
            loop=True,
        )

        # ATTACK
        self.aggiungi_animazione(
            nome="attack",
            percorso="AdrianCalcioSpriteSheet.png",
            frame_width=256,
            frame_height=256,
            num_frame=10,
            colonne=5,
            durata=0.3,
            loop=False,
        )


class MenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
    def on_draw(self):
        self.clear()
        arcade.draw_text("SUPER MEGA BOTTE&BAMBA 2 TURBO: ADRIAN vs GABIBBO EDITION", SCREENWIDTH / 2, SCREENHEIGHT / 2 + 100,
                         arcade.color.WHITE, font_size=33, anchor_x="center", bold=True)
        arcade.draw_text("Premi INVIO per iniziare", SCREENWIDTH / 2, SCREENHEIGHT / 2,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER or key == arcade.key.RETURN:
            battle_view = Giochino()
            battle_view.setup()
            self.window.show_view(battle_view)


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
        arcade.draw_lbwh_rectangle_filled(self.center_x,self.center_y,self.width,self.height,arcade.color.BLACK)
        Vita_Width = (self.VitaAttuale / self.MaxVita) *self.width
        if Vita_Width > 0:
            arcade.draw_lbwh_rectangle_filled(self.center_x, self.center_y, Vita_Width, self.height, arcade.color.GREEN)
        testo_vita = f"{int(self.VitaAttuale)} / {int(self.MaxVita)}"
        arcade.draw_text(testo_vita, 
                         self.center_x + 5,               
                         self.center_y + self.height / 2, 
                         arcade.color.WHITE, 
                         font_size=11, 
                         anchor_x="left",                 
                         anchor_y="center",
                         bold=True)


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
        arcade.draw_lbwh_rectangle_filled(self.center_x,self.center_y,self.width,self.height,arcade.color.BLACK)
        Vita_Width = (self.VitaAttuale / self.MaxVita) *self.width
        if Vita_Width > 0:
            arcade.draw_lbwh_rectangle_filled(self.center_x, self.center_y, Vita_Width, self.height, arcade.color.GREEN)
        testo_vita = f"{int(self.VitaAttuale)} / {int(self.MaxVita)}"
        arcade.draw_text(testo_vita, 
                         self.center_x + self.width - 5,
                         self.center_y + self.height / 2, 
                         arcade.color.WHITE, 
                         font_size=11, 
                         anchor_x="right",               
                         anchor_y="center",
                         bold=True)


class Attacco1(arcade.Sprite):
    def __init__(self,player):
        super().__init__("./pugno.png",scale= 0.1)
        self.center_x = player.center_x
        self.center_y = player.center_y
        self.distanza_percorsa = 0
        self.distanza_massima = 150
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
        self.distanza_percorsa = 175
        self.distanza_massima = 0
        self.speed = 15
        

    def update(self,delta_time):
        self.center_x -= self.speed
        self.distanza_percorsa -= self.speed
        if self.distanza_percorsa <= self.distanza_massima:
            self.remove_from_sprite_lists()


class Giochino(arcade.Window):
    
    def __init__(self):
        super().__init__(SCREENWIDTH,SCREENHEIGHT,"Super Botte&Bamba 2 Turbo: ADRIAN vs GABIBBO EDITION")
    
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
        self.guardAdrian = False
        self.guardGabibbo = False
        self.adrian_morto = False
        self.gabibbo_morto = False
        self.lista_potere = arcade.SpriteList()
        self.setup()



    def setup(self):
        self.lista_Gabibbo.clear()
        self.lista_Adrian.clear()
        self.wall_list.clear()
        self.lista_potere.clear()


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
        self.texture_gabibbo_morto = arcade.load_texture("Gabibbo.png")


        self.sprite_adrian = AdrianAnimation()
        self.sprite_adrian.center_x = 200
        self.sprite_adrian.center_y = 250
        self.sprite_adrian.scale = 4.3
        self.lista_Adrian.append(self.sprite_adrian)
        self.texture_adrian_morto = arcade.load_texture("Adrian.png")

        self.immagine_fine1 = arcade.load_texture("Vittoria Adrian.png")
        self.immagine_fine2 = arcade.load_texture("Vittoria Gabibbo.png")
        self.immagine_fine3 = arcade.load_texture("Pareggio.png")



        self.physics_engine_gabibbo = arcade.PhysicsEnginePlatformer(self.sprite_gabibbo, walls=self.wall_list, gravity_constant=GRAVITY)
        self.physics_engine_adrian = arcade.PhysicsEnginePlatformer(self.sprite_adrian, walls=self.wall_list, gravity_constant=GRAVITY)


        self.BarraVitaAdrian = Vita1()
        self.BarraVitaGabibbo = Vita2()


    def on_update(self, delta_time: float) -> bool | None:

        self.sprite_adrian.update_animation(delta_time)

        # --- LOGICA ANIMAZIONI CORRETTA ---
        if self.muovi_destraAdrian:
            self.sprite_adrian.imposta_animazione("walk1")
            
        elif self.muovi_sinistraAdrian: # Usiamo elif per collegarli
            self.sprite_adrian.imposta_animazione("walk2")
            
        elif self.sprite_adrian.animazione_corrente != "attack":
            # Torna idle solo se NON si muove in nessuna direzione E non sta attaccando
            self.sprite_adrian.imposta_animazione("idle")

        if self.muovi_destraAdrian and not self.guardAdrian:
            self.sprite_adrian.center_x += 7.5

        if self.muovi_sinistraAdrian and not self.guardAdrian:
            self.sprite_adrian.center_x -= 7.5


        if self.sprite_adrian.center_x <= 0:
            self.sprite_adrian.center_x = 1

        if self.sprite_gabibbo.center_x <= 0:
            self.sprite_gabibbo.center_x = 1

        if self.sprite_adrian.center_x >= 1272:
            self.sprite_adrian.center_x = 1271

        if self.sprite_gabibbo.center_x >= 1272:
            self.sprite_gabibbo.center_x = 1271

        if self.muovi_destraGabibbo and not self.guardGabibbo:
            self.sprite_gabibbo.center_x += 7.5
        if self.muovi_sinistraGabibbo and not self.guardGabibbo:
            self.sprite_gabibbo.center_x -= 7.5

        if self.sprite_adrian.center_y >= 600:
            self.sprite_adrian.center_y = 600

        if self.sprite_gabibbo.center_y >= 600:
            self.sprite_gabibbo.center_y = 600


        if self.BarraVitaGabibbo.VitaAttuale <= 0:
            self.BarraVitaGabibbo.VitaAttuale = 0
            self.gabibbo_morto = True
        if self.gabibbo_morto:
            self.sprite_gabibbo.texture = self.texture_gabibbo_morto
            self.sprite_gabibbo.center_y -= 20


        if self.BarraVitaAdrian.VitaAttuale <= 0:
            self.BarraVitaAdrian.VitaAttuale = 0
            self.adrian_morto = True
        if self.adrian_morto:
            self.sprite_adrian.texture = self.texture_adrian_morto
            self.sprite_adrian.center_y -= 20


        distanza_x = abs(self.sprite_adrian.center_x - self.sprite_gabibbo.center_x)
        distanza_minima = 70
        if distanza_x < distanza_minima:
            if self.sprite_adrian.center_x < self.sprite_gabibbo.center_x:
                if self.muovi_destraAdrian:
                    self.sprite_adrian.center_x -= 7.5
                if self.muovi_sinistraGabibbo:
                    self.sprite_gabibbo.center_x += 7.5
        
        self.physics_engine_adrian.update()
        self.physics_engine_gabibbo.update()

        self.lista_potere.update()


        for attacco in self.lista_potere:
            if isinstance(attacco,Attacco1):
                if arcade.check_for_collision(attacco, self.sprite_gabibbo):
                    danno = 15 if not self.guardGabibbo else 0
                    self.BarraVitaGabibbo.VitaAttuale -= danno
                    attacco.remove_from_sprite_lists()
                    continue
            elif isinstance(attacco, Attacco2):
                if arcade.check_for_collision(attacco, self.sprite_adrian):
                    danno = 15 if not self.guardAdrian else 0
                    self.BarraVitaAdrian.VitaAttuale -= danno
                    attacco.remove_from_sprite_lists()
                    continue
        if self.BarraVitaGabibbo.VitaAttuale <= 0: self.BarraVitaGabibbo.VitaAttuale = 0
        if self.BarraVitaAdrian.VitaAttuale <= 0: self.BarraVitaAdrian.VitaAttuale = 0
            
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background_image,
            arcade.LBWH(0,0,SCREENWIDTH,SCREENHEIGHT)
        )

        self.lista_Gabibbo.draw()
        self.lista_Adrian.draw()
        #self.wall_list.draw()
        #self.lista_potere.draw()
        self.BarraVitaAdrian.draw()
        self.BarraVitaGabibbo.draw()
        if self.gabibbo_morto and not self.adrian_morto:
            arcade.draw_texture_rect(
                self.immagine_fine1, 
                arcade.XYWH(SCREENWIDTH / 2, SCREENHEIGHT / 2, 400, 200))
        if self.adrian_morto and not self.gabibbo_morto:
            arcade.draw_texture_rect(
                self.immagine_fine2, 
                arcade.XYWH(SCREENWIDTH / 2, SCREENHEIGHT / 2, 400, 200))
        if self.gabibbo_morto and self.adrian_morto:
            arcade.draw_texture_rect(
                self.immagine_fine3, 
                arcade.XYWH(SCREENWIDTH / 2, SCREENHEIGHT / 2, 400, 200))
            
 
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
            attacco = Attacco1(self.sprite_adrian)
            self.lista_potere.append(attacco)
            self.sprite_adrian.imposta_animazione("attack")
        if key == arcade.key.C:
            self.guardAdrian = True
        if key == arcade.key.N:
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
    window = arcade.Window(SCREENWIDTH, SCREENHEIGHT, "Super Botte & Bamba 2 Turbo: ADRIAN vs GABIBBO EDITION")
    menu_iniziale = MenuView()
    window.show_view(menu_iniziale)
    arcade.run()


if __name__ == "__main__":
    main()