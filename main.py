import utils

logger = utils.Logger("log.dat")
CLI = utils.CLI(logger)

CLI.graph("S_i1")
CLI.graph("iso_S_w")

while True:
    userInput = input(">>> ")

    command = userInput.split(" ")[0]
    args = userInput.split(" ")[1:]
    
    if userInput == "exit":
        break
    elif command in dir(CLI):
        try:
            getattr(CLI, command)(*args)
        except Exception as e:
            logger.log(str(e), 7)
    else:
        logger.log("User echo : " + userInput)

logger.log("Exiting program.")