from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage


class CarouselApp(App):
    def build(self):
        carousel = Carousel(direction='right')
        for i in range(10):
            src = "http://placehold.it/480x270.png&text=slide-%d&.png" % i
            image = AsyncImage(source=src, allow_stretch=True)
            carousel.add_widget(image)
        return carousel


CarouselApp().run()