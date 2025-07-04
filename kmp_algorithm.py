def build_lps(pattern):
    lps = [0] * len(pattern)
    length = 0 
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text, pattern):
    if pattern == "":
        return True
    
    lps = build_lps(pattern)
    i = j = 0 

    while i < len(text):
        if pattern[j].lower() == text[i].lower():
            i += 1
            j += 1
        if j == len(pattern):
            return True 
        elif i < len(text) and pattern[j].lower() != text[i].lower():
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return False
