import arcade
import logging
import math
import random
import sys

import client.settings as settings
import server.interface.game_service_pb2 as gs


def hand_value(cards):
    total_value = 0
    aces = 0
    ranks_to_value = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
        '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 1,
    }

    for card in cards:
        total_value += ranks_to_value[card.rank]
        if card.rank == 'A':
            aces += 1

    while aces > 0:
        if total_value + 10 > 21:
            break
        total_value += 10
        aces -= 1

    return total_value


class Card:
    def __init__(self, suit, rank, load_sprite=True):
        self.suit = suit
        self.rank = rank
        self.face_up = True
        if load_sprite:
            self.sprite = arcade.Sprite('data/images/cards/{} {}.png'.format(suit, rank), 1.5)

class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(
            settings.screen_width_px,
            settings.screen_height_px,
            settings.window_title)

        self.location_x = 0
        self.location_y = 0
        self.deck = []
        self.my_hand = []
        self.dealer_hand = []
        self.total_time = 0
        self.you_won = None
        self.back_sprite = arcade.Sprite('data/images/cards/back.png', 1.5)

    def setup(self):
        for suit in ['diamonds', 'clubs', 'spades', 'hearts']:
            for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
                card = Card(suit, rank)
                self.deck.append(card)
        self.reshuffle()

    def reshuffle(self):
        self.you_won = None
        self.deck.extend(self.my_hand)
        self.deck.extend(self.dealer_hand)
        random.shuffle(self.deck)
        for index, card in enumerate(self.deck):
            card.sprite.center_x = 200 + index*15
            card.sprite.center_y = 500
            card.sprite.angle = 0
        self.my_hand = []
        self.dealer_hand = []
        self.hit_me()
        self.hit_me()

    def update(self, delta_time: float):
        self.total_time += delta_time
        if self.you_won:
            for index, card in enumerate(self.deck):
                card.sprite.angle += delta_time
                card.sprite.center_x += math.cos((self.total_time*10 + index)*0.2)*0.2
                card.sprite.center_y += math.sin((self.total_time*10 + index)*0.2)*0.2

    def hit_me(self):
        self.my_hand.append(self.deck.pop())
        self.my_hand[-1].sprite.center_y = 200
        self.my_hand[-1].sprite.center_x = 200 + len(self.my_hand)*15

    def hit_dealer(self):
        self.dealer_hand.append(self.deck.pop())
        self.dealer_hand[-1].sprite.center_y = 200
        self.dealer_hand[-1].sprite.center_x = 600 + len(self.dealer_hand)*15

    def on_draw(self):
        arcade.start_render()
        for card in self.deck:
            if self.you_won:
                card.sprite.draw()
            else:
                self.back_sprite.center_x = card.sprite.center_x
                self.back_sprite.center_y = card.sprite.center_y
                self.back_sprite.draw()
        for card in self.my_hand:
            card.sprite.draw()
        for card in self.dealer_hand:
            card.sprite.draw()
        arcade.draw_text('Your hand value: {}'.format(hand_value(self.my_hand)), 180, 50, arcade.color.WHITE, 24,)
        arcade.draw_text('Dealer\'s hand value: {}'.format(hand_value(self.dealer_hand)), 580, 50, arcade.color.WHITE, 24,)
        if self.you_won == True:
            arcade.draw_text('You won!', 400, 100, arcade.color.WHITE, 24,)
        if self.you_won == False:
            arcade.draw_text('You lost!', 400, 100, arcade.color.WHITE, 24,)

    def play_dealer(self):
        logging.info('Dealer\'s turn.')
        while hand_value(self.dealer_hand) < 17:
            self.hit_dealer()
        self.you_won = (hand_value(self.my_hand) <= 21 and hand_value(self.my_hand) > hand_value(self.dealer_hand)) or hand_value(self.dealer_hand) > 21

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            logging.info('Escape pressed. Closing game.')
            self.close()
        if self.you_won is None and symbol == arcade.key.SPACE:
            self.hit_me()
            if hand_value(self.my_hand) > 21:
                self.play_dealer()
        if self.you_won is None and symbol == arcade.key.Q:
            self.play_dealer()
        if symbol == arcade.key.R:
            self.reshuffle()

    def update_state(self, state: gs.StateResponse):
        if state.location_x is not None:
            self.location_x = state.location_x
        if state.location_y is not None:
            self.location_y = state.location_y
