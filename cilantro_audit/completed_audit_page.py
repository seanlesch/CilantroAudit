import kivy
from cilantro_audit.excel_file import ExcelFile
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.utils import get_hex_from_color
from mongoengine import connect

from cilantro_audit.completed_audit import CompletedAudit
from cilantro_audit.audit_template import AuditTemplate
from cilantro_audit.constants import KIVY_REQUIRED_VERSION, PROD_DB, RGB_RED, RGB_YELLOW, RGB_GREEN

import os

kivy.require(KIVY_REQUIRED_VERSION)

kvfile = Builder.load_file("./widgets/completed_audit_page.kv")

connect(PROD_DB)


# Class for adding a block of text on a completed audit page that holds one question and the answers provided.
class QuestionAnswer(FloatLayout):
    question_label = ObjectProperty()
    question_text = StringProperty()

    answer_response_label = ObjectProperty()
    answer_response_text = StringProperty()

    answer_comments_label = ObjectProperty()
    answer_comments_text = StringProperty()

    answer_severity_label = ObjectProperty()
    answer_severity_text = StringProperty()


# Class for the save dialog popup.
class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


# Class for the popup that asks you if you want to overwrite a file.
class OverwritePopup(FloatLayout):
    yes = ObjectProperty(None)
    no = ObjectProperty(None)


# Class for the popup that lets you know your file was saved.
class FileSavedPopup(FloatLayout):
    ok = ObjectProperty(None)


# Class for the popup that gives you an error if you are not saving a file.
class ErrorPopup(FloatLayout):
    ok = ObjectProperty(None)


