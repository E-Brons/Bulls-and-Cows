#!/usr/bin/env python3
'''
Solve and play Bulls and cows
Author: Elkana Bronstein
Date: Jan 2022
'''

from random import randint
import argparse

class BullsAndCowsSecret:
    def __init__(self, value: str):
        self.val_list = self.val_str_to_list(value)

    @staticmethod
    def is_digit(d: int):
        return d>=0 and d<10

    @staticmethod
    def is_value_valid(val_list: list):
        try:
            # check that all items are unique
            if len(set(val_list)) != len(val_list):
                return False
            # check that all items are digits
            if any([not(BullsAndCowsSecret.is_digit(d)) for d in val_list]):
                return False
            #all checks pass
            return True
        except:
            # probably wrong item type
            return False

    @staticmethod
    def val_str_to_list(value: str):
        vlist = [int(d) for d in value]
        if BullsAndCowsSecret.is_value_valid(vlist):
            return vlist
        raise ValueError(value)

    def n_digits(self):
        return len(self.val_list)

    def digit_test(self, d:int, idx:int):
        if not (self.is_digit(d) and self.is_digit(idx)) or idx >= self.n_digits():
            raise ValueError(d)
        if d in self.val_list:
            if d == self.val_list[idx]:
                return "bull"
            else:
                return "cow"
        else:
            return "none"

    def combination_test(self, value: str):
        if len(value) != self.n_digits():
            raise ValueError(value)

        d = dict(bull = 0,
                 cow = 0,
                 none = 0)

        for idx,v in enumerate(self.val_str_to_list(value)):
            digit_res = self.digit_test(int(v),idx)
            d[digit_res] += 1

        return d

class BullsAndCowsCalc:
    def __init__(self, secret: BullsAndCowsSecret):
        self.secret = secret
        self.permutations = list()
        self.gen_permutations()

    def gen_permutations(self):
        for c in range(10**self.secret.n_digits()):
            try:
                cand = BullsAndCowsSecret(str(c).zfill(self.secret.n_digits()))
                self.permutations.append(cand)
            except ValueError:
                continue

    def combination_test(self, calc_value: str):
        calc_combination_result = self.secret.combination_test(calc_value)
        self.permutations = [p for p in self.permutations if p.combination_test(calc_value) == calc_combination_result]
        return calc_combination_result

    def get_status(self):
        return self.permutations


def arg_parse():
    parser = argparse.ArgumentParser(description='Game or Calc arguments')
    # input signals source(s). required either of 'dump' or 'sigdict'
    game_or_calc = parser.add_mutually_exclusive_group(required=True)
    game_or_calc.add_argument('-game', action='store_true', default=False, help='play a game')
    game_or_calc.add_argument('-calc', action='store_true', default=False, help='calc result')
    # other argument
    parser.add_argument('-secret', type=str, required=False, help='use this vaue as the secret')
    parser.add_argument('-n_digits', type=int, default=4, help='number of digits')
    parser.add_argument('-max_steps', type=int, default=5, help='number of max steps')
    parser.add_argument('-hint_level', type=int, default=2, help='hint level')

    return parser.parse_args()


def get_input():
    return input("Enter new combination:")


def game(secret : BullsAndCowsSecret, max_steps :int, hint_level: int):
    calc = BullsAndCowsCalc(secret)
    for step in range(max_steps):
        while True:
            try:
                guess = get_input()
                ret = calc.combination_test(guess)
                break
            except:
                print(f"{guess} is not a valid guess")
        stat = calc.get_status()
        print(f"Guess #{step+1:<3}/{max_steps} '{guess}' has {ret['bull']:<2} Bulls & {ret['cow']:<2} Cows")
        if ret['bull'] == secret.n_digits():
            print(" Congrats!! You made it!!")
            return
        if hint_level>=1:
            if len(stat) == 1:
                print(" Almost there - one option left...")
            else:
                print(f" There are still {len(stat)} combinations possible")
        if hint_level>=2:
            print("  Possible options are:")
            for s in stat:
                print(f"   {s.val_list}")

    print(f'Sorry. You reached max out of tries ({max_steps})')

#
# Run main
#
if __name__ == "__main__":
    args = arg_parse()
    if args.secret:
        secret = BullsAndCowsSecret(args.secret)
    else:
        secret = None
        while secret is None:
            cand = randint(0, 10**args.n_digits)
            try:
                secret = BullsAndCowsSecret(f"{args.n_digits:0>8}")
            except:
                pass


    if args.game:
        game(secret, args.max_steps, args.hint_level)
    #elif args.calc:
    #    calc(secret)
    else:
        print(f"Wrong args {args}")