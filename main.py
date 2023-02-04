import os
from bson import ObjectId
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineAvatarIconListItem, MDList, IconLeftWidget, IconRightWidget
from kivymd.uix.scrollview import MDScrollView
from pymongo import MongoClient
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
import reconhecimento.Coletor_de_dados as cd
import cv2


client = MongoClient('URL')
db = client['Cluster0']
collection = db['trfse']

way = "reconhecimento/dataset/"
data_path = 'reconhecimento/dataset/User.'

def GerarId():
    result = True
    Id = 0
    user_ids = []
    for i in collection.find():
        user_ids.append(i["_id"])
    while True:
        result = True
        for id in user_ids:
            if Id == id:
                Id += 1
                result = False
                break
        if result:
            return str(Id)

def CadastrarUser(id, nome, rg, cpf, matricula, telefone):
    data = {"_id": id, "nome": nome, "rg": rg, "cpf": cpf, "matricula": matricula, "telefone": telefone}
    collection.insert_one(data)

def ListUsers():
    dic = {}
    for u in collection.find():
        dic[f"{u['nome'].lower()}"] = {"id": u["_id"], "nome": u["nome"], "matricula": u["matricula"]}
    return dic

def DeleteUser(id):
    collection.delete_one({"_id": id})
    for i in range(9999):
        cont = 5
        try:
            os.remove(way + f"User.{id}.{i}.jpg")
        except:
            if cont == 0:
                break
            else:
                cont += 1

class Home_Screen(Screen):
    def sair_lista(self):
        try:
            self.ids.lista.pos_hint = {"center_y": 10}
            self.ids.lista_users.remove_widget(self.scrow)
        except:
            pass

    def atualizar_lista(self):
        try:
            self.ids.lista_users.remove_widget(self.scrow)
        except:
            pass
        self.ids.lista.pos_hint = {"center_y": .5}

        self.lista_itens = []
        self.list_users = ListUsers()
        self.lista_ordem = sorted(self.list_users)
        self.scrow = MDScrollView()
        self.list = MDList()

        for i in self.lista_ordem:
            self.items = TwoLineAvatarIconListItem(IconRightWidget(id=str(self.list_users[i]['id']), icon="trash-can-outline", on_release=lambda x: self.excluir_user(x.id)), id=str(self.list_users[i]['id']), text=self.list_users[i]['nome'], secondary_text=f"Matrícula: {self.list_users[i]['matricula']}", on_release=lambda x: self.card_user(x.id))
            self.lista_itens.append(self.items)
            self.list.add_widget(self.items)
        self.scrow.add_widget(self.list)
        self.ids.lista_users.add_widget(self.scrow)

    def deleta_e_atualiza(self, id):
        DeleteUser(id)
        self.atualizar_lista()
        self.dialog.dismiss(force=True)

    def excluir_user(self, id):
        self.dialog = MDDialog(
            text="Tem certeza que deseja excluir esse usúario?",
            buttons=[
                MDFlatButton(
                    text="Não",
                    theme_text_color="Custom",
                    text_color="blue",
                    on_release=lambda x: self.dialog.dismiss(force=True)
                ),
                MDFlatButton(
                    text="Sim",
                    theme_text_color="Custom",
                    text_color="blue",
                    on_release=lambda x: self.deleta_e_atualiza(id)
                )])
        self.dialog.open()

    def card_user(self, id):
        self.sair_lista()
        self.user = collection.find_one({"_id": id})
        self.ids.user_card.pos_hint = {"center_y": .5}
        self.ids.edit_nome.text = f"Nome: {self.user['nome']}"
        self.ids.edit_id.text = f"ID: {self.user['_id']}"
        self.ids.edit_id1.text = f"ID: {self.user['_id']}"
        if self.user['cpf'] != "":
            self.ids.edit_cpf.text = f"CPF: {self.user['cpf']}"
        if self.user['rg'] != "":
            self.ids.edit_rg.text = f"RG: {self.user['rg']}"
        self.ids.edit_matricula.text = f"Matrícula: {self.user['matricula']}"
        if self.user['telefone'] != "":
            self.ids.edit_telefone.text = f"Telefone: {self.user['telefone']}"

    def sair_card_user(self):
        self.ids.user_card.pos_hint = {"center_y": 10}
        self.atualizar_lista()

    def voltar_card_user(self):
        self.ids.edit_user.pos_hint = {"center_y": 10}
        self.ids.user_card.pos_hint = {"center_y": .5}

    def abrir_edit_user(self):
        self.ids.txt_nome.text = ""
        self.ids.txt_cpf.text = ""
        self.ids.txt_rg.text = ""
        self.ids.txt_matricula.text = ""
        self.ids.txt_telefone.text = ""
        self.ids.edit_user.pos_hint = {"center_y": .5}
        self.ids.user_card.pos_hint = {"center_y": 10}

    def salvar_edit_user(self):
        self.nome = self.ids.txt_nome.text
        self.cpf = self.ids.txt_cpf.text
        self.rg = self.ids.txt_rg.text
        self.matricula = self.ids.txt_matricula.text
        self.telefone = self.ids.txt_telefone.text
        if self.nome != "":
            collection.update_one(self.user, {"$set": {"nome": self.nome}})

        if self.cpf != "":
            collection.update_one(self.user, {"$set": {"cpf": self.cpf}})

        if self.rg != "":
            collection.update_one(self.user, {"$set": {"rg": self.rg}})

        if self.matricula != "":
            collection.update_one(self.user, {"$set": {"matricula": self.matricula}})

        if self.telefone != "":
            collection.update_one(self.user, {"$set": {"telefone": self.telefone}})

        self.dialog = MDDialog(
            text="Edição concluído com sucesso!",
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color="blue",
                    on_release=lambda x: self.dialog.dismiss(force=True)
                )])
        self.dialog.open()
        self.ids.edit_user.pos_hint = {"center_y": 10}
        self.card_user(self.user["_id"])

