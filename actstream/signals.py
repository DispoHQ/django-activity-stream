from django.dispatch import Signal

action = Signal(providing_args=['verb', 'action_object', 'related_action_object',
                                'target', 'description', 'timestamp'])
