from cons import *
from fltk import *

def ask_clic():
    ev = donne_ev()
    tev = type_ev(ev)
    if tev == "ClicGauche":
        print("Clic droit au point", (abscisse(ev), ordonnee(ev)))
        return (abscisse(ev), ordonnee(ev))
    return None
    