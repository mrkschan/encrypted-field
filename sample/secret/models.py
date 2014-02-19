from django.db import models


KEY = '1' * 32


class EncryptedAttr(object):
    '''Descriptor that encrypt content on write, decrypt on read'''
    def __init__(self, attr, secret_key):
        self.attr = attr
        self.key = secret_key

    def encrypt(self, v):
        '''A simple XOR chiper'''
        return ''.join(chr(ord(a) ^ ord(b)) for (a, b) in zip(self.key, v))

    def decrypt(self, v):
        '''A simple XOR chiper'''
        return ''.join(chr(ord(a) ^ ord(b)) for (a, b) in zip(self.key, v))

    def __get__(self, obj, owner):
        '''Get `attr` from owner, and decrypt it'''
        cipher_text = getattr(obj, self.attr, None)
        if not cipher_text:
            return ''

        return self.decrypt(cipher_text)


    def __set__(self, obj, value):
        '''Encrypt value, and set to owner via `attr`'''
        if not value:
            setattr(obj, self.attr, '')
            return

        cipher_text = self.encrypt(value)
        setattr(obj, self.attr, cipher_text)


class Secret(models.Model):
    _content = models.CharField(max_length=32)

    content = EncryptedAttr('_content', KEY)
