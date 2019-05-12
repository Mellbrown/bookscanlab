class HintSystem:
    def __init__(self):
        self.tag = '[Hint System]:'
        self.mapHint = {}
        self.lstTrigger = []
        self.bufHint = set()

    def clear(self):
        self.mapHint = {}
        self.bufHint = set()

    def registTrigger(self, name, reqHints, trigger):
        print(self.tag, '로드 %s 프로세스' % name)
        self.lstTrigger.append({
            'name': name,
            'reqHints': reqHints,
            'trigger': trigger
        })

    def getHint(self, hintName):
        return self.mapHint[hintName]

    def getHints(self, hintNames):
        return [self.mapHint[name] for name in hintNames]

    def putHint(self, name, hintObj):
        print(self.tag, '힌트 %s 추가' % name)
        self.mapHint[name] = hintObj
        self.bufHint.add(name)

    def putHints(self, mapHints):
        print(self.tag, '힌트 [%s] 추가' % ', '.join(mapHints.keys()))
        self.mapHint.update(mapHints)
        self.bufHint.update(mapHints.keys())

    def commitHint(self):
        mapRun = {}
        for trigger in self.lstTrigger:
            name = trigger['name']
            reqHints = trigger['reqHints']
            trg_proc = trigger['trigger']

            isNeedRun = False
            isSatisfyReq = True
            for hint in reqHints:
                if hint in self.bufHint:
                    isNeedRun = True
                elif hint not in self.mapHint:
                    isSatisfyReq = False

            if isNeedRun and isSatisfyReq:
                mapRun[name] = trg_proc

        print(self.tag, '실행할 프로세스: [%s]' % ', '.join(mapRun.keys()) )
        self.bufHint = set()
        for run in mapRun:
            mapRun[run](self)

    def runSystem(self):
        print(self.tag, '프로세스 시작')
        proc_cnt = 0
        while len(self.bufHint) != 0:
            proc_cnt += 1
            print()
            print(self.tag, '%d회 프로세스, 새 힌트:%s' % (proc_cnt, self.bufHint))
            self.commitHint()
        print(self.tag, '프로세스 종료')