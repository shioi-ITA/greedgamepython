# -*- coding: utf-8 -*-
class Observer:
    '''
    Observer or Listener
    '''
    def __init__(self):
        pass
    
    def register(self, subject):
        subject.register(self)
        
    def update(self, event):
        pass

class Subject:
    '''
    Subject
    '''
    def __init__(self):
        self.observers = []

    def register(self, observer):
        self.observers.append(observer)
 
    def unregister(self, observer):
        self.observers.remove(observer)
 
    def notify_listeners(self, event):
        for observer in self.observers:
            observer.update(event)