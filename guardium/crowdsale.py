from boa.interop.Neo.Blockchain import GetHeight
from boa.interop.Neo.Runtime import CheckWitness
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.Storage import Get, Put
from boa.builtins import concat
from guardium.token import *
from guardium.txio import get_asset_attachments

OnKYCRegister = RegisterAction('kyc_registration', 'address')
OnTransfer = RegisterAction('transfer', 'addr_from', 'addr_to', 'amount')
OnRefund = RegisterAction('refund', 'addr_to', 'amount')


def kyc_register(ctx, args):
    # TOKEN SALE IS OVER, NOT NEEDED
    return 0


def kyc_status(ctx, args):
    # TOKEN SALE IS OVER, NOT NEEDED
    return False


def perform_exchange(ctx):
    # TOKEN SALE IS OVER, NOT NEEDED
    return False


def can_exchange(ctx, attachments, verify_only):
    # TOKEN SALE IS OVER, NOT NEEDED
    return False


def calculate_can_exchange(ctx, amount, address, verify_only):
    # TOKEN SALE IS OVER, NOT NEEDED
    return False
