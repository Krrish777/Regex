import sys

class Regex:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.alternatives = self.split_alternatives(pattern)  

    def split_alternatives(self, pattern: str):
        parts = pattern.split('|')  
        return [self.tokenize(part) for part in parts]  

    def tokenize(self, pattern: str):
        tokens = []
        i = 0
        while i < len(pattern):
            char = pattern[i]
            if char == "^":
                tokens.append({"type": "START", "value": char, "pos": i})
            elif char == "$":
                tokens.append({"type": "END", "value": char, "pos": i})
            elif char == ".":
                tokens.append({"type": "ANY", "value": char, "pos": i})
            elif char in "?*+":
                tokens.append({"type": "QUANTIFIER", "value": char, "pos": i})
            elif char == "\\" and i + 1 < len(pattern):
                escaped_char = pattern[i:i+2]
                tokens.append({"type": "ESCAPED", "value": escaped_char, "pos": i})
                i += 1
            elif char == "[":
                set_end = pattern.find("]", i)
                if set_end == -1:
                    raise ValueError("Unmatched '[' in pattern")
                tokens.append({"type": "CHARSET", "value": pattern[i:set_end+1], "pos": i})
                i = set_end
            elif char == "(":
                tokens.append({"type": "GROUP_START", "value": char, "pos": i})
            elif char == ")":
                tokens.append({"type": "GROUP_END", "value": char, "pos": i})
            else:
                tokens.append({"type": "LITERAL", "value": char, "pos": i})
            i += 1
        return tokens

    def match_token(self, token, value):
        if token["type"] == "LITERAL":
            return token["value"] == value
        elif token["type"] == "ANY":
            return True
        elif token["type"] == "CHARSET":
            char_set = token["value"][1:-1]
            return value in char_set
        elif token["type"] == "ESCAPED":
            escaped_char = token["value"][1]
            if escaped_char == "d":
                return value.isdigit()
            elif escaped_char == "w":
                return value.isalnum() or value == "_"
            elif escaped_char == 's':
                return value.isspace()
        return False

    def match_star(self, token, string, idx_string):
        count = 0
        while idx_string + count < len(string) and self.match_token(token, string[idx_string + count]):
            count += 1
        return count

    def match_plus(self, token, string, idx_string):
        count = self.match_star(token, string, idx_string)
        return count if count > 0 else -1

    def match_question(self, token, string, idx_string):
        return 1 if idx_string < len(string) and self.match_token(token, string[idx_string]) else 0

    # Main matching function
    def match_sequence(self, tokens, string, idx_string=0, idx_token=0):
        if idx_token >= len(tokens):
            return idx_string == len(string)

        token = tokens[idx_token]

        if token['type'] == 'END':
            return idx_string == len(string)

        if idx_token + 1 < len(tokens) and tokens[idx_token + 1]['type'] == 'QUANTIFIER':
            quantifier = tokens[idx_token + 1]['value']

            if quantifier == '*':
                count = self.match_star(token, string, idx_string)
            elif quantifier == '+':
                count = self.match_plus(token, string, idx_string)
                if count == -1:
                    return False
            elif quantifier == '?':
                count = self.match_question(token, string, idx_string)

            return self.match_sequence(tokens, string, idx_string + count, idx_token + 2)

        if idx_string >= len(string):
            return False

        if not self.match_token(token, string[idx_string]):
            return False

        return self.match_sequence(tokens, string, idx_string + 1, idx_token + 1)

    # Handles the alternation operator '|'
    def match(self, string: str) -> bool:
        for tokens in self.alternatives:
            if self.match_sequence(tokens, string):
                return True
        return False

if __name__ == "__main__":
    pattern = r"abc|def"
    regex = Regex(pattern)
    test_strings = ["abc", "def", "abd", "xyz"]
    for string in test_strings:
        print(f"'{string}' matches: {regex.match(string)}")
