
from twisted.trial import unittest
import tidy
import md5

class TidyTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        foo='''<html>
    <h1>woot</h1>
    <hr>
    <img src=\'asdfasdf\'>
    <p>é
<!-- hhmts end -->
  </body>
</html>
'''
        file('foo.htm', 'w').write(foo)
        self.input1="<html><script>1>2</script>"
        self.input2="<html>\n" + "<p>asdkfjhasldkfjhsldjas\n" * 100
    def defaultDocs(self):
        doc1=tidy.parseString(self.input1)
        doc2=tidy.parseString(self.input2)
        doc3=tidy.parse("foo.htm")
        doc4=tidy.parse("bar.htm") # doesn't exist
        return (doc1, doc2, doc3, doc4)
    def test_badOptions(self):
        badopts=[{'foo': 1}, {'indent': '---'}, {'indent_spaces': None}]
        for dct in badopts:
            try:
                tidy.parseString(self.input2, **dct)
            except tidy.TidyLibError:
                pass
            else:
                self.fail("Invalid option %s should have raised an error" %
                          repr(dct))
    def test_errors(self):
        doc1, doc2, doc3, doc4=self.defaultDocs()
        for doc in [doc1, doc2, doc3]:
            str(getattr(doc, 'errors'))
            self.assertEquals(doc1.errors[0].line, 1)
    def test_options(self):
        options = dict(wrap=30)
        print tidy.parseString("<Html>asdlkhf alksfh alsdfh asldkfjh sdlfjh slhfasdf ", **options)
        options = dict(add_xml_decl=1, show_errors=1, newline='CR', 
                       output_xhtml=1)
        doc2 = tidy.parseString("<Html>", **options)
        self.failUnless(str(doc2).startswith('<?xml'))
##        self.failIf(len(doc2.errors)>1) # FIXME - tidylib doesn't
##                                        # support this?
        self.failUnless(str(doc2).find('\n')<0)
        doc3 = tidy.parse('foo.htm', output_encoding='utf8',
                        alt_text='foo')
        self.failUnless(str(doc3).find('\xc3\xa9')>=0)
        self.failUnless(str(doc3).find('alt="foo"')>=0)
    def test_parse(self):
        doc1, doc2, doc3, doc4=self.defaultDocs()
        digest = lambda name: md5.new(str(name)).hexdigest()
        self.assertEqual(digest(doc1), '60534de02e2cf4f66b63ba601d1b74b7')
        self.assertEqual(digest(doc2), 'f3b4f0c2fb5f14ed01b95db3d8289a4d')
        self.assertEqual(digest(doc3), 'f9061475c3d0d08ca8c80fb48aa21655')
    def test_unicode(self):
        ''
        # set options in unicode
        # different output encodings
