#!/usr/bin/python
import copy


class Originator(object):

    class Memento(object):
        def __init__(self, mstate):
            self.mstate = mstate

        def rollback_state(self):
            return self.mstate

    def set_state(self, state):
        print ('Originator: setup state to: {0}'.format(state))
        self.state = state

    def get_state(self):
        print ('Originator: reading state to: {0}'.format(self.state))

    def save_state(self):
        print ('Originator: saving state')
        return self.Memento(copy.deepcopy(self))

    def rollback_state(self, memento):
        self = memento.rollback_state()
        print ('Originator: rollbac to state: {0}'.format(self.state))


if __name__ == '__main__':
    orig = Originator()
    orig.set_state('State 1')
    orig.get_state()
    orig.set_state('State 2')
    orig.get_state()
    saved_state = orig.save_state()
    orig.set_state('State 3')
    orig.get_state()
    orig.rollback_state(saved_state)
