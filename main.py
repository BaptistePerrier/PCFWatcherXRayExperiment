import utils

logger = utils.Logger("log.dat")
CLI = utils.CLI(logger)

while True:
    userInput = input(">>> ")

    command = userInput.split(" ")[0]
    args = userInput.split(" ")[1:]
    
    if userInput == "exit":
        break
    elif userInput == "help" or userInput == "h" or userInput == "-h":
        print("Available commands : ")
        for method in [func for func in dir(CLI) if callable(getattr(CLI, func)) and not func.startswith("__")]:
            print("\t{}".format(method))
    elif command in dir(CLI):
        try:
            getattr(CLI, command)(args)
        except Exception as e:
            logger.log(str(e), 7)
    else:
        logger.log("User echo : " + userInput)

logger.log("Exiting program.")