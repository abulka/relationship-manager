import unittest
from src.examples.observer import Observer, Observable


class TestObserver(unittest.TestCase):
    def test_basic_instantiation(self):
        me = Observable()
        spriteview = Observer()
        me.AddObserver(spriteview)
        # assert spriteview in me.observers
        assert spriteview.subject == me

    def test_notifications_work(self):
        class Watcher(Observer):
            state = 0

            def Notify(self, target, notificationEventType):
                Watcher.state += 1

        class Model(Observable):
            def Add(self):
                self.NotifyAll(notificationEventType='')

        me = Model()
        o = Watcher()
        me.AddObserver(o)
        assert Watcher.state == 0
        me.Add()
        assert Watcher.state == 1

        me.Add()
        assert Watcher.state == 2

        me.RemoveObserver(o)

        me.Add()  # should be no notification, thus no change in Watcher state.
        assert Watcher.state == 2

    def test_multiple_observers(self):
        class StateKeeper:
            state = 0

        class Watcher1(Observer):
            def Notify(self, target, notificationEventType):
                StateKeeper.state += 1

        class Watcher2(Observer):
            def Notify(self, target, notificationEventType):
                StateKeeper.state += 10

        class Model(Observable):
            def Add(self):
                self.NotifyAll(notificationEventType='')

        me = Model()
        o1 = Watcher1()
        o2 = Watcher2()
        me.AddObserver(o1)
        me.AddObserver(o2)
        assert StateKeeper.state == 0

        me.Add()
        assert StateKeeper.state == 11  # two notifications in a row did this.

        me.RemoveObserver(o1)
        me.Add()
        assert StateKeeper.state == 21  # one notification did this.


def suite():
    suite1 = unittest.makeSuite(TestObserver, 'test')
    alltests = unittest.TestSuite((suite1,))
    return alltests


def main():
    # default is descriptions=1, verbosity=1
    runner = unittest.TextTestRunner(descriptions=0, verbosity=2)
    runner.run(suite())


if __name__ == '__main__':
    main()
