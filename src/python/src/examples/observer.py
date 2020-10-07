"""
Observer Pattern - RelationshipManager based implementation

Note: this is a but hacky, could be better and use RM more fully.
e.g. Observer doesn't reference RM?
"""
from src.relationship_manager import RelationshipManager


class Observer:
    def __init__(self):
        self.subject = None

    def Notify(self, target, notificationEventType):
        pass


class Observable:
    rm = RelationshipManager()

    def __init__(self):
        #self.observers = []
        #self.rm = RelationshipManager()
        pass

    def NotifyAll(self, notificationEventType):
        observers = self.rm.FindObjects(self, None)
        for o in observers:
            o.Notify(self, notificationEventType)

    def AddObserver(self, observer):
        # self.observers.append(observer)
        self.rm.AddRelationship(self, observer)
        observer.subject = self
        # print 'AddObserver', observer, observer.subject

    def RemoveObserver(self, observer):
        # print 'RemoveObserver', observer, self
        observer.subject = None
        # self.observers.remove(observer)
        self.rm.RemoveRelationships(From=self, To=observer)
