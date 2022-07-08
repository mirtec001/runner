import random
import arcade


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH / 16 * 9)
SCREEN_TITLE = "Runner"

CHARACTER_SCALING = 1
TILE_SCALING = 1
PLAYER_MOVEMENT_SPEED = 7
PLAYER_JUMP_SPEED = 17
GRAVITY = 1
SPIKE_SCALING = 2


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.scene = None

        self.player_sprite = None
        self.physics_enginge = None
        self.camera = None
        self.gui_camera = None
        self.level_size = 5000
        self.level = 1

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        self.scene = arcade.Scene()

        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Platforms", use_spatial_hash=True)
        self.scene.add_sprite_list("Spikes", use_spatial_hash=True)
        self.scene.add_sprite_list("Exit", use_spatial_hash=True)

        self.player_sprite = arcade.SpriteSolidColor(32, 32, arcade.csscolor.RED)
        self.player_sprite.center_x = 32
        self.player_sprite.center_y = 64
        self.scene.add_sprite("Player", self.player_sprite)

        exit = arcade.SpriteSolidColor(8, 32, arcade.csscolor.YELLOW)
        exit.center_x = self.level_size - 4
        exit.center_y = 48
        self.scene.add_sprite("Exit", exit)

        for x in range(0, self.level_size, 32):
            wall = arcade.SpriteSolidColor(32, 32, arcade.csscolor.DARK_GREEN)
            wall.center_x = x
            wall.center_y = 16
            self.scene.add_sprite("Platforms", wall)
        
        for y in range(300, self.level_size, 400):
            flip = random.randint(0, 1)
            if flip == 1:
                self.create_spikes(y)


        self.physics_enginge = arcade.PhysicsEnginePlatformer(self.player_sprite, gravity_constant = GRAVITY, walls = self.scene["Platforms"])
    
    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        if screen_center_x < 0:
            screen_center_x = 0

        if screen_center_y < 0:
            screen_center_y = 0

        player_centered = screen_center_x, screen_center_y
        
        self.camera.move_to(player_centered)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            if self.physics_enginge.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

    def on_update(self, delta_time):
        self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED


        self.physics_enginge.update()

        self.center_camera_to_player()

        spike_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Spikes"])
        for _ in spike_hit_list:
            self.level = 0
            self.level_size = 5000
            self.setup()

        exit_hit = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Exit"])
        for _ in exit_hit:
            self.level += 1
            self.level_size += (500 * self.level) 
            self.setup()

        

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()

        self.gui_camera.use()
        self.hud_text = f"Level: {self.level}"
        arcade.draw_text(
            self.hud_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18
        )
            

    def create_spikes(self, start_point ):

        for x in range(3):
            spike = arcade.Sprite("img/sm_spike.png", SPIKE_SCALING)
            spike.center_x = start_point + (x * 32)
            spike.center_y = 48
            self.scene.add_sprite("Spikes", spike)




def main():
    window = MyGame()
    window.setup()

    arcade.run()


if __name__ == "__main__":
    main()
