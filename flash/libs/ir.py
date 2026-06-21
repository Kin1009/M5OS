import json
import time

    from hardware import IR as _HWIR

import network


# Try hardware IR import (M5Stack firmware)
try:
except:
    _HWIR = None


_ir = None
_rx_cb = None

_last_data = None
_last_addr = None


# -------------------------
# INIT
# -------------------------

def init():
    global _ir

    if _HWIR is None:
        raise Exception("IR hardware not available")

    if _ir is None:
        _ir = _HWIR()

    return _ir


# -------------------------
# CALLBACK WRAPPER
# -------------------------

def _internal_cb(data, addr, ctrl):
    global _last_data, _last_addr, _rx_cb

    _last_data = data
    _last_addr = addr

    if _rx_cb:
        _rx_cb(data, addr, ctrl)


# -------------------------
# RX SETUP
# -------------------------

def rx_start(callback=None):
    global _rx_cb, _ir

    ir = init()

    _rx_cb = callback

    ir.rx_cb(_internal_cb)



def rx_get():
    global _last_data, _last_addr

    if _last_data is None:
        return None

    return (_last_data, _last_addr)



def rx_clear():
    global _last_data, _last_addr
    _last_data = None
    _last_addr = None


# -------------------------
# TX
# -------------------------

def tx(data, addr=0):
    ir = init()
    return ir.tx(data, addr)


# -------------------------
# OPTIONAL DEBUG
# -------------------------

def status():
    if _ir is None:
        return 'OFF'
    return 'READY'
