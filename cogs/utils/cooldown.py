import json
import os
import time

def cooldown(user_id, command, cooldown = 5, write = True):
    # write = false lets us check if a cooldown has elapsed without resetting it
    user_id = str(user_id)
    if os.path.isfile('users.json'):
        try:
            with open('users.json', 'r') as fp:
                cooldowns = json.load(fp)
            time_diff = time.time() - cooldowns[user_id][f'{command}.cooldown']
            # user is in database for this command
            if time_diff >= cooldown:
                if write:
                    cooldowns[user_id][f'{command}.cooldown'] = time.time()
                    with open('users.json', 'w') as fp:
                        json.dump(cooldowns, fp, sort_keys=False, indent=4)
                return True
            else:
                return False
        except KeyError:
            # user isn't in database with this command
            with open('users.json', 'r') as fp:
                cooldowns = json.load(fp)
            try:
                cooldowns[user_id][f'{command}.cooldown'] = time.time()
            except KeyError:
                # user isn't in database at all
                cooldowns[user_id] = {}
                cooldowns[user_id][f'{command}.cooldown'] = time.time()
            finally:
                if write:
                    with open('users.json', 'w') as fp:
                        json.dump(cooldowns, fp, sort_keys=False, indent=4)
                return True
    else:
        # initialize database
        if write:
            cooldowns = {user_id: {}}
            cooldowns[user_id][f'{command}.cooldown'] = time.time()
            with open('users.json', 'w') as fp:
                json.dump(cooldowns, fp, sort_keys=False, indent=4)
        return True