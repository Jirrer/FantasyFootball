

DraftPicks = {'testusername': []} # need to create empty arrays when game gets started


def submitPick(username, pick):
    DraftPicks[username].append(pick)

    print(DraftPicks)