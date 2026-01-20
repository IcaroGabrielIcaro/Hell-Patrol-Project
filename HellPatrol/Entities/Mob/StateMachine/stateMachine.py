from Entities.Mob.StateMachine.States.state import State

class StateMachine:

    def __init__(self, states):
        self.states={}
        for state in states:
            self.states[state.stateName]=state
        self.currentState=states[0]

    def switchTo(self,name):
        self.currentState.quit()
        self.currentState=self.states[name]
        self.currentState.start()

