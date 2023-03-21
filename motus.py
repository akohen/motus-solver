from pathlib import Path
from string import ascii_uppercase
from typing import DefaultDict

def get_weights(words, missing):
    seen, weights = DefaultDict(int), []
    # frequencies of letters not found yet in possible words
    for word in words:
        for i in set(word[i] for i in missing).intersection(ascii_uppercase):
            seen[i] += 1
    freqs = {i:seen[i]/len(words) for i in seen}

    # score for a letter = 0 if not present in any word, or in all words, = 1 if present in half of possible words
    # score for a word = sum of unique missing letters scores
    for word in words:
        weights.append( (sum(1 - 2*abs(freqs[c]-0.5) for c in set(word[i] for i in missing)), word) )
    return sorted(weights, reverse=True)

if __name__ == "__main__":
    with Path(__file__).parent.joinpath("ods8.fr").open(encoding="UTF-8") as f:
        words = f.read().splitlines()
        length = int(input("Word length ? "))
        constraints = {
            "correct":[(0,input("First letter ? ").upper())],
            "incorrect": [],
            "misplaced": [],
            "missing": list(range(1,length))}

        def check_word(word):
            if len(word) != length:
                return False
            
            for i, c in constraints["correct"]:
                if word[i] != c:
                    return False
                
            for i, c in constraints["misplaced"]:
                if word[i] == c or word.count(c) == 0: # TODO: if the same letter is both correct & misplaced in the same round
                    return False
                
            for _, c in constraints["incorrect"]:
                for i in constraints["missing"]:
                    if word[i] == c:
                        return False
            return True
        
        words = list(filter(check_word, words))
        while len(words) > 1:
            print(len(words), [x[1] for x in get_weights(words, constraints["missing"])[:10]])
            next_word = input("Next try ? ").upper()
            if not next_word: exit()
            for i in range(1,len(next_word)):
                result = input(next_word[i]+"? 1-Correct  2-Misplaced  3-Incorrect > ")
                if result == "1":
                    t = "correct"
                    if i in constraints["missing"]: constraints["missing"].remove(i)
                elif result == "2":
                    t = "misplaced"
                else:
                    t = "incorrect"
                constraints[t].append((i, next_word[i]))
            words = list(filter(check_word, words))
        print(words)
