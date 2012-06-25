#!/usr/bin/env python

__author__  = "MetaCarta"
__copyright__ = "Copyright (c) 2006-2008 MetaCarta"
__license__ = "Clear BSD" 
__version__ = "$Id: Flickr.py 468 2008-05-18 06:31:59Z crschmidt $"

from FeatureServer.DataSource import DataSource
from vectorformats.Feature import Feature
import md5
import urllib
import xml.dom.minidom as minidom

FLICKR_API_KEY = "065ba003282b719d84e2a322046c7364"
FLICKR_SECRET = "a192dec51fb99499"

class Flickr (DataSource):
    """Datasource for talking to the flickr API."""
    def __init__(self, name, api_key = None, secret = None, maxpages = 1, maxfeatures = 100, **args):
        DataSource.__init__(self, name, **args)
        global FLICKR_API_KEY, FLICKR_SECRET
        self.attributes = ['user_id','tags','tag_mode','text','min_upload_date','max_upload_date','min_taken_date','max_taken_date','license','sort','privacy_filter','accuracy','machine_tags','machine_tag_mode','group_id','per_page']
        self.queryable   = ','.join(self.attributes)
        self.api_key     = api_key or FLICKR_API_KEY
        self.secret      = secret  or FLICKR_SECRET
        self.maxpages    = maxpages
        self.maxfeatures = maxfeatures
        self.api         = API(self.api_key, self.secret)
        
    def select (self, action):
        """Use the flickr.photos.search method to find photos based on bbox/attributes, 
           or the flickr.photos.getInfo method if given an ID.""" 
        features = [] 
        if action.id is not None:
            data = self.api.request({'method':'flickr.photos.getInfo','photo_id':action.id})
            doc = minidom.parseString(data)
            photo = doc.getElementsByTagName("photo")[0]
            features.append(self.convert_single_photo_xml_to_feature(photo))
            
        else:
            page = 1 
            pages = self.maxpages
            max = action.maxfeatures or self.maxfeatures
            while page <= pages and len(features) < max:
                params = {'method':'flickr.photos.search', 'extras':'geo,tags,license', 'page': page, 'per_page': max  }
                if hasattr(self, 'auth_token'):
                    params['auth_token'] = self.auth_token
                for attr in self.attributes:
                    if hasattr(self, attr):
                        params[attr] = getattr(self, attr) 
                    elif action.attributes.has_key(attr):
                        params[attr] = action.attributes[attr]
                if action.bbox:
                    if action.bbox[0] < -180:
                        action.bbox[0] = -180
                    if action.bbox[1] < -90:
                        action.bbox[1] = -90
                    if action.bbox[2] > 180:
                        action.bbox[2] = 180
                    if action.bbox[3] > 90:
                        action.bbox[3] = 90
                    params['bbox'] = ','.join(map(str,action.bbox))
                data = self.api.request(params)
                doc = minidom.parseString(data)
                
                # Determine the number of pages we should iterate through
                photos_elem = doc.getElementsByTagName("photos")[0]
                pages_from_xml = int(photos_elem.attributes['pages'].value)
                if pages_from_xml < pages:
                    pages = pages_from_xml
                
                photos = doc.getElementsByTagName("photo")
                for photo in photos:
                    if len(features) == max: continue
                    feature = self.convert_photo_xml_to_feature(photo)
                    features.append(feature)
                page += 1        
        return features    

    def convert_single_photo_xml_to_feature(self, xml):
        """Convert the Flickr Photo XML to a Feature object. XML arg is
           an xml.dom.minidom object. this reads the response from the getInfo
           method.""" 
        attrs = xml.attributes.items() 
        props = {}
        for attr in attrs:
            props[attr[0]] = attr[1]
        
        props['owner'] = xml.getElementsByTagName("owner")[0].attributes['nsid'].value
        for i in ['title', 'description']:
            node = xml.getElementsByTagName(i)[0]
            if node.firstChild:
                props[i] = node.firstChild.nodeValue
        
        loc = xml.getElementsByTagName("location")[0]
        coordinates = [float(loc.attributes['longitude'].value), float(loc.attributes['latitude'].value)]
        return Feature(id=xml.getAttribute("id"), geometry={'type':"Point", 'coordinates':coordinates}, srs=self.srid_out, props=props)
        
    def convert_photo_xml_to_feature(self, xml):
        """Convert the Flickr Photo XML to a Feature object. XML arg is an
        xml.dom.minidom object. This reads a photo which is part of a list of
        photos returned by the search method.""" 
        attrs = xml.attributes.items() 
        props = {}
        for attr in attrs:
            props[attr[0]] = attr[1]
        coordinates = [float(props['longitude']), float(props['latitude'])]
        props['img_url'] = "http://farm%s.static.flickr.com/%s/%s_%s_m.jpg" % (props['farm'], props['server'], props['id'], props['secret'])
        del props['latitude']
        del props['longitude']
        return Feature(id=xml.getAttribute("id"), geometry={'type':"Point", 'coordinates':coordinates}, srs=self.srid_out, props=props)

class API:
    """Utility class for talking to Flickr API. This is a very lightweight
       utility for this purpose, to save us from having to cart around another
       library."""
    def __init__(self, api_key = "065ba003282b719d84e2a322046c7364", secret = "a192dec51fb99499", url_base = "http://api.flickr.com/services/rest/"):
        self.api_key = api_key
        self.secret = secret
        self.base = url_base
    
    def params_sig(self, params):
        items = []
        keys = params.keys()
        keys.sort()
        for key in keys: 
            items.append("%s%s" % (key,params[key]))
        sign_string = "%s%s" % (self.secret, "".join(items))
        return md5.md5(sign_string).hexdigest()
    
    def request(self, params):
        params['api_key'] = self.api_key
        sig = self.params_sig(params)
        params['api_sig'] = sig
        return urllib.urlopen(self.base, urllib.urlencode(params)).read()
    
    def fetch_frob(self):
        data = self.request({'method':'flickr.auth.getFrob'})
        doc = minidom.parseString(data)
        self.frob = doc.getElementsByTagName("frob")[0].firstChild.nodeValue
        return self.frob
    
    def get_link(self):
        self.fetch_frob()
        sig = self.params_sig({'api_key':self.api_key, 'perms':'read', 'frob': self.frob})
        return "http://flickr.com/services/auth/?api_key=%s&perms=read&frob=%s&api_sig=%s" % ( self.api_key, self.frob, sig )
    
    def get_token(self):
        params = {
          'method':'flickr.auth.getToken',
          'frob':self.frob
        }
        doc = minidom.parseString( self.request(params) )
        return doc.getElementsByTagName("token")[0].firstChild.nodeValue
        
    

if __name__ == "__main__":
    a = API()
    print "Open the following URL in a browser:" 
    print a.get_link()
    print "Press enter when complete."
    raw_input()
    token = a.get_token()
    print "Your auth token is:\n\n    %s\n\nAdd the following line to a Flickr data source to complete configuration:\n\nauth_token=%s  " % (token,token)
