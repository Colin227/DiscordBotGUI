import weather
import joke

'''
This is the message handler

It takes in the user message, the nickname being used and the actual username.

We separate the nickname and the username in order to address each user by their
preferred name, while using the username to hard code values that cannot be retrieved
automatically, such as location.

I used match-case in python to direct each command to the proper function.

'''




def getCommand(msg, usr, usrId):
    match msg:
        case '!goodnight':
            tmpString = f'Goodnight {usr}!'
            return tmpString
            #weatherObj = weather.getWeather(usrId, "forecast")
            #return weatherObj
            # TODO: possibly add weather forecast to goodnight message - removed 
            # right now for simplicity

        case '!goodmorning':
            currentWeather = weather.getWeather(usrId, "current")
            tmpString = 'Good morning ' + str(usr) + "! " + currentWeather
            return tmpString

        case '!joke':
            tmpJoke = joke.get_joke()
            return tmpJoke

        case "!weather":
            weatherObj = weather.getWeather(usrId, "forecast")
            return weatherObj
            
        case _:
            print(msg)
            return "UNKNOWN_COMMAND"