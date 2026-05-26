from cons import *
from fltk import *
import time

def ask_clic():
    ev = donne_ev()
    tev = type_ev(ev)
    if tev == "ClicGauche":
        return (abscisse(ev), ordonnee(ev))
    return None
    

def sleep_for_fps(fps):
    duree_frame = 1.0 / fps
    last_tick = time.time()

    def wait():
        nonlocal last_tick
        now = time.time()
        elapsed = now - last_tick
        remaining = duree_frame - elapsed
        if remaining > 0:
            time.sleep(remaining)
        last_tick = time.time()

    return wait