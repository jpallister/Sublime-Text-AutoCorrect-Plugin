
wiki_list = open("wiki_autocorrections")
freq_list = open("en.txt")
out = open("autocorrections", "w")

word_freqs = {}

for w in freq_list.readlines():
    s = w.split()
    word_freqs[s[0]] = int(s[1])

for line in wiki_list.readlines():
    s = line.split("->")
    oword = s[1]

    commas = map(lambda x: x.strip(), oword.split(","))
    if len(commas) > 1:
        f = {}

        for w in commas:
            if w in word_freqs:
                f[word_freqs[w]] = w
            else:
                f[0] = w

        oword = f[max(f.keys())]
        print "Multiple options for", s[0], "selecting", oword

    out.write("\"" + s[0].strip() + "\" \"" + oword.strip() + "\"")


out.close()
