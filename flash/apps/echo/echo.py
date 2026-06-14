import os, sys, io
import M5
from M5 import *
from audio import Recorder
import time
from audio import Player
import system



label_title = None
label_tip = None
label_cnt = None
label_conut = None
label_status = None
recorder = None
player = None


flag_record = None
record_start_time = None
remaining = None
RECORD_DURATION = None
record_file_path = None


def btnA_wasClicked_event(state):
  global label_title, label_tip, label_cnt, label_conut, label_status, recorder, player, flag_record, record_start_time, remaining, RECORD_DURATION, record_file_path
  if not flag_record and not (recorder.is_recording()):
    print('start record')
    flag_record = True
    record_start_time = time.ticks_ms()
    label_status.setCursor(x=9, y=50)
    label_status.setText(str('Recording...'))
    label_status.setColor(0xff0000, 0x000000)
    recorder.record("file://flash/res/audio/" + str(record_file_path), RECORD_DURATION, False)


def setup():
  global label_title, label_tip, label_cnt, label_conut, label_status, recorder, player, flag_record, record_start_time, remaining, RECORD_DURATION, record_file_path

  M5.begin()
  Widgets.setRotation(0)
  Widgets.fillScreen(0x000000)
  label_title = Widgets.Label("Audio", 39, 5, 1.0, 0x19b1d7, 0x000000, Widgets.FONTS.Montserrat18)
  label_tip = Widgets.Label("BtnA Record", 8, 210, 1.0, 0xffffff, 0x000000, Widgets.FONTS.Montserrat18)
  label_cnt = Widgets.Label("count down", 11, 88, 1.0, 0xffffff, 0x000000, Widgets.FONTS.Montserrat18)
  label_conut = Widgets.Label("5", 48, 118, 1.0, 0xffffff, 0x000000, Widgets.FONTS.Montserrat44)
  label_status = Widgets.Label("Stop", 45, 50, 1.0, 0xffffff, 0x000000, Widgets.FONTS.Montserrat18)

  BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btnA_wasClicked_event)

  Mic.end()
  Speaker.end()
  Speaker.setPA(True)
  recorder = Recorder(8000, 16, True)
  player = Player(None)
  RECORD_DURATION = 5
  record_file_path = 'test.amr'
  player.set_vol(90)


def loop():
  global label_title, label_tip, label_cnt, label_conut, label_status, recorder, player, flag_record, record_start_time, remaining, RECORD_DURATION, record_file_path
  M5.update()
  if flag_record:
    if recorder.is_recording():
      remaining = RECORD_DURATION - (time.ticks_diff((time.ticks_ms()), record_start_time)) / 1000
      if remaining > 0:
        label_conut.setText(str(int(remaining)))
      else:
        label_conut.setText(str(0))
    else:
      flag_record = False
      label_conut.setText(str(''))
      label_cnt.setText(str(''))
      label_status.setColor(0x33cc00, 0x000000)
      label_status.setCursor(x=22, y=50)
      label_status.setText(str('Playing...'))
      player.play("file://flash/res/audio/" + str(record_file_path), pos=0, volume=-1, sync=True)
      label_status.setColor(0xffffff, 0x000000)
      label_status.setCursor(x=45, y=50)
      label_status.setText(str('Stop'))
      label_cnt.setText(str('count down'))
      label_conut.setText(str(5))
exit_hold_start = None

def check_exit():
    global exit_hold_start

    if system.key1_pressed() and system.key2_pressed():

        if exit_hold_start is None:
            exit_hold_start = time.ticks_ms()

        elif time.ticks_diff(time.ticks_ms(), exit_hold_start) > 2000:
            return True

    else:
        exit_hold_start = None

    return False
setup()
while True:
    if check_exit():
        break
    loop()
Widgets.setRotation(1)
Widgets.fillScreen(0x000000)