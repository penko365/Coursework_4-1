from dbfunc2 import *
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
# from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.button import MDFlatButton
# from kivymd.uix.textfield import MDTextField
# from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog

from kivymd.uix.scrollview import MDScrollView
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.relativelayout import MDRelativeLayout

from kivymd.uix.list import OneLineIconListItem

Builder.load_file('kv/Navigation.kv')

authDict = {
    'dbname':'dbname',
    'user':'username',
    'password':'password',
    'host':'localhost',
    'port': '2345',
    'conn_state': False,
    'sslmode':'require'
}

class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

#--------------------------------------------

class LoginScreen(MDScreen):

    def login(self):
        print("-----------SoMeTh")
        db_name = self.ids.dbname_fld.text
        user_name = self.ids.username_fld.text
        password = self.ids.password_fld.text
        host = self.ids.host_fld.text
        if db_name!='' or user_name!='' or password!='' or host!='':
            host_ip, host_port = host.split(':')
            print(host_ip)
            print(host_port)
            authDict.update({'dbname': db_name, 'user': user_name, 'password': password, 'host': host_ip, 'port': host_port})
            print(authDict)
            if connectToDB(authDict) == -1:
                alert = MainApp()
                alert.showAlert("[!] FAIL")
            else:
                authDict.update({'conn_state': True})
                self.manager.current = "MainScreen"
        else:
            alert = MainApp()
            alert.showAlert("[!] One or more fields are blank.")

#---
class CustomOneLineIconListItem(OneLineIconListItem):
    pass

class DrugSearchScreen(MDScreen):
    rv_data = ListProperty()
    def searchData(self, drug_name):
        def add_drug_item(drug_name):
            self.ids.rv.data.append(
                {
                    "viewclass": "CustomOneLineIconListItem",
                    "text": drug_name,
                    "font_size": 18,
                    "callback": lambda x: x,
                }
            )

        self.ids.rv.data = []
        # drug_name = self.ids.drug_name_fld.text()
        # drug_atc = self.ids.inputline_drug_atc.text()
        if drug_name != '':
            res = find_drugs(authDict, drug_name, '')
            print(res)
            if res != 0:
                # self.fillTable(res)
                for tup in res:
                    print(f"---{tup}")
                    if drug_name.upper() in tup[1]:
                        add_drug_item(f'{tup[1]}  {tup[2]}')

            elif res == -1:
                alert = MainApp()
                alert.showAlert("[!] Error connecting to database.")
            else:
                alert = MainApp()
                alert.showAlert("Nothing was found...")
        else:
            self.ids.rv.data = []

#---
class DrugAddScreen(MDScreen):
    def insertData(self):
        inputCorrect = True
        error_message = ""
        name = self.ids.drug_name_fld.text
        atc = self.ids.drug_atc_fld.text
        quantity = self.ids.drug_quantity_fld.text
        # descr = self.ids.inputline_drug_description.toPlainText()
        descr = ''
        drug_id = ''

        # manufacturer_id_name = (self.ids.manufacturerComboBox.currentText()).split(' ')
        # supplier_id_name = (self.ids.supplierComboBox.currentText()).split(' ')
        # manufacturer_is_supplier = self.ids.manufacturer_is_supplier_checkbox.isChecked()
        manufacturer_id = '1'
        # manufacturer_name = ''
        supplier_id = '1'
        # supplier_name = ''
        # whith_supplier_exists = False
        # whith_manufacturer_exists = False
        # absolutely_new_drug = False

        if name == '':
            inputCorrect = False
            error_message += '[!] Drug name field is blank.\n'
        
        if atc != '':
            if check_atc_chemical_substance(authDict, atc) == 0:
                inputCorrect = False
                error_message += '[!] ATC "{}" doesn\'t exists in database.\n'.format(atc.upper())
        else:
            inputCorrect = False
            error_message += '[!] ATC field is blank.\n'

        # if manufacturer_id_name != ['']:
        #     manufacturer_id = manufacturer_id_name[0]
        #     manufacturer_name = manufacturer_id_name[1]
        # else:
        #     inputCorrect = False
        #     error_message += '[!] Manufacturer is not selected.\n'

        # if manufacturer_is_supplier == False:
        #     if supplier_id_name != ['']:
        #         supplier_id = supplier_id_name[0]
        #         supplier_name = supplier_id_name[1]
        #     else:
        #         inputCorrect = False
        #         error_message += '[!] Supplier is not selected.\n'
        # elif manufacturer_is_supplier == True and manufacturer_id_name != ['']:
        #     supplier_id, supplier_name = manufacturer_id, manufacturer_name

        if descr == '':
            descr = "Some description."
        if check_drugs(authDict, name, atc) == 0:
            print(f'>{name}<  >{atc}<')
            absolutely_new_drug = True
            inputCorrect = False
            error_message += '[!] Drug with current parameters is not in database.\n'

        if inputCorrect:
            res = 1
            
            drug_data = get_drug(authDict, name, atc)
            drug_id = str(drug_data[0][0])
            current_quantity = int(drug_data[0][3])
            updated_quantity = str(current_quantity + int(quantity))
            res = update_drugs(authDict, drug_id, quantity=updated_quantity)
            if check_drugs(authDict, name, atc, manufacturer_id) == 1:
                whith_manufacturer_exists = True
            if check_drugs(authDict, name, atc, supplier_id=supplier_id) == 1:
                whith_supplier_exists = True
        
            drug_data = get_drug(authDict, name, atc)
            print(drug_data)
            if drug_data != 0:
                drug_id = str(drug_data[0][0])
            # if whith_manufacturer_exists == False:
            #     res1 = insert_drug_manufacturer(authDict, drug_id, manufacturer_id)
            # if whith_supplier_exists == False:
            #     res2 = insert_drug_supplier(authDict, drug_id, supplier_id)
            # get_drug(authDict, name=name, atc=atc, descr=descr)[0][0]
        
            if res == 1:
                done_msg = "Quantity of existing drug was increased"
                # self.flushFields()
                alert = MainApp()
                alert.showAlert(done_msg)
            else:
                alert = MainApp()
                alert.showAlert("[!] Error connecting to database.")
        else:
            alert = MainApp()
            alert.showAlert(error_message)


class MainScreen(MDScreen):
    pass

class RootWidget(ScreenManager):
    pass

#--------------------------------------------


class MainApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        return RootWidget()

    def showAlert(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text = message,
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda _: self.dialog.dismiss()
                    )
                ],
            )
        self.dialog.open()

if __name__ == "__main__":
    MainApp().run()