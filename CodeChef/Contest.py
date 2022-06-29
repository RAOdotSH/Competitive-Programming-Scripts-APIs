# Contest class file

class Contest:
    code = ""
    name = ""
    startDate = ""
    startTime = ""
    endTime = ""
    duration = ""

    def makeContest(self):
        return {"code": self.code, "name": self.name, "startDate": self.startDate, "startTime": self.startTime, "endTime": self.endTime, "duration": self.duration}