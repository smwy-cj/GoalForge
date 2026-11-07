import json

d = json.load(open('source/DOC030.json', encoding='utf-8'))
T = {t['source_id']: t['text'] for t in d['turns']}
quotes = {
'T001a': "I really started practicing coding questions in grade 11 back then, because, I'm doing a computer contest for university applications.",
'T001b': "I use several platforms to practice coding questions, and I practice them mainly for the job interviews.",
'T003a': "all the companies take questions or variations of the questions from the leetcode, and it's the primary reason I use leetcode",
'T003b': "one other benefits that we can discuss like the same question with my friend",
'T003c': "I mainly use it to find find a like more explained solution",
'T003d': "but on GrreksForGreeks. It actually, like, walk through the the exact algorithm. And it's just provide more descriptions and more examples.",
'T005a': "So he just sent me, like the the leetcode question numbers to me, so I can directly practice the the question numbers and and get used to it, so I can be more prepared for my interviews",
'T005b': "if we're using the same platform he can just send me the number, and I can look at the exact question.",
'T007a': "So I chose neetcode because it gives me like a more a more concise list of the questions that I should be practicing",
'T007b': "these questions are more popular in in the job interviews",
'T007c': "I just want to try a random question to just test myself or I want to discover, like a new question, or to to see if there's a new algorithm that I haven't learned.",
'T007d': "I used NeetCode to practice the questions specific for job interviews.",
'T009a': "the main purpose is just to get a job",
'T009b': "I want to like practice my coding skills. So it would be beneficial in my daily work as a student, but also my work if I acquire a position at a company.",
'T011a': "So I basically just set a milestone that I want to finish all the array questions in this category in the neetcode",
'T013a': "so I usually just practicing code practice code questions during the interviewing season.",
'T013b': "if I just want to get a refresher, I will just do like 2 questions, and they can just be like an easy to medium level question, just to keep my brain functioning, and just to not be so rusty.",
'T013c': "usually if my mood is okay, I can do like 10 questions a day or more.",
'T015a': "I will practice daily if I know that an interview is coming is coming up",
'T015b': "Because after you practice right before the interview, your your brain is more functioning and you can prepare better",
'T015c': "So usually, I just allocate like a big chunk of time for a day.",
'T015d': "you need to like allocate a good chunk of the time for you to sit down and go through the practice go through the problems like more patiently",
'T017a': "I usually spend an hour. And then to conclude that no, I cannot do this on my own. So I will go look at the solutions",
'T017b': "it's also really important to go back to this question some other time to make sure that you don't forget",
'T017c': "but I cannot guarantee that I can solve.",
'T019a': "I usually practice medium hard questions and target like within, like 20 to 40Â min",
'T019b': "I would just allocate like, for example, like 10Â min to solve this question",
'T019c': "the difficulty level set by equal, it's not. It's not 100% correct.",
'T019d': "I will just try to practice more on this category of questions, so I can do better next time.",
'T021a': "But I usually use it for just get a rough idea of how long I should complete this question.",
'T023a': "So I can just practice the categories that I am not familiar with.",
'T023b': "if I'm in a bad mood, I can just go to an easy question to feel good about myself.",
'T023c': "So you can keep practicing the a. The question in this in the same category.",
'T025a': "so I will try to find one that I haven't complete to to practice it",
'T027a': "the platform doesn't allow me to do that, because it says like, you are submitting things too quickly",
'T027b': "I think that's really annoying for me. So that's really slows me down.",
'T027c': "the performance is not always correct",
'T027d': "It just tells me that I am using the optimal algorithm it just. But the the details they cannot really reflect.",
'T029a': "I usually just time myself on how long it takes for me to solve like a problem again for meeting problem. I'm targeting 20 to 30Â min and for hard problem, I'm targeting 20 to 40Â min.",
'T029b': "there's also, like a timer on the on the on the code on the problem. Page and you can just click, start timer once you want to start and then stop timer. Once you submit.",
'T031a': "I really want it to add more test cases, because usually this, they just give us like one to 3 test case",
'T031b': "I also wanted to like. allow the allow other users to add their custom at their test cases to the existing test case",
'T031c': "I also wanted to provide, like approximately, how much time we would need to take to solve for solve a question.",
'T033a': "it also have a feature to to track all the questions I did, and how many questions I did so after like seeing me doing like I have, like 200 questions done like it really gives me confidence.",
'T033b': "So in my job interview I can be more confident and not be so nervous when I am answering questions",
'T035a': "It helps me to gain the reading skills, to transform, like a new set, a new set of questions and then transform it to something that I practiced before.",
'T035b': "It's just really a another metric that I use to evaluate my coding skills. Whether or not I can do the weekly contest questions.",
'T037a': "I just pick the problem from the weekly contest, and I don't like enter the contest myself, because they have a specific time.",
'T037b': "I feel that in the contest. Environment might be too stressful.",
'T039a': "you can see your username on like the leaderboard or something",
'T043a': "definitely start with the easy medium questions.",
}
bad = 0
for k, q in quotes.items():
    sid = 'DOC030:' + k[:4]
    if sid not in T:
        print('NO TURN', k, sid)
        bad += 1
        continue
    c = T[sid].count(q)
    if c != 1:
        print('BAD', k, sid, 'count', c)
        bad += 1
print('done, bad =', bad)