class Register_Screen(Screen):
    def register_screen(self):
        self.ids.frente.pos_hint = {"center_y": 10}
        self.ids.cima.pos_hint = {"center_y": 10}
        self.ids.baixo.pos_hint = {"center_y": 10}
        self.ids.esquerda.pos_hint = {"center_y": 10}
        self.ids.direita.pos_hint = {"center_y": 10}
        self.ids.nome.text = ""
        self.ids.cpf.text = ""
        self.ids.rg.text = ""
        self.ids.matricula.text = ""
        self.ids.telefone.text = ""

    def frente_screen(self):
        self.nome = self.ids.nome.text
        self.cpf = self.ids.cpf.text
        self.rg = self.ids.rg.text
        self.matricula = self.ids.matricula.text
        self.telefone = self.ids.telefone.text
        if len(self.nome) > 2 and len(self.matricula) > 2:
            self.ids.frente.pos_hint = {"center_y": .5}
            self.id = GerarId()

        else:
            self.dialog = MDDialog(
                text="Por favor insira os campos obrigatórios",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color="blue",
                        on_release=lambda x: self.dialog.dismiss(force=True)
                    ),
                ],
            )
            self.dialog.open()



    def cima_screen(self):
        self.fotos = []
        f1 = cd.program(25)
        self.fotos.append(f1)
        self.ids.cima.pos_hint = {"center_y": .5}

    def baixo_screen(self):
        f2 = cd.program(25)
        self.fotos.append(f2)
        self.ids.baixo.pos_hint = {"center_y": .5}

    def esquerda_screen(self):
        f3 = cd.program(25)
        self.fotos.append(f3)
        self.ids.esquerda.pos_hint = {"center_y": .5}

    def direita_screen(self):
        f4 = cd.program(25)
        self.fotos.append(f4)
        self.ids.direita.pos_hint = {"center_y": .5}

    def ultimo_screen(self):
        f5 = cd.program(25)
        self.fotos.append(f5)
        count = 0
        for i in self.fotos:
            for face in i:
                cv2.imwrite(data_path + str(self.id) + '.' + str(count) + '.jpg', face)
                # cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (168, 200, 173), 2)
                count += 1
        # os.system('python reconhecimento/Treino.py')
        CadastrarUser(self.id, self.nome, self.rg, self.cpf, self.matricula, self.telefone)
        self.dialog = MDDialog(
            text="Usuário Cadastrado Com Sucesso!",
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color="blue",
                    on_release=lambda x: self.dialog.dismiss(force=True)
                ),
            ],
        )
        self.dialog.open()
        self.register_screen()


class Screen_Manager(ScreenManager):
    pass

class Aplicativo_(MDApp):
    def build(self):
        Window.size = (1024, 720)
        self.title = 'TRFSE'
        self.theme_cls.primary_palette = 'Blue'
        return Builder.load_file("main.kv")

    def Sair(self):
        self.stop()

if __name__ == "__main__":
    Aplicativo_().run()



