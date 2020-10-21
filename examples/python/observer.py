"""
Observer Pattern - Relationship Manager based implementation

Each observer can have one subject only in this implementation, but it could be
enhanced very easily. 

A further enhancement might be to allow a different relationship id so that
observers could observer a subject in multiple ways (each way would correspond
to a relationship id). The the notification could be of a certain relationship
id, thus making more granular and efficient notifications.
"""
from relmgr import RelationshipManager


rm = RelationshipManager()


class Observer:
   
    @property
    def subject(self):
        return rm.find_target(self)

    @subject.setter
    def subject(self, _subject):
        rm.add_rel(self, _subject)

    def notify(self, subject, notification_type):
        pass  # implementations override this and do something


class Subject:

    def notify_all(self, notification_type: str):
        observers = rm.find_sources(self)  # all things pointing at me
        for o in observers:
            o.Notify(self, notification_type)

    def add_observer(self, observer):
        rm.add_rel(observer, self)

    def remove_observer(self, observer):
        rm.remove_rel(source=observer, target=self)
