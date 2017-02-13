#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import smbus


from flask import request, render_template, current_app, url_for, make_response
from flask.views import View

from lib.jsonApi import api_response
from lib.bus.digitalInOut import digiInOut


def sys_status_betrieb():
    """"""
    pins = digiInOut()
    stateMsg = {"ZUL St1": "0",
                "ZUL St2": "0",
                "FOL St1": "0",
                "FOL St2": "0",
                "LE PU": "0",
                "5": "0",
                "6": "0",
                "7": "0"}
    status = pins.getValue(0x21)
    if status&1 != 0:
        stateMsg["ZUL St1"] = "1"
    if status&2 != 0:
        stateMsg["ZUL St2"] = "1"
    if status&4 != 0:
        stateMsg["FOL St1"] = "1"
    if status&8 != 0:
        stateMsg["FOL St2"] = "1"
    if status&16 != 0:
        stateMsg["LE PU"] = "1"
    if status&32 != 0:
        stateMsg["5"] = "1"
    if status&64 != 0:
        stateMsg["6"] = "1"
    if status&128 != 0:
        stateMsg["7"] = "1"
    return stateMsg

def sys_status_stoerung():
    """"""
    pins = digiInOut()
    stateMsg = {"Quit": "0",
                "Sammelalarm": "0",
                "Frost": "0",
                "StroemZul": "0",
                "StroemFol": "0",
                "AL5": "0",
                "AL6": "0",
                "AL7": "0"}
    status = pins.getValue(0x22)
    if status&1 != 0:
        stateMsg["Quit"] = "1"
    if status&2 != 0:
        stateMsg["Sammelalarm"] = "1"
    if status&4 != 0:
        stateMsg["Frost"] = "1"
    if status&8 != 0:
        stateMsg["StroemZul"] = "1"
    if status&16 != 0:
        stateMsg["StroemFol"] = "1"
    if status&32 != 0:
        stateMsg["AL5"] = "1"
    if status&64 != 0:
        stateMsg["AL6"] = "1"
    if status&128 != 0:
        stateMsg["AL7"] = "1"
    return stateMsg

def air_get_status_stoerung():
    """"""
    status = sys_status_stoerung()
    return api_response(status)


def air_get_status_betrieb():
    """"""
    status = sys_status_betrieb()

    return api_response(status)


def air_set_status(pin,state):
    """"""
    pins = digiInOut()
    pins.setValue(0x20, pin, state)
    status = sys_status_betrieb()
    r =api_response(status,304)
    r.headers["Location"] = "/"
    return r


def air_set_level(level):
    """"""
    if(level == 0):
        air_set_status(0,0)
        air_set_status(1,0)
    if(level == 1):
        air_set_status(0,1)
        air_set_status(1,0)
    if(level == 2):
        air_set_status(0,1)
        air_set_status(1,1)
    status = sys_status_betrieb()
    r =api_response(status,304)
    r.headers["Location"] = "/"
    return r


def air_set_timer(time):
    """"""
    print time
    status = sys_status_betrieb()
    r =api_response(status,304)
    r.headers["Location"] = "/"
    return r


def air_set_temp(temp):
    """"""
    print temp
    status = sys_status_betrieb()
    r =api_response(status,304)
    r.headers["Location"] = "/"
    return r


def air_set_raucherraum_on():
    """"""
    return air_set_status(2,1)


def air_set_raucherraum_off():
    """"""
    return air_set_status(2,0)
