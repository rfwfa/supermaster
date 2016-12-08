import unittest
from rfaUtils import buildURL, getHttpResponse, getHttpResponseCode
from time import sleep


class TestRfaUtils(unittest.TestCase):

    def test_buildUrls1(self):
        self.assertEqual(buildURL([""]), "")
    def test_buildUrls2(self):
        self.assertEqual(buildURL(["url"]), "url") 
    def test_buildUrls3(self):
        self.assertEqual(buildURL(["url/"]), "url") 
    def test_buildUrls4(self):
        self.assertEqual(buildURL(["myhost.com", "files/show_all", ""]), "myhost.com/files/show_all") 
    def test_buildUrls5(self):
        self.assertEqual(buildURL(["myhost.com", "files/show_all", "/"]), "myhost.com/files/show_all")
    def test_buildUrls6(self):
        self.assertEqual(buildURL(["myhost.com", "files/show_all"]), "myhost.com/files/show_all") 
    def test_buildUrls7(self):
        self.assertEqual(buildURL(["/myhost.com", "/files/show_all"]), "myhost.com/files/show_all")   
    def test_buildUrls8(self):
        self.assertEqual(buildURL(["/myhost.com/", "/files/show_all/"]), "myhost.com/files/show_all")
    def test_buildUrls9(self):
        self.assertEqual(buildURL(["/myhost.com/", "/files/show_all/", " "]), "myhost.com/files/show_all")
    def test_buildUrls10(self):
        self.assertEqual(buildURL(["/myhost.com/", " /files/show_all/ "]), "myhost.com/files/show_all")
                                           
        
    def test_getHttpResponse1(self):
        response = getHttpResponse('https://echo.getpostman.com/post', 'GET', {'username':'admin1', 'password':'pass'})
        r_code = getHttpResponseCode(response, 'string')
        self.assertEqual(r_code, "404")
        
    def test_getHttpResponse2(self):  
        response = getHttpResponse('https://echo.getpostman.com/post', 'GET', {'username':'admin2', 'password':'pass'})
        r_code = getHttpResponseCode(response, 'int')
        self.assertEqual(r_code, 404)
        
    def test_getHttpResponse3(self):
        resp = getHttpResponse('https://echo.getpostman.com/post', 'POST', {'username':'admin', 'password':'pass'})
        self.assertTrue(resp.content != "", resp)
        
if __name__ == "__main__": unittest.main()

