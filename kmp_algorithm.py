def build_lps(pattern):
    """Build longest prefix suffix (LPS) array for KMP algorithm."""
    lps = [0] * len(pattern)
    length = 0  # length of the previous longest prefix suffix

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
    """Search for pattern in text using the KMP algorithm. Returns True if found."""
    if pattern == "":
        return True  # empty pattern matches anything

    lps = build_lps(pattern)
    i = j = 0  # index for text and pattern

    while i < len(text):
        if pattern[j].lower() == text[i].lower():  # case-insensitive search
            i += 1
            j += 1
        if j == len(pattern):
            return True  # match found
        elif i < len(text) and pattern[j].lower() != text[i].lower():
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return False
