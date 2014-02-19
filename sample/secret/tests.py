from django.test import TestCase
from secret.models import Secret, KEY


class SimpleTest(TestCase):
    def test_encrypt(self):
        v = '1' * 32
        c = ''.join(chr(ord(a) ^ ord(b)) for (a, b) in zip(KEY, v))

        s = Secret()
        s.content = v
        self.assertEqual(s._content, c)

        print
        print 'DEBUG encrypt: c', ''.join('%02x' % ord(i) for i in c)
        print 'DEBUG encrypt: s._content', ''.join('%02x' % ord(i) for i in s._content)

    def test_decrypt(self):
        v = '1' * 32
        c = ''.join(chr(ord(a) ^ ord(b)) for (a, b) in zip(KEY, v))

        s = Secret(_content=c)
        self.assertEqual(s.content, v)

        print
        print 'DEBUG decrypt: v', v
        print 'DEBUG decrypt: s.content', s.content
