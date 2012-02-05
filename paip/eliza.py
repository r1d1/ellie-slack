#!/usr/bin/env python

"""
**Eliza** is a pattern-matching automated psychiatrist.  Given a set of rules
in the form of input/output patterns, Eliza will attempt to recognize user input
phrases and generate relevant psychobabble responses.

Each rule is specified by an input pattern and a list of output patterns.  A
pattern is a sentence consisting of space-separated words and variables.  Input
pattern variables come in two forms: single variables and segment variables;
single variables (which take the form `?x`) match a single word, while segment
variables (which take the form `?*x`) can match a phrase.  Output pattern
variables are only single variables.  The variable names contained in an input
pattern should be the same as those in the corresponding output pattern, and
each segment variable `?*x` in an input pattern corresponds to the single
variable `?x` in the output pattern.

The rule base is specified in JSON format as a mapping from input patterns to
possible output patterns.  An example:

    {
        "hello ?x, my name is ?*y. what is yours?": [
            "listen here, ?y, that's mr. ?x to you!",
            "hello ?y. my name is dave, not ?x."
        ],
        "whatup ?*x": [
            "please use proper grammar; also, my name is not ?x."
        ]
    }

To run Eliza with this rule base, stored in a file `rules.json`, simply

`python eliza.py rules.json`

Input proceeds by reading a sentence from the user, searching through the rules
to find an input pattern that matches, replacing variables in the output
pattern, and printing the results to the user.

This implementation is inspired by Chapter 5 of "Paradigms of Artificial
Intelligence Programming" by Peter Norvig.
"""


__author__ = 'Daniel Connelly'
__email__ = 'dconnelly@gatech.edu'


import json
import sys
import random
import string


# Pattern-matching functions
# ==========================


def respond(rules, input):
    """Respond to an input sentence according to the given rules."""

    input = input.split() # match_pattern expects a list of tokens

    # Look through rules and find an input pattern that matches the input.
    for pattern, transforms in rules:
        pattern = pattern.split()
        replacements = match_pattern(pattern, input)
        if replacements:
            break

    # If no match is found, we return `None`.  A possible extension will keep
    # track of user input and respond with "tell me more about ...".
    if not replacements:
        return None

    # When a rule is found, choose one of its output patterns at random.
    output = random.choice(transforms)

    # Replace the variables in the output pattern with the values matched from
    # the input string.
    for variable, replacement in replacements.items():
        replacement = ' '.join(switch_viewpoint(replacement))
        if replacement:
            output = output.replace('?' + variable, replacement)
    
    return output
    

def match_pattern(pattern, input, bindings=None):
    """
    Determine if the input string matches the given pattern.

    Expects pattern and input to be lists of tokens, where each token is a word
    or a variable.

    Returns a dictionary containing the bindings of variables in the input
    pattern to values in the input string, or False when the input doesn't match
    the pattern.
    """

    # Check to see if matching failed before we got here.
    if bindings is False:
        return False
    
    # When the pattern and the input are identical, we have a match, and
    # no more bindings need to be found.
    if pattern == input:
        return bindings

    bindings = bindings or {}

    # Match input and pattern according to their types.
    if is_segment(pattern):
        token = pattern[0] # segment variable is the first token
        var = token[2:] # segment variable is of the form ?*x
        return match_segment(var, pattern[1:], input, bindings)
    elif is_variable(pattern):
        var = pattern[1:] # single variables are of the form ?foo
        return match_variable(var, [input], bindings)
    elif contains_tokens(pattern) and contains_tokens(input):
        # Recurse:
        # try to match the first tokens of both pattern and input.  The bindings
        # that result are used to match the remainder of both lists.
        return match_pattern(pattern[1:],
                             input[1:],
                             match_pattern(pattern[0], input[0], bindings))
    else:
        return False


def match_segment(var, pattern, input, bindings, start=0):
    """
    Match the segment variable against the input.

    pattern and input should be lists of tokens.

    Looks for a substring of input that begins at start and is immediately
    followed by the first word in pattern.  If such a substring exists,
    matching continues recursively and the resulting bindings are returned;
    otherwise returns False.
    """

    # If there are no words in pattern following var, we can just match var
    # to the remainder of the input.
    if not pattern:
        return match_variable(var, input, bindings)

    # Get the segment boundary word and look for the first occurrence in
    # the input starting from index start.
    word = pattern[0]
    try:
        pos = start + input[start:].index(word)
    except ValueError:
        # When the boundary word doesn't appear in the input, no match.
        return False

    # Match the located substring to the segment variable and recursively
    # pattern match using the resulting bindings.
    var_match = match_variable(var, input[:pos], dict(bindings))
    match = match_pattern(pattern, input[pos:], var_match)

    # If pattern matching fails with this substring, try a longer one.
    if not match:
        return match_segment(var, pattern, input, bindings, start + 1)
    
    return match


def match_variable(var, replacement, bindings):
    """Bind the input to the variable and update the bindings."""
    binding = bindings.get(var)
    if not binding:
        # The variable isn't yet bound.
        bindings.update({var: replacement})
        return bindings
    if replacement == bindings[var]:
        # The variable is already bound to that input.
        return bindings

    # The variable is already bound, but not to that input--fail.
    return False


# === Tests for pattern types ===


def contains_tokens(pattern):
    """Test if pattern is a list of subpatterns."""
    return type(pattern) is list and len(pattern) > 0


def is_variable(pattern):
    """Test if pattern is a single variable."""
    return (type(pattern) is str
            and pattern[0] == '?'
            and len(pattern) > 1
            and pattern[1] != '*'
            and pattern[1] in string.letters
            and ' ' not in pattern)


def is_segment(pattern):
    """Test if pattern begins with a segment variable."""
    return (type(pattern) is list
            and pattern
            and len(pattern[0]) > 2
            and pattern[0][0] == '?'
            and pattern[0][1] == '*'
            and pattern[0][2] in string.letters
            and ' ' not in pattern[0])


# Helper functions and setup
# ==========================


def replace(word, replacements):
    """Replace word with rep if (word, rep) occurs in replacements."""
    for old, new in replacements:
        if word == old:
            return new
    return word


def switch_viewpoint(words):
    """Swap some common pronouns for interacting with a robot."""
    replacements = [('I', 'YOU'),
                    ('YOU', 'I'),
                    ('ME', 'YOU'),
                    ('AM', 'ARE'),
                    ('ARE', 'AM')]
    return [replace(word, replacements) for word in words]


def remove_punct(string):
    """Remove common punctuation marks."""
    return (string.replace(',', '')
            .replace('.', '')
            .replace(';', '')
            .replace('!', ''))


USAGE = 'python eliza.py rules.json'


def main(args):
    try:
        file = open(args[0])
    except:
        print 'Must specify rules as a file in JSON format'
        print USAGE
        return

    try:
        rules_dict = json.loads(str(file.read()))
    except:
        print 'Rules must be a file containing JSON'
        print USAGE
        return

    # We need the rules in a list containing elements
    # `(input pattern, [output pattern 1, output pattern 2, ...]`
    rules = []
    for pattern, transforms in rules_dict.items():
        # Remove the punctuation from the pattern to simplify matching.
        pattern = remove_punct(str(pattern.upper())) # kill unicode
        transforms = [str(t).upper() for t in transforms]
        rules.append((pattern, transforms))

    # Read a line, process it, and print the results until no input remains.
    while True:
        try:
            # Remove the punctuation from the input to simplify matching.
            input = remove_punct(raw_input('ELIZA> ').upper())
        except:
            break
        print respond(rules, input)

    file.close()


if __name__ == '__main__':
    main(sys.argv[1:])
