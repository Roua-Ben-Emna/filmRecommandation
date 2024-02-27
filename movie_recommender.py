from kivymd.app import MDApp
from kivy.uix.image import Image
from kivymd.uix.button import MDIconButton
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from experta import *
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
import os
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.graphics.stencil_instructions import StencilPush, StencilUse, StencilPop, StencilUnUse


class BackgroundLayout(MDBoxLayout):
    def __init__(self, image_source, **kwargs):
        super(BackgroundLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        with self.canvas.before:
            self.bg = Image(source=image_source, allow_stretch=True, keep_ratio=False)
            self.bind(size=self._update_bg_size, pos=self._update_bg_pos)
            
    def _update_bg_size(self, instance, value):
        self.bg.size = value

    def _update_bg_pos(self, instance, value):
        self.bg.pos = value

class CustomChoiceButton(ButtonBehavior, Label):
    def __init__(self, **kwargs):
        super(CustomChoiceButton, self).__init__(
            size_hint=(None, None),
            height=dp(40),
            width=dp(150),
            **kwargs
        )
        with self.canvas.before:
            Color(215/255, 71/255, 71/255, 0.9),  
            self.bg = RoundedRectangle(size=self.size, pos=self.pos, radius=[12,])

        self.bind(pos=self._update_bg_pos, size=self._update_bg_size)

    def _update_bg_size(self, instance, value):
        self.bg.size = value

    def _update_bg_pos(self, instance, value):
        self.bg.pos = value

class Film(Fact):
    """Information sur le film"""
    pass

class InterferenceEngine(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.recommended_movies = []
        self.responses = {}

    def clear_recommended_movies(self):
        self.recommended_movies = []
        
    def clear_responses(self):
        self.responses = {}
    def retract(self, fact):
        if fact in self.facts:
            self.facts.remove(fact)

    @Rule(
        OR(
            AND(
                Film(Avec_des_amis=True),
                Film(peur=True),
                Film(appreciez_musique=True)
            ),
            AND(
                Film(Avec_des_amis=True),
                Film(peur=True),
                Film(appreciez_musique=True),
                Film(interet_personnalites_reelles=True),
                Film(age_lte_12=True)
            )
        ),
        salience=3  
    )
    def musical(self):
        recommended_movie = "La La Land"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="Musical", recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)
            print("La La Land recommended")

    @Rule(AND(
        Film(Avec_des_amis=True),
        Film(peur=True),
        Film(appreciez_musique=True),
        NOT(Film(age_lte_12=True)),
        Film(interet_personnalites_reelles=True),
    ),
    salience=3
    )
    def bohemian_rhapsody(self):
        recommended_movie = "Bohemian Rhapsody"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="Musical", recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)
            print("Bohemian Rhapsody recommended")

    @Rule(
        Film(Avec_des_amis=True),
        Film(peur=True),
        Film(appreciez_musique=True),
        Film(age_lte_12=True),
        NOT(Film(interet_personnalites_reelles=True)),
        salience=3  
    )
    def greatest_showman(self):
        recommended_movie = "The Greatest Showman"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="Musical", recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)
            print("The Greatest Showman recommended")
    @Rule(
        OR(
            AND(
                NOT(Film(peur=True)),
                Film(voyages_et_les_aventures=True),
                Film(vivre_sur_une_ile_deserte=True),
            ),
            AND(
                NOT(Film(peur=True)),
                Film(voyages_et_les_aventures=True),
            )
        ),
        salience=2 
    )
    def aventure(self):
        self.declare(Film(genre="Aventure"))

    @Rule(
        AND(
            Film(genre="Aventure"),
            Film(lire_le_roman=True)
        ),
        salience=1 
    )
    def Hunger(self):
        recommended_movie = "The Hunger Games"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="Aventure",recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)
    @Rule(
        AND(
            Film(genre="Aventure"),
            Film(une_duree_journee=True)
        ),
        salience=1
    )
    def king(self):
        recommended_movie = "King Kong"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="Aventure",recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)
            
    @Rule(
        AND(
            Film(genre="Aventure"),
            OR(Film(age_lte_12=True), Film(age_ge_13=True), Film(age_lt_18=True))
        ),
        salience=1 
    )
    def Jumanji(self):
        recommended_movie = "Jumanji welcome to the jungle"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="Aventure",recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)       
    @Rule(
        AND(
            Film(genre="Aventure"),
            Film(appreciez_histoires_stimulent_imagination=True),
            Film(voyager_dans_futur=True),
        ),
        salience=6
    )
    def science_fiction(self):
        self.declare(Film(genre="Science Fiction"))               
    @Rule(
        AND(
            Film(genre="Science Fiction"),
            Film(genre="Aventure")
        ),
        salience=5 
    )
    def interstellar(self):
        recommended_movie = "Interstellar"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)       
            
    @Rule(
        AND(
            Film(genre="Aventure"),
            Film(genre="Science Fiction"),
            Film(lire_le_roman=True),
        ),
        salience=5
    )
    def divergent(self):
        recommended_movie = "Divergent"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="Science Fiction",recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)  
    @Rule(
        AND(
            Film(genre="Science Fiction"),
            Film(emotion=True),
        ),
        salience=5
    )
    def Inception(self):
        recommended_movie = "Inception"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="Science Fiction",recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)
    @Rule(
            AND(
                Film(genre="Aventure"),
                Film(appreciez_histoires_stimulent_imagination=True),
                Film(movie_night_desire=True),
            ),
            salience=6
        )
    def fantastique(self):
        recommended_movie = "Troll"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="Fantastique", recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie) 
    @Rule(
        AND(
            Film(Avec_des_amis=False),
            NOT(Film(peur=True)),
            Film(reaction=True),
        )
    )
    def war(self):
        self.declare(Film(genre="War"))   
       
    @Rule(
        AND(
            Film(genre="War"),
            OR(
                Film(une_duree_journee=True),
                AND(
                    Film(age_ge_13=True),
                    Film(age_lt_18=True),
                )
            )
        )
    )
    def jojo_recommendation(self):
        recommended_movie = "Jojo Rabbit"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="War",recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)
    @Rule(
        AND(
            Film(genre="War"),
            Film(emotion_sport=True)
        ) 
    )
    def recommend_1917(self):
        recommended_movie = "1917"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="War",recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)    
    @Rule(
        AND(
            OR(
                Film(Avec_des_amis=True),
                Film(En_solo=True)
            ),
            OR(
                Film(voyager_dans_passe=True),
                Film(personne_guerre=True)
            )
        ),
        salience=9 
    )
    def history(self):
           self.declare(Film(genre="Histoire"))    
    @Rule(
        AND(
            Film(genre="War"),
            Film(genre="Histoire"),
            Film(lire_le_roman=True),
        ),
        salience=8 
    )
    def imitationgame(self):
        recommended_movie = "The imitation game"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)   
    @Rule(
        AND(
            Film(genre="Histoire"),
            Film(emotion_pleur=True),
        ),
        salience=8
    )
    def togo(self):
        recommended_movie = "Togo"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="Histoire",recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)
    @Rule(
        AND(
            Film(En_famille=True),
            Film(animated_story_interest=True),
        )
    )
    def animation(self):
        self.declare(Film(genre="Animation"))     

    @Rule(
        AND(
            Film(genre="Animation"),
            Film(emotion_rire=True),
        )
    )
    def boss_baby(self):
        recommended_movie = "Boss Baby"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="Animation",recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)          
    @Rule(
        AND(
            Film(genre="Animation"),
            Film(age_lte_12=True),
        )
    )
    def thegrinch(self):
        recommended_movie = "The Grinch"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="Animation",recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)  
    @Rule(
        AND(
            Film(genre="Animation"),
            Film(age_lte_12=True),
        )
    )
    def toystory(self):
        recommended_movie = "Toy Story"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="Animation",recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)                           
    @Rule(
        AND(
            Film(Avec_mon_partenaire=True),
            OR(Film(hobby_lec=True),
               Film(peur=True),)
            
        )
    )
    def Romantique(self):
        self.declare(Film(genre="Romantique"))              
    
    @Rule(
        AND(
            Film(genre="Romantique"),
            Film(lire_le_roman=True),
           
        )
    )
    def twilight(self):
        recommended_movie = "Twilight"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="Romantique",recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie) 
    @Rule(
        AND(
            Film(genre="Romantique"),
            Film(age_lt_18=True),  
        )
    )        
    def fifty_shades_of_gray(self):
        recommended_movie = "Fifty Shades Of Gray"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="Romantique",recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)  
    
    @Rule(
        AND(
            Film(genre="Romantique"),
            Film(emotion_pleur=True),
           
        )
    )
    def a_walk_to_remember(self):
        recommended_movie = "A walk to remember"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="Romantique",recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)       
    @Rule(
        AND(
            Film(En_famille=True),
            Film(facts_fascinants= True)       
        )
    )
    def documentary(self):
        self.declare(Film(genre="Documentary"))        
    @Rule(
        AND(
            Film(genre="Documentary"),
            Film(reaction=True),
        )
    )
    def World_War(self):
        recommended_movie = "The World at War"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="Documentary",recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)  

    @Rule(
        AND(
            Film(genre="Documentary"),
            Film(emotion_pleur=True),    
        )
    )
    def yallagaza(self):
        recommended_movie = "Yalla Gaza"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="Documentary",recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)  
    @Rule(
        AND(
            Film(genre="Documentary"),
            Film(interet_personnalites_reelles=True),   
        )
    )
    def chute(self):
        recommended_movie = "La Chute"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="Documentary",recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)  
    @Rule(
        AND(
            OR(Film(En_solo=True), Film(Avec_des_amis=True)),
            Film(interet_personnalites_reelles=True)
        ),
    )
    def biography(self):
        recommended_movie = "Blonde"    
        if recommended_movie not in self.recommended_movies:    
            self.declare(Film(genre="Biography", recommended_movie=recommended_movie)) 
            self.recommended_movies.append(recommended_movie)
    @Rule(
        AND(
            Film(genre="Documentary"),
            Film(genre="Biography"),  
        )
    )
    def Oppenheimer(self):
        recommended_movie = "Oppenheimer"
        if recommended_movie not in self.recommended_movies:
            self.declare(Film(genre="Biography",recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie) 
    @Rule(
    OR(
        AND(
            Film(Avec_des_amis=True),
            NOT(Film(peur=True)),
            OR(Film(une_duree_journee=True), Film(emotion_sport=True))
        ),
        AND(
            Film(Avec_mon_partenaire=True),
            NOT(Film(peur=True)),
            OR(Film(une_duree_journee=True), Film(emotion_sport=True))
        )
    ),
)
    def action(self):
        recommended_movie = "Mission impossible" 
        if recommended_movie not in self.recommended_movies:    
            self.declare(Film(genre="Action",recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)  
    @Rule(
        AND(
            Film(genre="Aventure"),
            Film(genre="Action"),   
        )
    )
    def fastandfurious(self):
        recommended_movie = "Fast and Furious"
        if recommended_movie not in self.recommended_movies:    
            self.declare(Film(recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie)            
    @Rule(
        AND(
            Film(genre="Romantique"),
            Film(genre="Action"),     
        )
    )
    def smith(self):
        recommended_movie = "Ms and Mr Smith"
        if recommended_movie not in self.recommended_movies:    
            self.declare(Film(recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie) 
    @Rule(
        AND(
            Film(combat_explosions=True),
            Film(genre="Action"),
        )
    )
    def extraction(self):
        recommended_movie = "Extraction"
        if recommended_movie not in self.recommended_movies:    
            self.declare(Film(recommended_movie=recommended_movie))
            self.recommended_movies.append(recommended_movie) 
           
class QuestionScreen(Screen):
    def __init__(self, question_data, key, engine, **kwargs):
        super(QuestionScreen, self).__init__(**kwargs)
        self.question_data = question_data
        self.key = key  
        self.response_key = f"{key}_response"
        self.engine = engine
        self.create_question_layout()

    
    def create_question_layout(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_dir, 'movie.jpeg')
        background_layout = BackgroundLayout(image_source=image_path)
        self.add_widget(background_layout)

        layout = BoxLayout(orientation='vertical', spacing=5, padding=5, size_hint=(None, None))
        layout.width = self.width 
        question_label = MDLabel(text=self.question_data["question"], font_style='Subtitle1', size_hint_y=None, size_hint_x=3)  
        layout.add_widget(question_label)
        remaining_space = 1 - layout.height / self.height
        layout.add_widget(Widget(size_hint_y=remaining_space))
        buttons_layout = BoxLayout(orientation='vertical', spacing=5, padding=5, size_hint_y=None)

        for choice in self.question_data["choices"]:
            button = CustomChoiceButton(size_hint_x=None,text=choice, on_release=lambda instance, choice=choice: self.on_choice_selected(instance, choice), size_hint_y=None)
            buttons_layout.add_widget(button)

        layout.add_widget(buttons_layout)
        button_width = dp(200)
        buttons_layout.width = button_width

        buttons_layout.height = sum(child.height for child in buttons_layout.children)
        buttons_layout.pos_hint = {'center_x': -0.2,'center_y': 0.5}

        layout.height = sum(child.height for child in layout.children)
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        question_label.pos_hint = {'center_x': 0.5}  
        self.add_widget(layout)

    def on_choice_selected(self, instance, choice):
        self.engine.responses[self.key] = choice
        self.engine.reset()

        for key, value in self.engine.responses.items():
            setattr(self.engine, f"{key}_response", value)            

        print("User Responses:", self.engine.responses)
      
        self.engine.declare(Film(
            Avec_des_amis=self.engine.question_0_response.lower() == 'amis',
            En_solo=self.engine.question_0_response.lower() == 'solo',
            En_famille=self.engine.question_0_response.lower() == 'famille',
            Avec_mon_partenaire=self.engine.question_0_response.lower() == 'partenaire',
            peur=self.engine.question_1_response.lower() == 'oui' if 'question_1' in self.engine.responses else False,
            appreciez_musique=self.engine.question_2_response.lower() == 'oui' if 'question_2' in self.engine.responses else False,
            interet_personnalites_reelles=self.engine.question_3_response.lower() == 'oui' if 'question_3' in self.engine.responses else False,
            age_lte_12=self.engine.question_4_response.lower() == '12 ans et moins' if 'question_4' in self.engine.responses else False,
            age_ge_13=self.engine.question_4_response.lower() == 'entre 13 et 18 ans' if 'question_4' in self.engine.responses else False,
            age_lt_18=self.engine.question_4_response.lower() == 'plus que 18' if 'question_4' in self.engine.responses else False,
            voyages_et_les_aventures=self.engine.question_5_response.lower() == 'oui' if 'question_5' in self.engine.responses else False,
            vivre_sur_une_ile_deserte=self.engine.question_6_response.lower() == 'oui' if 'question_6' in self.engine.responses else False,
            lire_le_roman=self.engine.question_7_response.lower() == 'oui' if 'question_7' in self.engine.responses else False,          
            une_duree_journee=self.engine.question_8_response.lower() == 'oui' if 'question_8' in self.engine.responses else False,          
            appreciez_histoires_stimulent_imagination=self.engine.question_9_response.lower() == 'oui' if 'question_9' in self.engine.responses else False,   
            voyager_dans_futur=self.engine.question_10_response.lower() == 'futur'  if 'question_10' in self.engine.responses else False,
            voyager_dans_passe=self.engine.question_10_response.lower() == 'passé'  if 'question_10' in self.engine.responses else False,
            emotion_pleur=self.engine.question_11_response.lower() == 'pleurer' if 'question_11' in self.engine.responses else False,
            emotion=self.engine.question_11_response.lower() == 'réfléchir profondément' if 'question_11' in self.engine.responses else False,
            emotion_sport=self.engine.question_11_response.lower() == 'être captivé par action' if 'question_11' in self.engine.responses else False,
            emotion_rire=self.engine.question_11_response.lower() == 'rire' if 'question_11' in self.engine.responses else False,
            reaction=self.engine.question_12_response.lower() == 'oui' if 'question_12' in self.engine.responses else False,
            personne_guerre=self.engine.question_13_response.lower() == 'personnalités de guerre' if 'question_13' in self.engine.responses else False,
            movie_night_desire=self.engine.question_14_response.lower() == 'oui' if 'question_14' in self.engine.responses else False,
            animated_story_interest=self.engine.question_15_response.lower() == 'oui' if 'question_15' in self.engine.responses else False,
            hobby_lec=self.engine.question_16_response.lower() == 'lecture' if 'question_16' in self.engine.responses else False,
            hobby_sport=self.engine.question_16_response.lower() == 'sports' if 'question_16' in self.engine.responses else False,
            facts_fascinants=self.engine.question_17_response.lower() == 'oui' if 'question_17' in self.engine.responses else False,
            combat_explosions=self.engine.question_18_response.lower() == 'oui' if 'question_18' in self.engine.responses else False,            
        ))              
        self.engine.run()

        self.manager.current = self.manager.next()


class ResultScreen(Screen):
    def __init__(self, engine, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        self.engine = engine
        self.result_layout = None
        self.layout_created = False

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        if not self.layout_created:
            self.create_result_layout()
            self.layout_created = True 
        else:
            print("Result Layout already created")

    def create_result_layout(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_dir, 'movie.jpeg')
        background_layout = BackgroundLayout(image_source=image_path)
        result_layout = MDBoxLayout(orientation='vertical', spacing=5, padding=5, size_hint=(None, None))
        result_layout.width = self.width  

        result_layout.clear_widgets()

        print("Recommended movies:", self.engine.recommended_movies) 

        if self.engine.recommended_movies:
            result_label = MDLabel(text=f"Film recommandé :\n {self.engine.recommended_movies[-1]}", font_style='Subtitle1', size_hint_x=3, size_hint_y=None)
            result_layout.add_widget(result_label)
        else:
            result_label = MDLabel(text="Film recommandé :\n Fast and Furious", halign="center", font_style='Subtitle1', size_hint_x=3,size_hint_y=None)
            result_layout.add_widget(result_label)

        remaining_space = 1 - result_layout.height / self.height
        result_layout.add_widget(Widget(size_hint_y=remaining_space))
        self.add_widget(background_layout)
        self.add_widget(result_layout)
        result_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        restart_button = CustomChoiceButton(
            size=(dp(120), dp(40)),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},  
            text="Restart",
            on_release=self.restart
        )

        result_layout.add_widget(restart_button)


    def restart(self, instance):
        print("befor:" , self.engine.recommended_movies)
        self.engine.clear_recommended_movies()
        print("after:" , self.engine.recommended_movies)
        self.engine.reset()
        self.layout_created = False  
        question_manager = self.manager
        question_manager.transition.direction = 'left'
        question_manager.current = "question_0"


class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.create_start_layout()

    def create_start_layout(self):
        background_layout = BackgroundLayout(image_source='C:/Users/manou/OneDrive/Bureau/ProjetIA/movie.jpeg')
        self.add_widget(background_layout)

        title_label = MDLabel(
            text="Quel film dois-je regarder?",
            font_style='H4',
            theme_text_color="Secondary",
            halign='center',
            size_hint=(None, None),
            size=(dp(350), dp(70)),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        self.add_widget(title_label)
        start_button = MDIconButton(
            icon="play",
            theme_text_color="Custom",  
            text_color=(1, 1, 1, 1), 
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            user_font_size="40sp", 
            on_release=self.start_questionnaire
        )
        start_button.md_bg_color = (215/255, 71/255, 71/255, 0.8)  # (R, G, B, A)
        self.add_widget(start_button)

    def start_questionnaire(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = "question_0"

class MovieRecommendationApp(MDApp):
    def build(self):
        Window.size = (300, 550)
        self.engine = InterferenceEngine()
        self.screen_manager = ScreenManager()
        start_screen = StartScreen(name="start_screen")
        self.screen_manager.add_widget(start_screen)
        questions = [
            {"question": "Avec qui allez-vous regarder un film?", "choices": ["Amis", "Famille", "Solo", "Partenaire"]},
            {"question": "Avez vous peur?", "choices": ["Oui", "Non"]},
            {"question": "Appréciez-vous la musique ?", "choices": ["Oui", "Non"]},
            {"question": "Êtes-vous intéressé par des films basés sur la vie de personnalités réelles?", "choices": ["Oui", "Non"]},           
            {"question": "Quel âge as-tu ?", "choices": ["12 ans et moins", "Entre 13 et 18 ans", "Plus que 18"]},
            {"question": "Aimez-vous les voyages et les aventures ?", "choices": ["Oui", "Non"]},
            {"question": "Si l'occasion se présentait, seriez-vous partant(e) pour vivre sur une île déserte ?", "choices": ["Oui", "Non"]},
            {"question": "Aimez-vous lire des romans ?", "choices": ["Oui", "Non"]},
            {"question": "Avez-vous eu une dure journée ?", "choices": ["Oui", "Non"]},           
            {"question": "Appréciez-vous les histoires qui stimulent l'imagination et explorent des mondes fantastiques ?", "choices": ["Oui", "Non"]},
            {"question": "Si vous pouviez voyager dans le temps, où choisiriez-vous d'aller", "choices": ["Passé", "Futur"]},
            {"question": "Quel type d'émotion recherchez-vous principalement en regardant un film ?", "choices": ["Rire", "Pleurer","Être captivé par action","Réfléchir profondément"]},
            {"question": "Quelle est votre réaction face à des scènes d'action intense et de batailles épiques ?", "choices": ["J'adore, c'est excitant!", "Ce n'est pas mon truc"]},
            {"question": "Si vous pouviez passer une journée à discuter avec une personne célèbre du passé ou du présent, qui choisiriez-vous?", "choices": ["Personnalités de guerre", "Personnalités musicales"]},           
            {"question": "Envie d'une soirée cinéma avec un soupçon de magie, d'aventure et d'humour ?", "choices": ["Oui", "Non"]},
            {"question": "Si une histoire captivante était narrée par des personnages dessinés, serais-tu partant pour une soirée animée?", "choices": ["Oui", "Non"]},
            {"question": "Quel est votre passe-temps préféré en dehors du travail ou des études ?", "choices": ["Lecture", "Sports"]},
            {"question": "Lorsque vous discutez de films avec des amis, êtes-vous plus enclin(e) à partager des faits fascinants de la réalité ?", "choices": ["Oui", "Non"]},
            {"question": "Aimez-vous les films avec des scènes de combat et d'explosions?", "choices": ["Oui", "Non"]}, 
        ]

        for i, question_data in enumerate(questions):
            screen_name = f"question_{i}"
            screen = QuestionScreen(name=screen_name, question_data=question_data, key=f"question_{i}", engine=self.engine)
            self.screen_manager.add_widget(screen)

        result_screen = ResultScreen(name="result_screen", engine=self.engine)
        result_screen.create_result_layout()  
        self.screen_manager.add_widget(result_screen)

        return self.screen_manager

if __name__ == "__main__":
    MovieRecommendationApp().run()