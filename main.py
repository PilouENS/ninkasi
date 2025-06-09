from pywebio.input import input, TEXT, radio
from pywebio.output import put_table, put_text, put_buttons, clear, put_html, put_scope
from pywebio import start_server

score_labels = ["15", "30", "45", "AV", "GAGNE 🎉"]
players = []
scores = {}
game_wins = {}
pending_win = None  # Pour stocker temporairement la demande de validation

def draw_table():
    clear()

    put_html('<h1 style="text-align:center; color:#900C3F;">🎾 Ninkasi 🤟</h1>')

    header = ['Score'] + players
    table = [header]

    for i, label in enumerate(score_labels):
        row = [label]
        for player in players:
            if scores[player] == i:
                row.append('✅')
            else:
                row.append(put_buttons(
                    ['⬤'],
                    small=True,
                    onclick=[lambda p=player, s=i: set_score(p, s)]
                ))
        table.append(row)

    put_html('<div style="display: flex; justify-content: center;">')
    put_table(table)
    put_html('</div>')

    put_html('<h3 style="text-align:center;">🧮 Jeux gagnés</h3>')
    game_table = [['Joueur', 'Jeux gagnés']]
    for player in players:
        game_table.append([player, str(game_wins[player])])

    put_html('<div style="display: flex; justify-content: center;">')
    put_table(game_table)
    put_html('</div>')

    if pending_win:
        confirm_victory(pending_win)


def set_score(player, score_index):
    global pending_win

    if score_index == len(score_labels) - 1:
        pending_win = player  # marquer la victoire en attente
    else:
        scores[player] = score_index
        pending_win = None
    draw_table()

def confirm_victory(player):
    choice = radio(f"Confirmer que {player} a gagné cette manche ?", options=["Oui", "Non"])
    if choice == "Oui":
        game_wins[player] += 1
        for p in players:
            scores[p] = -1
    global pending_win
    pending_win = None
    draw_table()

def main():
    global players, scores, game_wins, pending_win
    p1 = input("Nom du joueur 1 : ", type=TEXT)
    p2 = input("Nom du joueur 2 : ", type=TEXT)
    p3 = input("Nom du joueur 3 : ", type=TEXT)
    players = [p1, p2, p3]
    scores = {player: -1 for player in players}
    game_wins = {player: 0 for player in players}
    pending_win = None

    draw_table()

start_server(main, port=8080)
