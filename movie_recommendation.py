from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.metrics import dp

class MovieRecommendationApp(MDApp):
    def build(self):
        self.screen = MDScreen()

        # Liste des questions avec choix
        questions = [
            {"question": "Quel genre de film préférez-vous ?", "choices": ["Action", "Comédie", "Drame"]},
            {"question": "Avez-vous peur des films d'horreur ?", "choices": ["Oui", "Non"]},
            # Ajoutez d'autres questions selon vos besoins
        ]

        # Utilisation d'une grille pour organiser les éléments
        grid_layout = MDGridLayout(cols=1, adaptive_height=True, padding=10, spacing=10)

        # Création des widgets pour chaque question
        for question_data in questions:
            question_label = MDLabel(text=question_data["question"], halign="center", size_hint_y=None, height=dp(40))
            grid_layout.add_widget(question_label)

            for choice in question_data["choices"]:
                button = MDRaisedButton(text=choice, on_release=self.show_result)
                grid_layout.add_widget(button)

        # Ajout de la grille à l'écran
        self.screen.add_widget(grid_layout)

        return self.screen

    def show_result(self, instance):
        # Afficher la réponse de l'utilisateur dans une boîte de dialogue
        user_response = instance.text
        dialog = MDDialog(
            title="Votre choix",
            text=f"Vous avez choisi : {user_response}",
            buttons=[
                MDFlatButton(
                    text="Fermer", on_release=lambda x: dialog.dismiss()
                )
            ],
        )
        dialog.open()

if __name__ == "__main__":
    MovieRecommendationApp().run()
