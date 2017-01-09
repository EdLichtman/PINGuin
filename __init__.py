from flask import Flask
import os, urllib.request

app = Flask(__name__)


def findTargetUrlsListFromFile(filePath, fileName, delimiter):
    linesInFileJoined = delimiter.join(open(filePath + "/" + fileName).readlines())
    return linesInFileJoined.split(delimiter)

def attachPingCode(ping):
    errorMessage = '<div class="pingUrl">' + ping.geturl() + '</div>'
    errorMessage += '<div class="pingStatus">' + str(ping.getcode()) + '</div>'
    return errorMessage

def attachPingError(pingUrl, pingError):
    errorMessage = '<div class="pingUrl">' + pingUrl + '</div>'
    errorMessage += '<div class="pingStatus error">' + pingError + '</div>'
    return errorMessage

targetUrlsFilePath = os.path.dirname(os.path.realpath(__file__))
targetUrlsFileName = "commaDelimitedTargetUrls"
targetUrlsDelimiter = ","

@app.route("/")
def api_root():
    failedPings = ""
    successfulPings = ""
    targetUrlsList = findTargetUrlsListFromFile(targetUrlsFilePath, targetUrlsFileName, targetUrlsDelimiter)
    for targetUrl in targetUrlsList:
        try:
            ping = urllib.request.urlopen(targetUrl)
            successfulPings += attachPingCode(ping)
        except urllib.error.HTTPError as err:
                failedPings += attachPingError(err.url, str(err.code))
    messageToUser = failedPings + successfulPings
    return messageToUser

if __name__ == "__main__":
	app.run()