# Class for the completed audit.
class CompletedAuditPage(Screen):
    stack_list = ObjectProperty()
    grid_list = ObjectProperty()
    question_text = ObjectProperty()
    scrolling_panel = ObjectProperty()
    header_title = ObjectProperty()
    header_auditor = ObjectProperty()
    header_dt = ObjectProperty()
    main_popup = ObjectProperty()
    overwrite_popup = ObjectProperty()
    file_saved_popup = ObjectProperty()
    error_popup = ObjectProperty()
    other_popup = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.completed_audits = []
        self.audit_templates = []
        self.load_completed_audits()
        self.load_audit_templates()
        self.ca = CompletedAudit()
        self.at = AuditTemplate()

    # Loads all of the completed_audit objects from the database into a list.
    def load_completed_audits(self):
        self.completed_audits = list(CompletedAudit.objects().all_fields())
        self.completed_audits = sorted(self.completed_audits, key=lambda completed_audit: completed_audit.title)

    # Loads all of the audit_template objects from the database into a list.
    def load_audit_templates(self):
        self.audit_templates = list(AuditTemplate.objects().all_fields())
        self.audit_templates = sorted(self.audit_templates, key=lambda audit_template: audit_template.title)

    def reset_scroll_to_top(self):  # needs to be used in the routine that first populates the questions.
        # https://kivy.org/doc/stable/api-kivy.uix.scrollview.html Y scrolling value, between 0 and 1. If 0,
        # the content’s bottom side will touch the bottom side of the ScrollView. If 1, the content’s top side will
        # touch the top side.
        self.scrolling_panel.scroll_y = 1

    # Adds a title to the header
    def add_title(self, title):  # needs to be updated when you click out of one audit and load up another
        lbl = Label(text='[b]Audit: [/b]' + title, markup=True, size_hint_y=None, height=40, font_size=20,
                    halign="left")
        self.header_title = Label(text=title)
        self.grid_list.add_widget(lbl)

    # Adds the name of the auditor to the header.
    def add_auditor(self, auditor):  # needs to be updated when you click out of one audit and load up another
        lbl = Label(text='[b]Auditor: [/b]' + auditor, markup=True, size_hint_y=None, height=40, font_size=20,
                    halign="left")
        self.header_auditor = Label(text=auditor)

        self.grid_list.add_widget(lbl)

    # Adds the date/time to the header
    def add_date_time(self, dt):  # needs to be updated when you click out of one audit and load up another
        lbl = Label(text='[b]Date: [/b]' + dt, markup=True, size_hint_y=None, height=40, font_size=20, halign="left")
        self.header_dt = Label(text=dt)
        self.grid_list.add_widget(lbl)

    # Adds a blank label to the header for spacing.
    def add_blank_label(self, text):
        lbl = Label(text=text, size_hint_y=None, height=40, font_size=20, halign="left")
        self.grid_list.add_widget(lbl)

    # Adds one question/answer block to a completed audit page.
    def add_question_answer(self, question, answer):
        self.stack_list.height += 130  # integer (80) comes from question_answer size
        qa = QuestionAnswer()
        qa.question_text = "[b]Question: [/b]" + question.text
        qa.answer_response_text = "[b]Response: [/b]" + str(answer.response.response)
        qa.answer_comments_text = "[b]Comments: [/b]" + str(answer.comment)
        qa.answer_severity_text = "[b]Severity: [/b]" + str(answer.severity.severity)
        if qa.answer_severity_text == "[b]Severity: [/b]RED":
            qa.answer_severity_text = "[b]Severity: [/b][color="+get_hex_from_color(RGB_RED)+"]RED[/color]"
        elif qa.answer_severity_text == "[b]Severity: [/b]YELLOW":
            qa.answer_severity_text = "[b]Severity: [/b][color="+get_hex_from_color(RGB_YELLOW)+"]YELLOW[/color]"
        elif qa.answer_severity_text == "[b]Severity: [/b]GREEN":
            qa.answer_severity_text = "[b]Severity: [/b][color=#21ff2c]GREEN[/color]"
        self.stack_list.add_widget(qa)

    # Clears the page.
    def clear_page(self):
        self.grid_list.clear_widgets()
        self.stack_list.clear_widgets()
        self.stack_list.height = 0  # resets the height of the scrolling view. otherwise it grows with each new audit
        self.reset_scroll_to_top()

    # Closes the main file dialog popup.
    def close_main_popup(self):
        self.main_popup.dismiss()

    # Closes the overwrite popup.
    def close_overwrite_popup(self):
        self.overwrite_popup.dismiss()

    # Closes the error popup.
    def close_error_popup(self):
        self.error_popup.dismiss()

    # Closes the file saved popup.
    def close_file_saved_popup(self):
        self.file_saved_popup.dismiss()

    # Opens/builds the save dialog popup
    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.close_main_popup)
        self.main_popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self.main_popup.open()

    # Saves the file and does necessary checks.
    def save(self, path, filename):
        file_path = os.path.join(path, filename)
        ef = ExcelFile(self.header_title.text, self.header_auditor.text, self.header_dt.text, self.at, self.ca)
        sheetname = self.header_auditor.text + " - " + self.header_title.text
        wb = ef.open_file(sheetname, file_path)
        if file_path.endswith("\\"):
            content = ErrorPopup(ok=self.close_error_popup)
            self.error_popup = Popup(title="File Error", content=content, size_hint=(0.5, 0.5))
            self.error_popup.open()
        elif not file_path.endswith(".xlsx"):
            file_path = file_path + ".xlsx"
            if os.path.exists(file_path):
                content = OverwritePopup(yes=lambda: self.replace_file(wb, file_path), no=self.close_overwrite_popup)
                self.overwrite_popup = Popup(title="Overwrite File?", content=content, size_hint=(0.5, 0.5))
                self.overwrite_popup.open()
            else:
                wb.save(file_path)
                self.close_main_popup()
                content = FileSavedPopup(ok=self.close_file_saved_popup)
                self.file_saved_popup = Popup(title="File Exported", content=content, size_hint=(0.5, 0.5))
                self.file_saved_popup.open()
        else:
            if os.path.exists(file_path):
                content = OverwritePopup(yes=lambda: self.replace_file(wb, file_path), no=self.close_overwrite_popup)
                self.overwrite_popup = Popup(title="Overwrite File?", content=content, size_hint=(0.5, 0.5))
                self.overwrite_popup.open()
            else:
                wb.save(file_path)
                self.close_main_popup()
                content = FileSavedPopup(ok=self.close_file_saved_popup)
                self.file_saved_popup = Popup(title="File Exported", content=content, size_hint=(0.5, 0.5))
                self.file_saved_popup.open()

    # Overwrites a file.
    def replace_file(self, wb, path_to_file):
        os.remove(path_to_file)
        wb.save(path_to_file)
        self.overwrite_popup.dismiss()
        self.close_main_popup()
        content = FileSavedPopup(ok=self.close_file_saved_popup)
        self.file_saved_popup = Popup(title="File Exported", content=content, size_hint=(0.5, 0.5))
        self.file_saved_popup.open()