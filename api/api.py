
from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_restful import reqparse
from constants import JWT_SECRET_KEY
from game.game import Game
from game.hand import Hand
from models.user import User
from exceptions import *

app = Flask(__name__)
api = Api(app)

app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
jwt = JWTManager(app)


class Login(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help='Email address of the player')
        args = parser.parse_args()
        print(args)
        if not args['email']:
            return {"msg": "Missing user email."}, 400
        access_token = create_access_token(identity=args["email"])
        print(get_jwt_identity())
        try:
            user = User.get_user_by_email(args["email"])
        except UserNotFound:
            user = User(args["email"], "")
        return {"access_token": access_token}, 200

class Move(Resource):

    @jwt_required
    def post(self):  # Move can be either hit or stay.
        parser = reqparse.RequestParser()
        parser.add_argument("move", type=str, help="Move can be either hit or stay.")
        parser.add_argument("new_game", type=str, help="If true, a new game is to be prepared.")
        args = parser.parse_args()
        username, user, game = _get_username_user_and_game()
        if args.get("move") == "hit":
            game.hit()
            return {"msg": "Move ok."}, 200
        elif args.get("move") == "stay":
            game.stay()
            return {"msg": "Move ok."}, 200

        if args.get("new_game") == "true":
            game = Game(user)
            return {"msg": "The deed has been done, good sir."}

        return {"msg":
                'Request posted to /move should contain "new_game" or "move". Move can be hit or stay. New_game has to be "true"'}, 400


class Status(Resource):

    @jwt_required
    def post(self):
        def _format_ret_val():
            list_of_cards = player_hand.get_cards()
            ret = {cardno: {"suit": card.suit, "value": card.value}
                   for cardno, card in zip(("card1", "card2", "card3", "card4", "card5"), list_of_cards)
                   if card.suit and card.value}
            return ret
        parser = reqparse.RequestParser()
        parser.add_argument("get_hand", type=str, help="Get either player or computer hand.")
        parser.add_argument("get_winner", type=str, help="If true, evaluate hands and return winner.")
        args = parser.parse_args()
        username, user, game = _get_username_user_and_game()
        ret = {}
        if args.get("get_hand") == "player":
            player_hand = game.get_player_hand()
            ret = _format_ret_val()
            ret_200 = dict({"hand": ret})
        elif args.get("get_hand") == "computer":
            player_hand = game.get_computer_hand()
            ret = _format_ret_val()
            ret_200 = dict({"hand": ret})
        else:
            return {"msg": "Value of 'get_hand' has to be either 'computer' or 'player'."}, 400

        if args.get("get_winner") == "true":
            winner = game.evaluate_winner()
            ret_200 = dict(ret_200, **{"winner": winner})
        return ret_200, 200


class HelloWorld(Resource):

    @jwt_required
    def get(self):
        email = get_jwt_identity()
        return {'msg': f'Current user: {email}'}


api.add_resource(HelloWorld, '/')
api.add_resource(Login, "/login")
api.add_resource(Move, "/move")
api.add_resource(Status, "/status")

def _get_username_user_and_game():
    """Return username, user, game -tuple."""
    username = get_jwt_identity()
    user = User.get_user_by_email(username)
    game = Game(user)
    return username, user, game