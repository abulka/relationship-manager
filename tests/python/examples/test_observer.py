import unittest
from examples.python.observer import Observer, Subject


class TestObserver(unittest.TestCase):
    def test_basic_instantiation(self):
        me = Subject()
        spriteview = Observer()
        me.add_observer(spriteview)
        # assert spriteview in me.observers
        assert spriteview.subject == me

    def test_notifications_work(self):
        class Watcher(Observer):
            state = 0

            def Notify(self, target, notification_type):
                Watcher.state += 1

        class Model(Subject):
            def Add(self):
                self.notify_all(notification_type='')

        me = Model()
        o = Watcher()
        me.add_observer(o)
        self.assertEqual(Watcher.state, 0)
        me.Add()
        self.assertEqual(Watcher.state, 1)

        me.Add()
        self.assertEqual(Watcher.state, 2)

        me.remove_observer(o)

        me.Add()  # should be no notification, thus no change in Watcher state.
        self.assertEqual(Watcher.state, 2)

    def test_multiple_observers(self):
        class StateKeeper:
            state = 0

        class Watcher1(Observer):
            def Notify(self, target, notification_type):
                StateKeeper.state += 1

        class Watcher2(Observer):
            def Notify(self, target, notification_type):
                StateKeeper.state += 10

        class Model(Subject):
            def Add(self):
                self.notify_all(notification_type='')

        me = Model()
        o1 = Watcher1()
        o2 = Watcher2()
        me.add_observer(o1)
        me.add_observer(o2)
        assert StateKeeper.state == 0

        me.Add()
        assert StateKeeper.state == 11  # two notifications in a row did this.

        me.remove_observer(o1)
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
