#!/usr/bin/python
import random

NUM_CMDS = 200000
NUM_TEAMS = 777
ID_LOW = -80
ID_HIGH = 400
STR_LOW = -50
STR_HIGH = 400
TEAM_LOW = -5
TEAM_HIGH = NUM_TEAMS+5
FACTOR_LOW = -3
FACTOR_HIGH = 4


class Troll:
    def __init__(self, troll_id, troll_str):
        self.id = troll_id
        self.str = troll_str
        self.team = -1


def main():
    trolls = {}
    groups = range(0, NUM_TEAMS)
    cmd_dict = {1: 'AddTroll',
                2: 'AssignTroll',
                3: 'TeamUpgrade',
                4: 'JoinGroups',
                5: 'GetGroup',
                6: 'GetStrongestTroll',
                7: 'GetNumOfTrollsInRange'}
    result_dict = {1: 'Success',
                   2: 'Failure',
                   3: 'Invalid_input'}
    in_file = open('test.in', 'wb')
    out_file = open('test.out', 'wb')
    in_file.write('Init ' + str(NUM_TEAMS) + '\n')
    out_file.write('Init done.\n')

    for i in range(0, NUM_CMDS):
        if i < 20:
            troll_id = random.randint(ID_LOW, ID_HIGH)
            troll_str = random.randint(STR_LOW, STR_HIGH)
            in_file.write(cmd_dict[1] + ' ' + str(troll_id) + ' ' + str(troll_str) + '\n')
            # invalid input
            if troll_id < 0 or troll_str < 0:
                out_file.write(cmd_dict[1] + ': ' + result_dict[3] + '\n')
            # failure - troll exists
            elif troll_id in trolls.keys():
                out_file.write(cmd_dict[1] + ': ' + result_dict[2] + '\n')
            # success
            else:
                out_file.write(cmd_dict[1] + ': ' + result_dict[1] + '\n')
                trolls[troll_id] = Troll(troll_id, troll_str)
        else:
            cmd = random.randint(1, 7)
            # AddTroll
            if cmd == 1:
                troll_id = random.randint(ID_LOW, ID_HIGH)
                troll_str = random.randint(STR_LOW, STR_HIGH)
                in_file.write(cmd_dict[1] + ' ' + str(troll_id) + ' ' + str(troll_str) + '\n')
                # invalid input
                if troll_id < 0 or troll_str < 0:
                    out_file.write(cmd_dict[1] + ': ' + result_dict[3] + '\n')
                # failure - troll exists
                elif troll_id in trolls.keys():
                    out_file.write(cmd_dict[1] + ': ' + result_dict[2] + '\n')
                # success
                else:
                    out_file.write(cmd_dict[1] + ': ' + result_dict[1] + '\n')
                    trolls[troll_id] = Troll(troll_id, troll_str)
            # AssignTroll
            elif cmd == 2:
                troll_id = random.randint(ID_LOW, ID_HIGH)
                troll_team = random.randint(TEAM_LOW, TEAM_HIGH)
                in_file.write(cmd_dict[2] + ' ' + str(troll_id) + ' ' + str(troll_team) + '\n')
                # invalid input
                if troll_id < 0 or troll_team < 0 or troll_team >= NUM_TEAMS:
                    out_file.write(cmd_dict[2] + ': ' + result_dict[3] + '\n')
                # failure - troll exists or assigned
                elif troll_id not in trolls.keys() or (trolls[troll_id].team != -1 and
                                                               trolls[troll_id].team != troll_team):
                    out_file.write(cmd_dict[2] + ': ' + result_dict[2] + '\n')
                else:
                    out_file.write(cmd_dict[2] + ': ' + result_dict[1] + '\n')
                    trolls[troll_id].team = troll_team
            # TeamUpgrade
            elif cmd == 3:
                troll_team = random.randint(TEAM_LOW, TEAM_HIGH)
                factor = random.randint(FACTOR_LOW, FACTOR_HIGH)
                in_file.write(cmd_dict[3] + ' ' + str(troll_team) + ' ' + str(factor) + '\n')
                # invalid input
                if troll_team < 0 or factor < 1 or troll_team >= NUM_TEAMS:
                    out_file.write(cmd_dict[3] + ': ' + result_dict[3] + '\n')
                else:
                    out_file.write(cmd_dict[3] + ': ' + result_dict[1] + '\n')
                    for troll in trolls.keys():
                        if trolls[troll].team == troll_team:
                            trolls[troll].str = trolls[troll].str * factor
            # JoinGroups
            elif cmd == 4:
                team1 = random.randint(TEAM_LOW, TEAM_HIGH)
                team2 = random.randint(TEAM_LOW, TEAM_HIGH)
                in_file.write(cmd_dict[4] + ' ' + str(team1) + ' ' + str(team2) + '\n')
                # invalid input
                if team1 < 0 or team2 < 0 or team1 >= NUM_TEAMS or team2 >= NUM_TEAMS:
                    out_file.write(cmd_dict[4] + ': ' + result_dict[3] + '\n')
                # failure - same teams already
                elif groups[team1] == groups[team2]:
                    out_file.write(cmd_dict[4] + ': ' + result_dict[2] + '\n')
                else:
                    out_file.write(cmd_dict[4] + ': ' + result_dict[1] + '\n')
                    group2 = groups[team2]
                    group1 = groups[team1]
                    for j in range(0, NUM_TEAMS):
                        if groups[j] == group2:
                            groups[j] = group1
            # GetGroup
            elif cmd == 5:
                troll_id = random.randint(ID_LOW, ID_HIGH)
                in_file.write(cmd_dict[5] + ' ' + str(troll_id) + '\n')
                # invalid input
                if troll_id < 0:
                    out_file.write(cmd_dict[5] + ': ' + result_dict[3] + '\n')
                # failure - troll doesn't exist or unassigned
                elif troll_id not in trolls.keys() or trolls[troll_id].team == -1:
                    out_file.write(cmd_dict[5] + ': ' + result_dict[2] + '\n')
                else:
                    out_file.write(cmd_dict[5] + ': ' + result_dict[1] + ' ' +
                                   str(groups[trolls[troll_id].team]) + '\n')
            # GetStrongestTroll
            elif cmd == 6:
                group_id = random.randint(TEAM_LOW, TEAM_HIGH)
                in_file.write(cmd_dict[6] + ' ' + str(group_id) + '\n')
                # invalid input
                if group_id < 0 or group_id >= NUM_TEAMS:
                    out_file.write(cmd_dict[6] + ': ' + result_dict[3] + '\n')
                else:
                    max_id = -1
                    max_str = -1
                    for troll in trolls.keys():
                        if trolls[troll].team == -1:
                            continue
                        if groups[trolls[troll].team] == group_id:
                            if trolls[troll].str > max_str:
                                max_id = trolls[troll].id
                                max_str = trolls[troll].str
                            elif trolls[troll].str == max_str:
                                if trolls[troll].id < max_id:
                                    max_id = trolls[troll].id
                                    max_str = trolls[troll].str
                    # failure - no trolls in group
                    if max_id == -1:
                        out_file.write(cmd_dict[6] + ': ' + result_dict[2] + '\n')
                    else:
                        out_file.write(cmd_dict[6] + ': ' + result_dict[1] + ' ' + str(max_id) + '\n')
                # GetNumOfTrollsInRange
            else:
                mini = random.randint(STR_LOW, STR_HIGH/2)
                maxi = random.randint(STR_LOW * 2, STR_HIGH)
                in_file.write(cmd_dict[7] + ' ' + str(mini) + ' ' + str(maxi) + '\n')
                # invalid input
                if mini < 0 or mini >= maxi:
                    out_file.write(cmd_dict[7] + ': ' + result_dict[3] + '\n')
                else:
                    count = 0
                    for troll in trolls.keys():
                        if (trolls[troll].str > mini) and (trolls[troll].str <= maxi):
                            count += 1
                    out_file.write(cmd_dict[7] + ': ' + result_dict[1] + ' ' + str(count) + '\n')

    in_file.write('Quit\n')
    out_file.write('Quit done.\n')
    in_file.close()
    out_file.close()

if __name__ == "__main__":
    main()
