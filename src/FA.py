class FA:
    def __init__(self):
        '''
        - 유한 오토마타의 내용은 아래 5가지 항목이 순서대로 나와야 함.
        - 각 항목은 아래와 같은 StateSet, TerminalSet, DeltaFunctions, StartState, FinalStateSet 의 키워드로 구분되며, 원소를 표현하기 위한 구분자는 {}를 이용
        - 상태는 q로 시작하고 숫자 3자리로 구성됨
        - 터미널 심볼은 a~z, A~Z, 0~9 로 제한 함
        - 입실론 심볼은 ε를 사용
        - 상태전이함수는 아래 예시와 같이 (상태, 터미널) = { 출력상태1, 출력상태2 } 와 같이 구성됨
        - 시작 상태와 종결 상태는 아래와 같이 임의의 상태, 상태 집합으로 정의함

        ex)
        StateSet = { q000, q001, q002 }
        
        TerminalSet = { a, b, c, d }

        DeltaFunctions = {
        (q000, a) = {q000, q001, ...}
        (q000, b) = {q000, q002, ...}
        (q001, a) = {q000, q005, ...}
        (q001, ε) = {q000, q001, ...}
        }

        StartState = q000

        FinalStateSet = { q100, q220 }
        '''
        self.StateSet = []
        self.TerminalSet = []
        self.DeltaFunctions = ""
        self.StartState = []
        self.FinalStateSet = []