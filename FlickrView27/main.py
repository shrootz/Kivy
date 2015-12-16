'''
Flickr Gallery
=============
This is an upgraded version of the Pictures viewer demo.
Flickr images are downloaded using AsyncImage and manipulated with the Scatter widget.
Sample Flickr Accounts: smithsonian, nasa, briscoe_center
IMPORTANT
=============
To allow virtual keyboard support, run as follows
kivy main.py -c kivy:keyboard_mode:multi
'''


'''
Things I want to do:


'''
import kivy
kivy.require('1.0.6')

from random import randint
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage

# Flickr Support
import urllib2
import xml.etree.ElementTree as ET
from kivy.factory import Factory

# Text Input
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.logger import Logger

# Globals
textbox = TextInput(font_size=35, multiline=False)
api_key = '0428e2668dc1c757439017a27fe73028'
picture_count = 5;

class FlickrPhoto(Scatter):
    source = StringProperty(None)

class PicturesApp(App):

    def build(self):
        self.input_menu()
        
    def input_menu(self):
        ''' create containers for menu gui '''
        main_layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(400,200))     
        button_layout = BoxLayout(orientation='horizontal')
        
        # add transparent background
        with main_layout.canvas.before:
            Color(.5, .5, .5, .2) 
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
            
        # create components
        label = Label(font_size=25, text='Enter Username')
        done_button = Button(font_size=25, text='Done')
        exit_button = Button(font_size=25, text='Exit')
        
        # button events
        done_button.bind(on_release=self.get_flickr_images)
        exit_button.bind(on_release=self.exit_application)
        
        # add components to containers
        main_layout.add_widget(label)
        main_layout.add_widget(textbox)
        button_layout.add_widget(done_button)
        button_layout.add_widget(exit_button)
        main_layout.add_widget(button_layout)
        
        s = Scatter(size_hint=(None, None), size=(450,250), pos=(300, 300), do_rotation=False, do_scale=False)
        s.add_widget(main_layout)
        self.root.add_widget(s)

    def get_flickr_images(self, *args):
        ''' hide keyboard '''
        Window.release_all_keyboards()
        
        ''' get flickr user id from username '''
        user_name = textbox.text
        if len(user_name) > 0:
            print(user_name)
            user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
            #url = 'https://www.flickr.com/services/rest/?method=flickr.urls.lookupUser&format=rest&foo=bar&api_key='+api_key+'&url=http://www.flickr.com/photos/'+user_name
            url = 'https://api.flickr.com/services/rest/?method=flickr.urls.lookupUser&api_key='+api_key+'&url=http://www.flickr.com/photos/'+user_name+'/'
            headers={'User-Agent':user_agent,} 
            request=urllib2.Request(url,None,headers) #The assembled request
            '''Logger.info('THE URL TO TEST: '+request)'''
            #flickr_username_xml = urllib.request.urlopen(request)`
            flickr_username_xml = urllib2.urlopen(request)
            tree = ET.parse(flickr_username_xml)
            tree_root = tree.getroot()
            if tree_root.attrib['stat'] == 'ok':
                user_id = tree_root.find('user').attrib['id']
                print(user_id)
                
                ''' get flickr images with user id '''
                print('https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key='+api_key+'&user_id='+user_id+'&extras=url_o'+'&per_page=500')
                url = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key='+api_key+'&user_id='+user_id+'&extras=url_o'
                request=urllib2.Request(url,None,headers) #The assembled request
                #flickr_images_xml = urllib.request.urlopen(request)
                flickr_images_xml = urllib2.urlopen(request)
                tree = ET.parse(flickr_images_xml)
                photo_total = int(tree.find('photos').attrib.get('total'))
                photo_pages = int(tree.find('photos').attrib.get('pages'))
                photo_perpage = int(tree.find('photos').attrib.get('perpage'))
                photo_list = tree.findall('photos/photo')
                
                if photo_total != 0:
                    # randomize flickr image selections
                    if photo_pages == 1:
                        random_selection = [randint(0,photo_total) for _ in range(picture_count)]
                    elif photo_pages > 1:
                        random_selection = [randint(0,photo_perpage) for _ in range(picture_count)]
                    print(random_selection)
                    count = 0

                    for photo in photo_list:
                        if count in random_selection:
                            try:
                                # parse xml for image url_o
                                url_o = photo.attrib.get('url_o')
                                print(url_o)
                                if str(url_o) != 'None':
                                    # load the photo
                                    
                                    # sc = Scatter(size_hint=(None, None), size=(450,250), pos=(300, 300), do_rotation=True, do_scale=True)
                                    # img = AsyncImage(source= url_o,
                                    #                rotation=randint(-30,30),
                                    #                #pos=(randint(200,5500),randint(200,1800)), 
                                    #                scale_min =0.5,
                                    #                scale_max=15)
                                    #self.root.add_widget(img)
                                    # sc.add_widget(img)
                                    # self.root.add_widget(sc)
                                    
                                    flickr_photo = FlickrPhoto(source = url_o,
                                                               rotation=randint(-30,30))
                                                               #pos=(randint(200,5500),randint(200,1800))) 
                                                               #scale_min =.5,
                                                               #scale_max=15)
                                                               
                                    # add to the main field
                                    self.root.add_widget(flickr_photo)
                                else:
                                    error4 = Popup(title='ERROR!', content=Label(text='Image Missing url_o', font_size=25), size_hint=(None, None), size=(300, 200), pos_hint={'x': .5, 'top': .8})
                                    error4.open()
                                    break
                            except Exception as e:
                                Logger.exception('Pictures: Unable to load <%s>' % url_o)
                        count += 1
                    #self.root.add_widget(sc)
                else:
                    error3 = Popup(title='ERROR!', content=Label(text='No Images Available', font_size=25), size_hint=(None, None), size=(300, 200), pos_hint={'x': .5, 'top': .8})
                    error3.open()
            else:
                error2 = Popup(title='ERROR!', content=Label(text='Invalid User Name', font_size=25), size_hint=(None, None), size=(300, 200), pos_hint={'x': .5, 'top': .8})
                error2.open()
        else:
                error1 = Popup(title='ERROR!', content=Label(text='User Name Required', font_size=25), size_hint=(None, None), size=(300, 200), pos_hint={'x': .5, 'top': .8})
                error1.open()
        
        ''' clear textbox for next user '''
        textbox.text = ''
        
    def exit_application(self, button):
        kivy.app.stopTouchApp()
    
    def on_pause(self):
        return True

if __name__ == '__main__':
    PicturesApp().run()