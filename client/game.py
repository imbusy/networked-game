import arcade
import logging

import client.settings as settings
import server.interface.game_service_pb2_grpc as gs_grpc


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(
            settings.screen_width_px,
            settings.screen_height_px,
            settings.window_title)

    def setup(self):
        card_sprite = arcade.Sprite('data/images/cards/diamonds A.png', 1.0)
        card_sprite.center_x = 200
        card_sprite.center_y = 200
        self.card_sprite = card_sprite

    def update(self, delta_time: float):
        self.card_sprite.angle += 180 * delta_time

    def on_draw(self):
        arcade.start_render()
        self.card_sprite.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            logging.info('Escape pressed. Closing game.')
            self.close()


def run(server: gs_grpc.GameStub):
    logging.info('Running game.')
    window = GameWindow()
    window.setup()
    arcade.run()
