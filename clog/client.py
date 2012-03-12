import re
import subprocess
import textwrap
import pyfire

from datetime import datetime

from .voice import Voice


class ClientError(Exception):
    pass

class ClientArgumentError(ClientError):
    pass


client_commands = []

def command(f):
    client_commands.append(f.__name__)
    
    return f


class MessageFormatter(object):
    
    def __init__(self, **options):
        self._last_message = None
        self._last_user    = None
        self._options      = options
        self._start_time   = datetime.utcnow()
    
    
    def messages(self, messages):
        for message in messages:
            self.message(message)
    
    
    def message(self, message):
        if message.is_text():
            self.text_message(message)
    
    
    def text_message(self, message):
        message_time = message.created_at.strftime('%X  |  ')
        
        if self._last_user != message.user.name:
            if self._last_user is not None:
                print ''
            
            print message.user.name
            print '-' * len(message.user.name)
        
        lines = textwrap.wrap('%s%s' % (message_time, message.body))
        
        print ('\n%s' % (' ' * len(message_time))).join(lines)
        
        if self._options['text_to_speech'] and message.created_at >= self._start_time:
            self.speak(message)
        
        self._last_message = message
        
        if message.user:
            self._last_user = message.user.name
    
    
    def filtered_message(self, message):
        body = message.body
        
        body = re.sub(r'http://([^\s?#]+)', '\1', body)
        
        return body
    
    
    def speak(self, message):
        # Don't bother with pasted text.
        if not message.is_paste():
            voice        = Voice(user=message.user.name)
            message_body = self.filtered_message(message)
            
            subprocess.call('say -v %s "%s"' % (voice, message_body), shell=True)
    


class Client(object):
    
    @classmethod
    def command_list(cls):
        return client_commands
    
    
    def __init__(self, subdomain, auth_token):
        if subdomain is None or auth_token is None:
            raise ClientError('Missing valid credentials.')
        
        self.subdomain  = subdomain
        self.auth_token = auth_token
        
        self._campfire = None
    
    
    @property
    def campfire(self):
        if self._campfire is None:
            self._campfire = pyfire.Campfire(self.subdomain, self.auth_token, 'X', ssl=True)
        
        return self._campfire
    
    
    def call_command(self, command, *args, **options):
        if command in client_commands:
            command_func = getattr(self, command)
            command_func(*args, **options)
        else:
            raise ClientError("Unknown command '%s'" % command)
    
    
    @command
    def rooms(self, *args, **options):
        rooms       = self.campfire.get_rooms()
        room_names  = [room['name'] for room in rooms]
        display_pad = len(max(room_names, key=len))
        
        for room in rooms:
            if options['verbose']:
                name  = room['name']
                topic = room['topic']
                
                if not topic:
                    topic = '-'
                
                lines = textwrap.wrap(
                    ' %*s  %s' % (display_pad, name, topic)
                )
                
                print ('\n   %s' % (' ' * display_pad)).join(lines)
            else:
                print room['name']
    
    
    @command
    def info(self, *args, **options):
        if args:
            name = args[0]
            room = self.campfire.get_room_by_name(name)
            
            print room.name
            
            if room.topic:
                print '\t%s' % room.topic
            
            print ''
            print 'Users:'
            print '\n'.join(['\t%s' % user['name'] for user in room.get_users()])
        
        else:
            raise ClientArgumentError('Must specify a room name.')
    
    
    @command
    def stream(self, *args, **options):
        if args:
            name = args[0]
            room = self.campfire.get_room_by_name(name)
            
            message_formatter = MessageFormatter(**options)
            
            stream = room.get_stream(live=options['live'])
            
            def _stream_handler(message):
                message_formatter.message(message)
            
            stream.attach(_stream_handler).start()
            
            raw_input('Press ENTER to stop the server.\n\n')
            
            stream.stop().join()
        
        else:
            raise ClientArgumentError('Must specify a room name.')
    
    
    @command
    def recent(self, *args, **options):
        if args:
            room = self.campfire.get_room_by_name(args[0])
            message_formatter = MessageFormatter()
            
            message_formatter.messages(room.recent())
        else:
            raise ClientArgumentError('Must specify a room name.')
    

