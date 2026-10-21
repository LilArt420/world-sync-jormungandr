"""Episode 21 (Age of Heroes) quest log text, translated from the kRO
client's Korean quest table (System/OngoingQuestInfoList_True.lub) for this
mod. Quests the English translation already has (8882-8916, 12646-12656)
are taken from there by gen_quests.py; these are the rest.

id: (title, summary, description). Descriptions keep the client's
<NAVI> tags so the quest window can point at places.
"""


def nav(name, m, x, y):
    return '<NAVI>[%s]<INFO>%s,%d,%d,0,101,0</INFO></NAVI>' % (name, m, x, y)


EP21 = {
    # ---- The rift ----
    18334: ('A Rift Detected in the North', 'Talk to Nyar',
            'Nillem believes a rift has opened on Scale Island, near Issgard, and wants to look into it. '
            + nav('Shupapa', 'jor_tail', 233, 41) + ', waiting at the Frozen Tail, can take you to Scale Island.'),
    18335: ('The Rift on Scale Island', 'Talk to Nyar',
            'You crossed into the Scale Island of the past with Nyar. Somewhere in this time lies the source of '
            'Rasgand\'s power, and it has to be destroyed. Talk to ' + nav('Nyar', 'jor_crk_p', 105, 108) + '.'),
    18336: ('First Meeting', 'Meet someone near the rift',
            'While you were planning your next move on the Scale Island of the past, you sensed someone nearby. '
            'Meet whoever is ' + nav('near the rift', 'jor_crk_p', 95, 93) + '.'),
    18337: ('To Lunaforma', 'Talk to a soldier in Lunaforma',
            'The one you met on the Scale Island of the past was Ivan Wigner. Go with ' + nav('Ivan', 'jor_crk_p', 95, 93)
            + ' and his soldier to ' + nav('Lunaforma', 'jor_mbase', 124, 32) + '.'),
    # ---- The Georborg resistance ----
    23240: ('The Georborg Resistance', 'Listen to the argument',
            'The moment you reach Lunaforma, the Georborg resistance\'s base, you hear shouting. From the soldiers\' faces, '
            'the ones being shouted at are the resistance\'s ' + nav('captain', 'jor_mbase', 56, 152)
            + ' and vice-captain. Lehar and Nillem suggest listening quietly, out of the line of fire.'),
    23241: ('The Georborg Resistance', 'Talk to a resistance soldier',
            'The believers of Freyja, unhappy with a resistance built around Odin, left Lunaforma to look for another home. '
            'Once things calm down, a ' + nav('resistance soldier', 'jor_mbase', 54, 155) + ' waves you over.'),
    23242: ('The Georborg Resistance', 'Talk to Tan',
            'Tris welcomed you, Lehar and Nillem when you said you wanted to join. Until there is a proper task for you, '
            'you are to help Richard\'s mercenaries. The vice-captain, Tan, doesn\'t trust you, but Tris has told him to show you the way. '
            'Talk to ' + nav('Tan', 'jor_mbase', 57, 150) + '.'),
    23243: ('The Georborg Resistance', 'Talk to Richard',
            'Tan made it clear he doesn\'t trust you: if you last through the mercenaries\' training, he may think again. '
            'Head for ' + nav('Richard\'s mercenaries', 'jor_mbase', 313, 106) + ' in Lunaforma.'),
    24000: ('Richard\'s Mercenaries', 'Go to the mercenaries\' office',
            'Tan still doesn\'t trust you. Go to the ' + nav('mercenaries\' office', 'mbase_in', 289, 124)
            + ' in south-east Lunaforma and meet Richard.'),
    24001: ('Richard\'s Mercenaries', 'Talk to the man in the office',
            'The office was empty, until a ' + nav('man', 'mbase_in', 292, 127) + ' walked in. Ask him where Richard is.'),
    24002: ('Richard\'s Mercenaries', 'To Richard\'s room',
            'Richard might be in his room. Go to ' + nav('Richard\'s room', 'mbase_in', 113, 120)
            + ' in the central barracks of Lunaforma.'),
    24003: ('Richard\'s Mercenaries', 'The room next door',
            'Richard\'s room is locked. See if anyone is in the ' + nav('room next door', 'mbase_in', 113, 114) + '.'),
    24004: ('Richard\'s Mercenaries', 'Back to the office',
            'The woman from the room next door tells you to go back to the '
            + nav('mercenaries\' office', 'mbase_in', 289, 124) + '.'),
    24005: ('Richard\'s Mercenaries', 'Fill in the forms',
            'To join Richard\'s mercenaries you have to fill in the ' + nav('application forms', 'mbase_in', 299, 126) + '.'),
    24006: ('Richard\'s Mercenaries', 'Hand the forms to Valdaris',
            'Hand your filled-in forms to ' + nav('Valdaris', 'mbase_in', 302, 123) + ', at the back of the office.'),
    24007: ('Richard\'s Mercenaries', 'Talk to Tan',
            'As Valdaris checked your forms, Tan appeared. Talk to ' + nav('Tan', 'mbase_in', 302, 122) + '.'),
    24008: ('Richard\'s Mercenaries', 'Talk to Valdaris',
            'Tan left you with Valdaris and vanished again. Talk to ' + nav('Valdaris', 'jor_mbase', 316, 117)
            + ' outside the office.'),
    24009: ('Richard\'s Mercenaries', 'Follow Valdaris',
            'Valdaris will show you around Lunaforma. Follow ' + nav('Valdaris', 'jor_mbase', 243, 120) + '.'),
    24010: ('Richard\'s Mercenaries', 'Follow Valdaris',
            'You heard about the Wigner Company and the Walter fleet. On to the '
            + nav('next stop', 'jor_mbase', 145, 108) + '.'),
    24011: ('Richard\'s Mercenaries', 'Follow Valdaris',
            'You heard about the children of Lunaforma. Something is happening at the '
            + nav('training ground', 'jor_mbase', 135, 108) + '.'),
    24012: ('Richard\'s Mercenaries', 'To the training ground',
            'There\'s a commotion at the training ground in south Lunaforma. Get ' + nav('closer', 'jor_mbase', 135, 108) + '.'),
    24013: ('Richard\'s Mercenaries', 'To Richard\'s room',
            'At the training ground you found Richard being beaten up by Galaxia. Take him to '
            + nav('his room', 'mbase_in', 167, 128) + ' to patch him up.'),
    24014: ('Richard\'s Mercenaries', 'Talk to Richard',
            'Valdaris is furious. Ask ' + nav('Richard', 'mbase_in', 168, 126) + ' what the fight was about.'),
    24015: ('Richard\'s Mercenaries', 'Talk to Lee',
            'Richard and Galaxia were staging a fight for the illustrations of a combat manual. Look at '
            + nav('Lee', 'mbase_in', 166, 124) + '\'s drawings.'),
    24016: ('Richard\'s Mercenaries', 'To Galaxia\'s room',
            'Valdaris has words for Richard alone. Give them some room and go to '
            + nav('Galaxia\'s room', 'mbase_in', 167, 79) + '.'),
    24017: ('Richard\'s Mercenaries', 'Talk to Lee',
            'You heard about Galaxia and Richard. Go outside and let ' + nav('Lee', 'jor_mbase', 163, 196)
            + ' show you around.'),
    24018: ('Richard\'s Mercenaries', 'To Tris',
            'You seem to have earned a little trust. Meet ' + nav('Tris', 'jor_mbase', 168, 200) + ' in Lunaforma.'),
    23244: ('Profit and Loss', 'Talk to Tris',
            'You told Tris how it went with the mercenaries. Nillem has been sent to Alberta and Lehar to the Wigner Company, '
            'and Tris has someone to introduce to you. Talk to ' + nav('Tris', 'jor_mbase', 168, 200) + ' again.'),
    23245: ('Profit and Loss', 'Talk to Tris',
            'You were introduced to Heine, the wizard of Comodo, and to her newest invention: Heine\'s Tablet. '
            'Tell ' + nav('Tris', 'jor_mbase', 168, 200) + ' when you are ready for a new task.'),
    23246: ('Profit and Loss', 'Talk to Tris',
            'Heine wants you to gather Bright Eyes around Lunaforma yourself. From Tris\'s face, this was a sudden whim of hers. '
            'Hear the rest from ' + nav('Tris', 'jor_mbase', 168, 200) + '.'),
    23247: ('Profit and Loss', '1 Bright Eye',
            'Heine notices at once when something isn\'t done exactly as she said. Defeat 10 Skipskippers on the Raised Land, '
            'collect 1 Bright Eye, and report to ' + nav('Tris', 'jor_mbase', 168, 200) + '.'),
    23248: ('Profit and Loss', 'To Alberta',
            'Meanwhile Heine asked Tris to send you to Alberta. Join ' + nav('Nillem', 'jor_albe', 192, 209) + ' there.'),
    23249: ('The Black-Haired Beast', 'Talk to Tris',
            'Back at the barracks of Lunaforma, Heine\'s Tablet broke down in the middle of a call. '
            + nav('Tris', 'mbase_in', 92, 123) + ' suggests waiting until Heine calls back.'),
    23250: ('The Black-Haired Beast', 'To the private room',
            'The tablet reconnected, but Heine says it needs an overhaul and has named you her repair assistant. '
            'Tris lent you a ' + nav('private room', 'mbase_in', 21, 168) + ' in the barracks.'),
    23251: ('The Black-Haired Beast', '2 Vellelopy',
            'A remote repair never works on the first try, Heine says, so bring plenty of parts: 2 Vellelopy, from the Velellings of the Raised Land. '
            'Then return to ' + nav('Heine', 'mbase_in', 21, 168) + '.'),
    23252: ('The Black-Haired Beast', 'Help with the repair',
            'Heine has started the repair. Stay in the ' + nav('private room', 'mbase_in', 21, 168) + ' and assist her.'),
    23253: ('The Black-Haired Beast', 'Help with the repair',
            'The first attempt failed. Stay in the ' + nav('private room', 'mbase_in', 21, 168)
            + ' and assist her once more.'),
    23254: ('The Black-Haired Beast', 'Talk to Tris',
            'The tablet works, but Heine had another reason to pick you. You told her why you came from the future. '
            'Tell ' + nav('Tris', 'mbase_in', 92, 123) + ' the news.'),
    23255: ('The Black-Haired Beast', 'Go outside',
            'With what Leon found and the news you brought from the future, the Georborg resistance decided to prepare the all-out war '
            'that will end the fight with the Jormungandr cult. Then there is a loud noise outside. Go '
            + nav('outside', 'jor_mbase', 201, 192) + ' and see.'),
    # ---- Into the cult ----
    17752: ('Infiltrating the Cult', 'Enter the temple',
            'Time to act inside ' + nav('Gimle', 'jor_tmple1', 186, 72) + ', the temple of the Jormungandr cult.'),
    17753: ('Infiltrating the Cult', 'Search the temple 1',
            'Find out whether anyone in ' + nav('Gimle', 'jor_tmple1', 110, 190) + ' wants to escape.'),
    17754: ('Infiltrating the Cult', 'Search the temple 2',
            'Look for information about the ghost ship in ' + nav('Gimle', 'jor_tmple1', 186, 228) + '.'),
    17755: ('Infiltrating the Cult', 'Search the temple 3',
            'Maybe the 2nd floor of ' + nav('Gimle', 'jor_tmple1', 238, 268) + ' holds better information?'),
    17756: ('Infiltrating the Cult', 'Join the others',
            'Nothing useful. Meet the others at the meeting point in ' + nav('Gimle', 'jor_tmple1', 188, 72) + '.'),
    17757: ('Infiltrating the Cult', 'To Lunaforma',
            'Nobody found anything. Go back to ' + nav('Lunaforma', 'jor_mbase', 143, 272) + ' and think of something else.'),
    17758: ('Recruiting for Success', 'To the meeting place',
            'Meet Nadoyo at the meeting place on ' + nav('Scale Island', 'jor_crk_p', 71, 85)
            + ': Nadoyo knows the inside of the temple.'),
    17759: ('Recruiting for Success', 'Talk to Ivan',
            nav('Ivan', 'jor_crk_p', 69, 85) + ' has a proposal for those left on Scale Island...'),
    17760: ('Recruiting for Success', 'To Lunaforma',
            'The talent Ivan talked about works at the canteen of ' + nav('Lunaforma', 'jor_mbase', 166, 302)
            + '. Can you win him over?'),
    17761: ('Second Infiltration', 'To the Raised Land',
            'Join Nadoyo in the north of the ' + nav('Raised Land', 'jor_raise1', 323, 71)
            + ' and hear how to get into the temple.'),
    17762: ('Second Infiltration', 'To the temple\'s 2nd floor',
            'Meet Nadoyo, waiting in ' + nav('Gimle', 'jor_tmple1', 238, 268)
            + ', and learn what to watch out for inside the cult. You can\'t fail twice.'),
    17763: ('Second Infiltration', 'Register with the guard',
            'The guard of ' + nav('Gimle', 'jor_tmple1', 238, 268) + ' needs a moment to check the register.'),
    17764: ('Second Infiltration', 'Rescue Karmilgand',
            'Karmilgand, a high priest, is locked up somewhere in ' + nav('Gimle', 'jor_tmple1', 238, 268)
            + '. Help him escape.'),
    17765: ('Second Infiltration', 'To the Raised Land',
            'You barely got Karmilgand out. Join the others in the north of the ' + nav('Raised Land', 'jor_raise1', 323, 71) + '.'),
    17766: ('Second Infiltration', 'To Lunaforma',
            'The rescue worked. Take Karmilgand and the believers back to ' + nav('Lunaforma', 'jor_mbase', 143, 272) + '.'),
    17767: ('Second Infiltration', 'Somewhere quiet',
            'An open square is no place for this talk. Go somewhere quiet in ' + nav('Lunaforma', 'mbase_in', 116, 186) + '.'),
    17768: ('Second Infiltration', 'Talk to Reinhardt',
            'In the central barracks of ' + nav('Lunaforma', 'mbase_in', 118, 186)
            + ' everyone is talking about Reinhardt. He says he knows about the ghost ship.'),
    17769: ('Report on the Ghost Ship', 'To Maristella',
            'You have news of the ghost ship. Report to ' + nav('Maristella', 'jalbe_in', 68, 46) + ' in Alberta.'),
    # ---- The giant snake ----
    18338: ('Gathering Witnesses', 'Collect 3 accounts',
            'You decided to gather information about the giant serpent. Is it real? Hear the people who made it back to Lunaforma.'),
    18339: ('Witness 1', '', 'An exhausted soldier says he saw a vile, slimy serpent monster.'),
    18340: ('Witness 2', '', 'A believer who escaped the cult says he saw the serpent monster eat people.'),
    18341: ('Witness 3', '', 'A wounded soldier has the scars of huge scales across his back.'),
    18342: ('All Accounts Gathered!', 'Talk to Tris',
            'You have all the accounts. Report to ' + nav('Tris', 'jor_mbase', 204, 193) + ' in front of the central barracks.'),
    18343: ('Looking for Tan and Nadoyo', 'Talk to Nadoyo',
            'Tris is worried: Tan and Nadoyo haven\'t come back. Look for them in the '
            + nav('north of the Raised Land', 'jor_raise1', 199, 190) + '.'),
    18344: ('A Suspicious Place in the Temple', 'Examine the ornamental door',
            'With Tan, Nadoyo and Reinhardt you will check a suspicious spot outside Gimle. Examine the '
            + nav('ornamental door', 'jor_raise1', 128, 326) + ' outside the temple.'),
    18345: ('The Serpent\'s Lair?', 'Talk to Tris',
            'It seems the cult has made a giant serpent. Hurry back to Lunaforma and tell '
            + nav('Tris', 'jor_mbase', 204, 193) + '.'),
    18346: ('Left Out of the Last Battle', 'Talk to Nyar',
            'Tris and the resistance will face the giant serpent. Discuss what comes next with your companions in the '
            + nav('small room', 'mbase_in', 64, 184) + ' of the central barracks.'),
    18347: ('I Can\'t Sit This Out!', 'Talk to Nadoyo',
            'Heine urges you to join the battle against the serpent. Hurry to the '
            + nav('ornamental door', 'jor_raise1', 128, 326) + ' before Tris and the others face it.'),
    18348: ('Joining the Last Battle', 'Fight in the Last Battle',
            'Your comrades are searching the hidden place behind the ' + nav('ornamental door', 'jor_raise1', 128, 326)
            + ' for the giant serpent. Fight beside Tris in the last battle recorded in history.'),
    # ---- Gimle's secret ----
    18349: ('Carried Off by a Cat', 'Talk to Nyar',
            'Nyar appeared out of nowhere and carried you off. She had followed Jormungandr\'s mana to a hidden space behind the '
            + nav('ornamental altar', 'jor_tmple1', 170, 307) + ' of Gimle. Follow her.'),
    18350: ('Gimle\'s Suspicious Book', 'Press the suspicious book',
            'Behind Gimle\'s ' + nav('altar', 'jor_tmple1', 170, 307) + ' lies a hidden room with a very suspicious book. '
            'Nillem says it is some kind of mechanism and tells you to press it...'),
    18351: ('The Shining Door', 'Through the shining door',
            'Pressing the book opened a shining door below the ' + nav('altar', 'jor_tmple1', 170, 307)
            + '. Jormungandr\'s mana pours out of it. Go in!'),
    18352: ('A Real Mission at Last!', 'Break the secret altar',
            'The hidden place behind the ' + nav('altar', 'jor_tmple1', 170, 307) + ' leads further. Follow the surging mana and '
            'destroy Jormungandr\'s mana before it gathers in Rasgand.'),
    18353: ('The Source Is Cut Off', 'Talk to Nyar',
            'After all that, Nyar seems to have caught the mana meant for Rasgand. Discuss the next steps with '
            + nav('Nyar', 'jor_crk_p', 105, 108) + ' on the Scale Island of the past.'),
    # ---- Back to the present ----
    18354: ('Heine\'s Gift', 'Search the bushes',
            'Ilse el Heine called through the tablet: take the new tablet she hid in the '
            + nav('bushes', 'jor_mbase', 129, 43) + ' near the Lunaforma ferry.'),
    18355: ('Back to Scale Island', 'To Scale Island',
            'Return to the ' + nav('Scale Island', 'jor_crk', 137, 138) + ' of your own time and see whether everything went as planned.'),
    18356: ('Time to Check the Consequences', 'Talk to Nyar\'s Double',
            'Go to the Nest of Small Branches and check on Rasgand. ' + nav('Nyar\'s Double', 'jor_twig', 122, 164)
            + ' can tell how the sealed Rasgand\'s mana is doing.'),
    18357: ('Time to Settle the Curse', 'Wait, then talk to Nyar\'s Double',
            'Voglinde and Lehar went into the barrier to see the end of the curse. Wait and pray they succeed. '
            + nav('Nyar\'s Double', 'jor_twig', 122, 164) + ' will know.'),
    18358: ('Rasgand?', 'Check the Serene Sanctuary',
            'Rasgand keeps coming back to life. To check one possibility, you will go into the barrier yourself. '
            'Enter the Serene Sanctuary through ' + nav('Nyar\'s Double', 'jor_twig', 122, 164) + '.'),
    18359: ('Butterfly Effect', 'Talk to Nyar\'s Double',
            'As you thought: the Rasgand inside the barrier was not Rasgand. The mana of the shard of Ymir\'s heart was imitating him. '
            'Tell ' + nav('Nyar\'s Double', 'jor_twig', 122, 164) + '.'),
    18360: ('The Frozen Age of Heroes', 'Talk to Nyar',
            nav('Nyar', 'jor_crk', 105, 108) + ' and Nillem, closing the rift on Scale Island, say something strange has happened. Go to Scale Island.'),
    18361: ('Nyar\'s Primeval Pouch', 'Talk to Nyar', 'Nyar showed off her primeval pouch.'),
}
