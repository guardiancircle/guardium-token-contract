"""
GUARDIUM TOKEN SETTINGS

NOTE: THIS IS GUARDIUM TOKEN V2 (GRDM)

THIS CONTRACT WAS BUILT TO REPLACE GUARDIUM V1 (GDM) AS A VULNERABILITY
WAS DISCOVERED IN THE CODEBASE THAT THE ORIGINAL CONTRACT WAS DERIVED FROM

GRDM IS REPLACING GDM VIA AN AIRDROP TO EXISTING TOKEN HOLDERS
"""

from boa.interop.Neo.Storage import *


# This is the script hash of the address for the owner of the token
# This can be found in ``neo-python`` with the walet open, use ``wallet`` command
# TOKEN_OWNER = b'#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9'  # DEV PRIVNET
TOKEN_OWNER = b'\xb3\xc0\xa3\xef\\\x98\x94\xdf\xfb\x07B\xb5\xc8\x18\xa7\x07"\x19\xc27'  # MAIN & TESTNET


TOKEN_NAME = 'Guardium'
TOKEN_SYMBOL = 'GUARD'
TOKEN_DECIMALS = 8
TOKEN_INITIAL_AMOUNT = 80803317 * 100000000  # 80,803,317 * 10^8
TOKEN_CIRC_KEY = b'in_circulation'


def crowdsale_available_amount(ctx):
    # TOKEN SALE IS OVER NO FURTHER GUARDIUM IS FOR SALE
    return 0


def add_to_circulation(ctx, amount):
    """
    Adds an amount of token to circlulation

    :param amount: int the amount to add to circulation
    """

    current_supply = Get(ctx, TOKEN_CIRC_KEY)

    current_supply += amount
    Put(ctx, TOKEN_CIRC_KEY, current_supply)
    return True


def get_circulation(ctx):
    """
    Get the total amount of tokens in circulation

    :return:
        int: Total amount in circulation
    """
    return Get(ctx, TOKEN_CIRC_KEY)
