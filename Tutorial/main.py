from kivy.app import App

from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle


class TutorialApp(App):
    def build(self):
        name1 = 'Name1'
        lastname1 = 'Last1'
        name2 = 'Name2'
        name3 = 'Name3'
        name4 = 'Name4'
        name5 = 'Name5'
        f = FloatLayout()
        
        button_layout = BoxLayout(pos_hint={'x': 0, 'center_y': .5}, size_hint=(1, 1), orientation='vertical')
        
        with button_layout.canvas.before:
            Color(.5, .5, .5, .2) 
            self.rect = Rectangle(size=button_layout.size, pos=button_layout.pos)
            
        name1_button = Button(font_size=25, text=name1+lastname1, size=(150,150))
        name2_button = Button(font_size=25, text=name2, size=(150,150))
        name3_button = Button(font_size=25, text=name3, size=(150,150))
        name4_button = Button(font_size=25, text=name4, size=(150,150))
        name5_button = Button(font_size=25, text=name5, size=(150,150))
        
        #name1_button.bind(on_release=self.get_flickr_images(name1))
        name2_button.bind(on_release=self.on_touch_down)
        
        button_layout.add_widget(name1_button)
        button_layout.add_widget(name2_button)
        button_layout.add_widget(name3_button)
        button_layout.add_widget(name4_button)
        button_layout.add_widget(name5_button)
        
        #s = Scatter(size_hint=(None, None), size=(450,250), pos=(300, 300), do_rotation=False, do_scale=False)
        #s.add_widget(button_layout)
        #f.add_widget(s)
        f.add_widget(button_layout)
        return f
    
        #self.root.add_widget(button_layout)
        #f = FloatLayout()
        #s = Scatter()
        #l = Label(text="Hello!",
        #         font_size=150)
        #f.add_widget(s)
        #s.add_widget(l)
        #return f
        
        
    def get_flickr_images(self, *args):
        print args
        
    def exit_application(self, button):
        kivy.app.stopTouchApp()
        
    def on_touch_down(self, touch):
        #if touch.is_double_tap:
        x = Label(text = "HI!",
              font_size=150)
        s = Scatter(size_hint=(None, None), size=(150,150), pos=(300, 300), do_rotation=False, do_scale=False)
        s.add_widget(x)
        self.root.add_widget(s)
        return s
            
if __name__ == "__main__":
    TutorialApp().run()