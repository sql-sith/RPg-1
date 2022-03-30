import random
import time


monsterNames = ["goblin", "boar", "cow", "giant spider", "changeling", "shadow", "skeleton"]


def d20():  # a basic d20 that also tells for critical fails/successes.
    d20_roll = random.randint(1, 20)
    if d20_roll == 1:
        print("Critical fail!")
        return d20_roll
    elif d20_roll == 20:
        print("Critical success!")
        return d20_roll
    else:
        return d20_roll


def buried_house():
    pass


def short_rest(player):
    d20r = random.randint(1, 20)
    wisdom_roll = d20r + player.stat_ability["wis_ability"]
    if d20r == 1:
        print("The journey has taken a toll on you and even rest seems hard to find. You try to find some comfort, but")
        print("it seems that the road calls to you without stopping. Abandoning your rest, you answer the call.")
        player.status["summonGreg"] += 1
        return

    if wisdom_roll >= 20:
        print("You sit by a tree and take in the world around you. Sometimes part of the journey is enjoying the")
        print("little parts. You watch the ants as they scramble through the grass and wonder if anyone watches you")
        print("as you do the same.\n")
        player.status["health"] = player.status["max_health"]
        player.status["poison"] = 0
        time.sleep(3)
        print("After enjoying the scenery for a beautiful moment you decide the road is calling you yet again.")
        return

    elif wisdom_roll == range(13, 20):
        print("You find an old statue to lay down beside. The statue, ancient in making, is the form of one of the")
        print("ancient rulers of the land. Vines have overtaken much of the statue but you can still see a scowl on")
        print("on the face of the once king. One hand has fallen to the weather, but the remaining one points forward.")
        print("You wonder what the Frowning King was pursuing. Maybe they just made this statue on one of his bad days")
        time.sleep(3)
        print("As you get up to continue your journey, the statue continues to point towards the horizon forever more.")
        if player.status["health"] < player.status["max_health"]:
            player.status["health"] += 1
        player.knowledge.append("Frowning King")

    elif wisdom_roll == range(5, 13):
        pass

    elif wisdom_roll > 5:
        pass


def old_man(player, enemy,):
    answer = input("You meet an old man resting by the side of the road. What do you do?\nApproach/Leave\n")
    answer = answer.lower()
    answers = ["approach", "leave"]
    while answer not in answers:
        print("Please put approach or leave.")
        answer = input().lower()

    if answer == "leave":
        print("")
        print("You share a glance with the man as you leave.")
        print("The quiet path has always been the one you favored.")
        time.sleep(0.5)
        print("And that's okay.")
        return

    if answer == "approach":
        d20r = random.randint(1, 20)
        if d20r > 17:
            print(f'You approach the man. The closer you get to him the more aged he seems.\nHe asks you to have some'
                  f' soup that looks slightly burnt. He seems to be eager to share his cooking.\nJoin/Decline')
            soup = input()
            soup = soup.lower()
            soups = ["join", "decline"]
            while soup not in soups:
                print("Please put join or decline.")
                soup = input().lower()

            if soup == "decline":
                print("You decide to stay on the safe side. After talking to the man for a time, you decide it's time")
                print("to continue your journey. As the old man fades into the distance, you focus on the path to your")
                print("front.")
                return

            if soup == "join" and player.skills["defend"] != 1:
                random.shuffle(monsterNames)
                print("The soup is disgusting, but the company is worth it. The old man tells you tales of fights long")
                print("done that he participated in. As he talks, he gives some tips of how to defend yourself when")
                print("you're in battle. As you get up to continue your journey, you are grateful for the time. His")
                print(f'last words warn you to watch out for {monsterNames[1]}s. He saw one recently.\n')
                player.skills["defend"] = 1
                player.status["health"] = player.status["max_health"]
                player.status["poison"] = 0
                print("Skill: 'Defense' learned!")
                if monsterNames[1] not in player.knownMonsters:
                    player.knownMonsters.append(monsterNames[1])
                return

            else:
                print("The soup is actually pretty good. The man seems to have learned some cooking during his time")
                print("on the road. As you talk and enjoy the night with each other, he tells you of his great fights")
                print(f"with {monsterNames[1]}s. He even gives you some tips of how to fight them if you see")
                print("them. As your time to leave comes, you know that you will treasure this night with a stranger.")
                player.status["poison"] = 0
                player.status["health"] = player.status["max_health"]
                if monsterNames[1] not in player.knownMonsters:
                    player.knownMonsters.append(monsterNames[1])
                return

        if d20r in range(7, 18):
            random.shuffle(monsterNames)
            print("The old man's eyes seem almost glazed over. He seems so tired. He faces you and seems to come to")
            print("life more. You seem to remind him of someone he used to know. He tells you of to watch out for")
            print(f'{monsterNames[1]}s. He seems to have seen a lot of them lately.')
            if monsterNames[1] not in player.knownMonsters:
                player.knownMonsters.append(monsterNames[1])

        if d20r < 7:
            print(f"It seems this wasn't a man at all, but rather a {player.knownMonsters[0]} pretending to be one.")
            d20r2 = random.randint(1, 20)
            if d20r2 < 6:
                print("The creature seems angry that you disturbed it and gets ready to attack you.")
                return player.basic_combat(enemy)

            else:
                print("The creature doesn't seem to be dangerous, but you can never be too safe. What do you do?")
                print("Attack/Leave")
                moral = input()
                moral = moral.lower()
                morals = ["attack", "leave"]
                while moral not in morals:
                    print("Please put attack or leave.")
                    moral = input().lower()

                if moral == "leave":
                    print("The creature doesn't seem to be harming anyone. You decide to focus on the journey you have")
                    print("instead of ending someone else's.")
                    return

                if moral == "attack":
                    return player.basic_combat(enemy)
