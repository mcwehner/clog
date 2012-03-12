import re
import yaml


class Voice(object):
    DEFAULT = 'Tom'
    
    
    @classmethod
    def default(cls):
        return cls(voice=cls.DEFAULT)
    
    
    def __init__(self, user=None, voice=None):
        if voice is None:
            voice = self.DEFAULT
        
        self._voice_map = None
        self.voice      = voice
        
        if user is not None:
            for k, v in self.voice_map.iteritems():
                if re.match(k, user, flags=re.IGNORECASE):
                    self.voice = v
                    break
    
    
    def __str__(self):
        return self.voice
    
    
    @property
    def voice_map(self, path='./voices.yaml'):
        if self._voice_map is None:
            with open(path) as fh:
                self._voice_map = yaml.load(fh)
        
        return self._voice_map
    

