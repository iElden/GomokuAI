#!/usr/bin/env python3
import asyncio
from sys import argv
from Manager.UnitTest import UnitTest

TESTS = {
    "Basic Attack Jeremy": UnitTest(
        "START 20\nBOARD\n5,5,2\n5,6,2\n5,7,2\n5,8,2\n5,9,1\n9,5,1\n9,6,1\n9,7,1\n9,8,1\n9,9,2\nDONE",
        stdout="OK\n9,4", return_code=0),

    "Basic Defense middle 1": UnitTest(
        "START 5\nBOARD\n2,0,2\n2,1,2\n2,3,2\n2,4,2\nDONE",
        stdout="OK\n2,2", return_code=0),

    "Basic Defense middle 2": UnitTest(
        "START 5\nBOARD\n0,2,2\n1,2,2\n3,2,2\n4,2,2\nDONE",
        stdout="OK\n2,2", return_code=0),

    "Basic Defense Detect Side 1": UnitTest(
        "START 5\nBOARD\n0,1,2\n0,2,2\n0,3,2\n0,4,2\nDONE",
        stdout="OK\n0,0", return_code=0),

    "Basic Defense Detect Side 2": UnitTest(
        "START 5\nBOARD\n1,0,2\n2,0,2\n3,0,2\n4,0,2\nDONE",
        stdout="OK\n0,0", return_code=0),

    "Basic Defense Detect Side 3": UnitTest(
        "START 5\nBOARD\n1,1,2\n2,2,2\n3,3,2\n4,4,2\nDONE",
        stdout="OK\n0,0", return_code=0),

    "Basic Defense Detect Side 4": UnitTest(
        "START 5\nBOARD\n0,0,2\n1,1,2\n2,2,2\n3,3,2\nDONE",
        stdout="OK\n4,4", return_code=0),

    "Basic Defense Detect Side 5": UnitTest(
        "START 5\nBOARD\n4,3,2\n4,2,2\n4,1,2\n4,0,2\nDONE",
        stdout="OK\n4,4", return_code=0),

    "Basic Defense Detect Side 6": UnitTest(
        "START 5\nBOARD\n3,4,2\n2,4,2\n1,4,2\n0,4,2\nDONE",
        stdout="OK\n4,4", return_code=0),

    "Basic Defense Detect Side 7": UnitTest(
        "START 5\nBOARD\n0,0,2\n0,1,2\n0,2,2\n0,3,2\nDONE",
        stdout="OK\n0,4", return_code=0),

    "Basic Defense Detect Side 8": UnitTest(
        "START 5\nBOARD\n1,4,2\n2,4,2\n3,4,2\n4,4,2\nDONE",
        stdout="OK\n0,4", return_code=0),

    "Basic Defense Detect Side 9": UnitTest(
        "START 5\nBOARD\n0,0,2\n1,0,2\n2,0,2\n3,0,2\nDONE",
        stdout="OK\n4,0", return_code=0),

    "Basic Defense Detect Side 10": UnitTest(
        "START 5\nBOARD\n4,1,2\n4,2,2\n4,3,2\n4,4,2\nDONE",
        stdout="OK\n4,0", return_code=0),

    "Error Management: random input": UnitTest(
        "oisguoiapdsfjsqufhdsfqsdp,fpunpqsfd",
        return_code=0),

    "Error Management: bad start size (< 5)": UnitTest(
        "START 4",
        return_code=0),

    "Error Management: bad start size (< 0)": UnitTest(
        "START -1",
        return_code=0),

    "Error Management: BOARD: Out of range 1": UnitTest(
        "START 20\nBOARD\n20,5,1\nDONE",
        return_code=0),

    "Error Management: BOARD: Out of range 2": UnitTest(
        "START 20\nBOARD\n-1,5,1\nDONE",
        return_code=0),

    "Error Management: BOARD: Invalid player number 1": UnitTest(
        "START 20\nBOARD\n5,5,0\nDONE",
        return_code=0),

    "Error Management: BOARD: Invalid player number 2": UnitTest(
        "START 20\nBOARD\n5,5,3\nDONE",
        return_code=0),

    "Error Management: Invalid input during board": UnitTest(
        "START 20\nBOARD\n0,0,1\nhello ^-^\n0,1,1\n\n\nhow are you ?\n0,2,1\n\n0,3,1\n\n\n\t\nwhy you don't answer :(\nDONE",
        return_code=0),

    "Advanced Defense (counter possible 3-3)": UnitTest(
        "START 20\nBOARD\n4,5,2\n5,4,2\n5,6,2\n6,5,2\nDONE",
        stdout="OK\n5,5", return_code=0),

    "Advanced Attack (play a 3-3 borderless insead of just 3 borderless) 1": UnitTest(
        "START 20\nBOARD\n10,9,1\n9,10,1\n8,9,1\n9,8,1\n0,0,1\n0,1,1\nDONE",
        stdout="OK\n9,9", return_code=0),

    "Advanced Attack (play a 3-3 borderless insead of just 3 borderless) 2": UnitTest(
        "START 20\nBOARD\n4,5,1\n5,4,1\n5,6,1\n5,6,1\n19,19,1\n19,18,1\nDONE",
        stdout="OK\n5,5", return_code=0),

    "Advanced Defense (pattern: -X---O-XXX---)": UnitTest(
        "START 20\nBOARD\n1,5,2\n5,5,1\n7,5,2\n8,5,2\n9,5,2\nDONE",
        stdout="OK\n10,5", return_code=0),

    "Advanced Attack (Complete a 4-borderless insead of blocking a potential 4-with-border enemy)": UnitTest(
        "START 20\nBOARD\n1,5,2\n5,5,1\n5,4,1\n5,6,1\n7,5,2\n8,5,2\n9,5,2\n5,8,2\nDONE",
        stdout="OK\n5,3", return_code=0),
}

if __name__ == '__main__':
    program_path = './pbrain-gomoku-ai' if len(argv) < 2 else argv[1]
    loop = asyncio.get_event_loop()
    for name, test in TESTS.items():
        print(name,':', loop.run_until_complete(test.run(program_path)))