from web.Fast_API.game_play.game.game import Game
from web.Fast_API.game_play.player.bot import Bot
from web.Fast_API.game_play.player.player import Player
import logging


def test_game_1():
    # player = Player(name='Alex')
    bot_1 = Bot(Player(name='Bot_1'))
    bot_2 = Bot(Player(name='Bot_2'))
    bot_3 = Bot(Player(name='Bot_3'))
    bot_4 = Bot(Player(name='Bot_4'))
    bot_dict = {
        bot_1.player: bot_1,
        bot_2.player: bot_2,
        bot_3.player: bot_3,
        bot_4.player: bot_4,
    }

    game = Game()
    # game.add_player(player)
    for bot in bot_dict.keys():
        game.add_player(bot)

    active_player = game.start_round()

    while True:
        if game.cur_color == 'w':
            # bot select the color
            active_bot = bot_dict.get(active_player)
            color = bot_1.choose_random_color(last_card=game.cur_card, flip=game.flip)
            logging.info(f'#{active_bot} choose color {color}#')
            game.get_choose_color(color)
            active_player = game.cur_player
        else:
            # bot select the card
            active_player = game.cur_player
            active_bot = bot_dict.get(active_player)
            moving_card = active_bot.make_random_move(
                last_value=game.cur_value,
                last_color=game.cur_color,
                flip=game.flip
            )

            if moving_card:
                if len(active_player.card) == 1:
                    logging.info(f'Active player {active_player}, {active_bot}, cards: {active_player.card}, move with: {moving_card}')
                    logging.info(f'{active_bot} say Uno')
                if len(active_player.card) == 0:
                    logging.info(f'Active player {active_player}, {active_bot}, cards: {active_player.card}, move with: {moving_card}')
                    logging.info(f'{active_bot} win the round')
                    game.stack.get_droped_card(moving_card)
                    end_flag = game.end_round()
                    if end_flag:
                        logging.info(f'Game is over')
                        break
                    game.start_round()

            logging.info(f'{active_bot} move with card {moving_card}')
            active_player = game.get_move(card=moving_card, player=active_player)
            for player in game.player:
                logging.info(f'{player.name} cards: {player.card}, card_num: {len(player.card)} ')
            logging.info(f'Deck_len: {len(game.deck.card)}')
            logging.info(f'Stack: {game.stack.card}')





if __name__ == '__main__':
    test_game_1()
