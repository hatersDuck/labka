from sources.CheckDocument import CheckDocument

def main():
    test = CheckDocument("./test_document/testFile1Settings.json")
    #test.startAnalize()

    print(test.settings["Path-to-file"])
    print(test.studentInfo)
    print(test.errorsTitle)
    #print(test.biblio)
    print()

    return

if __name__ == "__main__":
    main()