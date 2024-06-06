class ObservableModel:
    '''The ObservableModel class is a Model object that can register
    an event listener. This will serve as the Parent class of all models
    within the project.'''

    def __init__(self):
        self._event_listeners = {}

    def add_event_listener(self, event, fn):
        '''
        Add an event listener to the ObservableModel.

        Parameters:
        - event (str): The name of the event
        - fn (func): The function to be called when this event is triggered

        Returns:
        - Remove Func (func): Function that can be called to remove the listener
        '''

        # Attempt to append a function to an existing event, otherwise
        # create the event and it's first function.
        try:
            self._event_listeners[event].append(fn)
        except KeyError:
            self._event_listeners[event] = [fn]

        return lambda: self._event_listeners[event].remove(fn)

    def trigger_event(self, event):
        '''
        Trigger the functions tied to a particular event

        Parameters:
        - event (str): The name of the event being triggered

        Returns:
        - None
        '''

        # Return early if the event isn't one previously registered
        # with the object.
        if event not in self._event_listeners.keys():
            return
        
        # Call all functions tied to the event.
        for func in self._event_listeners[event]:
            func(self)