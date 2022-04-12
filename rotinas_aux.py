def card_color(dificuldade, na, mt_facil, facil, normal, dificil, mt_dificil):
    inverte = True
    if dificuldade == 0:
        color_df = na 
        inverte = False
    elif dificuldade == 1:
        color_df = mt_facil
        inverte = False
    elif dificuldade == 2:
        color_df = facil
    elif dificuldade == 3:
        color_df = normal
    elif dificuldade == 4:
        color_df = dificil
    elif dificuldade == 5:
        color_df = mt_dificil

    return color_df, inverte


