from RecParser import isCorrect
import sys

test_correct = [
    "f :- d; c.",
    "f :- d; (d, d; d, ( d)).",
    "f :- (d; (d))  .",
    "f .",
    "f :- (k ; (c)), d , (f, dsf) .",
    "f :- (((k ; (c)), d) , (f), dsf ).",
    ""


]

test_incorrect = [
    "f :- d; .",
    "f :- d; (d, d d, ( d)).",
    "f :- (d; (d)  .",
    "f :-",
    "f :- (k ; (c), d , (f, dsf) .",
    "f :- .",
    ":- d."
]


if __name__ == "__main__":
    for test in test_correct:
        if not isCorrect(test, False):
            print("Test   '", test, "'   failed")
            sys.exit()
    for test in test_incorrect:
        if isCorrect(test, False):
            print("Test   '", test, "'   failed")
            sys.exit()
    print("Test passed")

