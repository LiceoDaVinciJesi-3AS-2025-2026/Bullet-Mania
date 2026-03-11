import bullet_mania.data.stats as stats

def bot_killed():
    stats.KILL += 1

def update_session_time(delta_time):
    stats.SESSION_TIME += delta_time

def next_horde():
    stats.HORDES += 1
