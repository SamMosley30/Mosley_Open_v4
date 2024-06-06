import unittest
import sys

sys.path.append("/Users/sammo/Mosley_Open_v4")
from models.observable_model import ObservableModel


class TestObservableModel(unittest.TestCase):

    def setUp(self):
        self.model = ObservableModel()
        self.triggered_events = []

    def test_model_initialization(self):
        self.assertDictEqual(self.model._event_listeners, dict())

    def test_add_event_listener(self):

        def example_func():
            pass

        self.model.add_event_listener('test_event', example_func)
        self.assertIn('test_event', self.model._event_listeners)

    def test_add_multiple_funcs(self):
        
        def example_func1():
            pass

        def example_func2():
            pass
        
        # Add the two functions as callbacks to the same event
        self.model.add_event_listener('test_event', example_func1)
        self.model.add_event_listener('test_event', example_func2)

        # Ensure that the number of event listeners is one, and
        # the number of functions tied to that event is two.
        self.assertEquals(len(self.model._event_listeners), 1)
        self.assertEquals(len(self.model._event_listeners['test_event']), 2)

    def test_add_multiple_event_listeners(self):

        def example_func1():
            pass

        def example_func2():
            pass

        # Add two events that use the example functions
        self.model.add_event_listener('test_event1', example_func1)
        self.model.add_event_listener('test_event2', example_func2)

        # Assert that both events were added to the listeners with no additional
        # events seen.
        self.assertIn('test_event1', self.model._event_listeners)
        self.assertIn('test_event2', self.model._event_listeners)
        self.assertEquals(len(self.model._event_listeners), 2)

        # Assert that test_event1 only has one function tied to it, and that it is
        # equivalent to example_func1
        self.assertEquals(len(self.model._event_listeners['test_event1']), 1)
        self.assertEqual(self.model._event_listeners['test_event1'][0], example_func1)

        # Assert that test_event2 only has one function tied to it, and that it is
        # equivalent to example_func2
        self.assertEquals(len(self.model._event_listeners['test_event2']), 1)
        self.assertEqual(self.model._event_listeners['test_event2'][0], example_func2)

    def test_remove_event_listener(self):

        def example_func():
            pass

        # Add event and create output for removing
        remove_event = self.model.add_event_listener('test_event', example_func)
        
        self.assertIn('test_event', self.model._event_listeners)
        self.assertEqual(self.model._event_listeners['test_event'][0], example_func)

        # Call the removal function and check that it was removed
        remove_event()
        self.assertEquals(len(self.model._event_listeners['test_event']), 0)

    def test_trigger_event(self):
        def on_test_event(model):
            self.triggered_events.append('test_event')

        self.model.add_event_listener('test_event', on_test_event)
        self.model.trigger_event('test_event')

        self.assertEqual(self.triggered_events, ['test_event'])

    def test_trigger_event_multiple_functions(self):
        def on_test_event1(model):
            self.triggered_events.append('function1_triggered')
        def on_test_event2(model):
            self.triggered_events.append('function2_triggered')

        self.model.add_event_listener('test_event', on_test_event1)
        self.model.add_event_listener('test_event', on_test_event2)

        self.model.trigger_event('test_event')
        self.assertEqual(self.triggered_events, ['function1_triggered', 'function2_triggered'])

    def test_event_not_registered(self):
        self.model.trigger_event('fake_event')
        self.assertEqual(self.triggered_events, [])


if __name__ == '__main__':
    unittest.main()
