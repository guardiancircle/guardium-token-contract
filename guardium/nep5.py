from boa.interop.Neo.Runtime import CheckWitness, Notify
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.Storage import *
from boa.builtins import concat

from guardium.token import *


OnTransfer = RegisterAction('transfer', 'addr_from', 'addr_to', 'amount')
OnApprove = RegisterAction('approve', 'addr_from', 'addr_to', 'amount')


def handle_nep51(ctx, operation, args):

    if operation == 'name':
        return TOKEN_NAME

    elif operation == 'decimals':
        return TOKEN_DECIMALS

    elif operation == 'symbol':
        return TOKEN_SYMBOL

    elif operation == 'totalSupply':
        return Get(ctx, TOKEN_CIRC_KEY)

    elif operation == 'balanceOf':
        if len(args) == 1:
            return Get(ctx, concat('g_', args[0]))

    elif operation == 'transfer':
        if len(args) == 3:
            return do_transfer(ctx, args[0], args[1], args[2])

    elif operation == 'transferFrom':
        if len(args) == 3:
            return do_transfer_from(ctx, args[0], args[1], args[2], args[3])

    elif operation == 'approve':
        if len(args) == 3:
            return do_approve(ctx, args[0], args[1], args[2])

    elif operation == 'allowance':
        if len(args) == 2:
            return do_allowance(ctx, args[0], args[1])

    return False


def do_transfer(ctx, t_from, t_to, amount):

    if amount <= 0:
        return False

    # if wallet address is not 20 chars reject the transaction
    if len(t_to) != 20:
        return False

    # check the transaction t_from matches the address initiating the transfer
    if CheckWitness(t_from):
        from_val = Get(ctx, concat('g_', t_from))

        if from_val < amount:
            print("insufficient funds")
            return False

        if t_from == t_to:
            print("transfer to self!")
            OnTransfer(t_from, t_to, amount)
            return True

        # if the from_val equals the amount being sent delete the now empty key on the blockchain
        if from_val == amount:
            Delete(ctx, concat('g_', t_from))
        else:
            Put(ctx, concat('g_', t_from), from_val - amount)

        to_value = Get(ctx, concat('g_', t_to))

        # credit the receiving address the funds being sent
        Put(ctx, concat('g_', t_to), to_value + amount)

        # announce the transaction
        OnTransfer(t_from, t_to, amount)

        return True
    else:
        print("from address is not the tx sender")

    return False


def do_transfer_from(ctx, t_originator, t_from, t_to, amount):

    if amount <= 0:
        return False

    # check the transaction t_originator matches the address initiating the transfer
    if CheckWitness(t_originator):

        if t_from == t_to:
            print("Aborting, from and to addresses are the same")
            return False

        available_key = concat('g_', t_from, t_to)

        # if addresses lengths are invalid abort the transaction
        if len(available_key) != 42:
            return False

        available_to_to_addr = Get(ctx, available_key)

        if available_to_to_addr < amount:
            print("Insufficient funds approved")
            return False

        from_balance = Get(ctx, concat('g_', t_from))

        if from_balance < amount:
            print("Insufficient tokens in from balance")
            return False

        to_balance = Get(ctx, concat('g_', t_to))

        # credit the address being sent funds
        Put(ctx, concat('g_', t_to), to_balance + amount)

        # debit the address sending funds
        Put(ctx, concat('g_', t_from), from_balance - amount)

        print("transfer complete")

        new_allowance = available_to_to_addr - amount

        if new_allowance == 0:
            print("balance is zero, removing storage key")
            Delete(ctx, available_key)
        else:
            print("updating allowance to new allowance")
            Put(ctx, available_key, new_allowance)

        OnTransfer(t_from, t_to, amount)

        return True

    else:
        print("originator address is not the tx sender")
        return False


def do_approve(ctx, t_owner, t_spender, amount):

    if len(t_spender) != 20:
        return False

    if not CheckWitness(t_owner):
        return False

    if amount < 0:
        return False

    approval_key = concat('g_', t_owner, t_spender)

    if amount == 0:
        Delete(ctx, approval_key)
    else:
        Put(ctx, approval_key, amount)

    OnApprove(t_owner, t_spender, amount)

    return True


def do_allowance(ctx, t_owner, t_spender):

    return Get(ctx, concat('g_', t_owner, t_spender))
