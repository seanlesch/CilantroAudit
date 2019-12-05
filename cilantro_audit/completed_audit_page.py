from cilantro_audit.excel_file import ExcelFile
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.utils import get_hex_from_color
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout

from cilantro_audit.constants import PROD_DB
from cilantro_audit.constants import RGB_RED
from cilantro_audit.constants import RGB_GREEN
from cilantro_audit.constants import RGB_YELLOW

from cilantro_audit.completed_audit import CompletedAudit
from cilantro_audit.audit_template import AuditTemplate

import os

kvfile = Builder.load_file("./widgets/completed_audit_page.kv")
from mongoengine import connect

from cilantro_audit.create_completed_audit_page import ConfirmationPop

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

    resolve_button = ObjectProperty(None)

    # Handles popup to confirm the resolving of a flagged question.
    def resolve_response(self):
        show = ResolvePop()
        show.yes.bind(on_release=lambda _: show.dismiss())
        show.yes.bind(on_release=lambda _: self.resolve_submit())
        show.no.bind(on_release=lambda _: show.dismiss())
        show.open()

    # Marks a question response as resolved in the database. NOTE: Currently if there are repeated questions in the
    # audit the behavior of which question will be resolved is undefined.
    def resolve_submit(self):
        audit_to_resolve = CompletedAudit.objects() \
            .filter(title=self.resolve_button.title,
                    auditor=self.resolve_button.auditor,
                    datetime=self.resolve_button.datetime) \
            .get(title=self.resolve_button.title,
                 auditor=self.resolve_button.auditor,
                 datetime=self.resolve_button.datetime)
        # Remove string label, which has 17 chars as defined in CompletedAuditPage.add_question_answer
        audit_answer_to_resolve = audit_to_resolve.answers.filter(text=self.question_text[17:]) \
            .get(text=self.question_text[17:])
        audit_answer_to_resolve.resolved = True
        audit_to_resolve.unresolved_count -= 1
        audit_to_resolve.save()
        self.remove_widget(self.resolve_button)

class ResolvePop(ConfirmationPop):
    yes = ObjectProperty(None)
    no = ObjectProperty(None)

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
    previous_page = ""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.completed_audits = []
        self.audit_templates = []
        self.load_completed_audits()
        self.load_audit_templates()
        self.ca = CompletedAudit
        self.at = AuditTemplate()

    # Loads all of the completed_audit objects from the database into a list.
    def load_completed_audits(self):
        self.completed_audits = list(CompletedAudit.objects().all_fields())
        self.completed_audits = sorted(self.completed_audits, key=lambda completed_audit: completed_audit.title)

    # Loads all of the audit_template objects from the database into a list.
    def load_audit_templates(self):
        self.audit_templates = list(AuditTemplate.objects().all_fields())
        self.audit_templates = sorted(self.audit_templates, key=lambda audit_template: audit_template.title)

    def reset_scroll_to_top(self):
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

    def add_question_answer(self, answer, title, datetime, auditor):
        self.stack_list.height += 125  # integer (85) comes from question_answer size
        qa = QuestionAnswer()
        qa.question_text = "[b]Question: [/b]" + answer.text
        qa.answer_response_text = "[b]Response: [/b]" + str(answer.response.response)
        qa.answer_comments_text = "[b]Comments: [/b]" + str(answer.comment)
        qa.answer_severity_text = "[b]Severity: [/b]" + str(answer.severity.severity[2:])
        if qa.answer_severity_text == "[b]Severity: [/b]RED":
            qa.answer_severity_text = "[b]Severity: [/b][color=" + get_hex_from_color(RGB_RED) + "]RED[/color]"
            if not answer.resolved:
                qa.resolve_button.visible = True
                qa.resolve_button.datetime = datetime
                qa.resolve_button.title = title
                qa.resolve_button.auditor = auditor
        elif qa.answer_severity_text == "[b]Severity: [/b]YELLOW":
            qa.answer_severity_text = "[b]Severity: [/b][color=" + get_hex_from_color(RGB_YELLOW) + "]YELLOW[/color]"
        elif qa.answer_severity_text == "[b]Severity: [/b]GREEN":
            qa.answer_severity_text = "[b]Severity: [/b][color=" + get_hex_from_color(RGB_GREEN) + "]GREEN[/color]"
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
        ef = ExcelFile(self.header_title.text, self.header_auditor.text, self.header_dt.text, self.ca.datetime)
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