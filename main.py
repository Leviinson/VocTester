import os
import sys
import json
import random
import logging
from typing import Dict, List
from dataclasses import dataclass

from PySide6 import (QtCore,
                     QtWidgets,
                     QtGui)


@dataclass
class ListPoints:
    def __init__(self, list) -> None:
        self.list = list
        self.init_points()
    
    def init_points(self):
        self.start_index: int = 0
        self.stop_index: int = len(self.list) - 1
    

class MainWindow(QtWidgets.QWidget):
    '''
    Class, that represents 
    main window.

    Attributes:
    -----------
        Doesn't have

    Methods:
    --------
        run() -> None:

    '''
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Vocabulary tester")
        self.resize(500, 100)
        self.layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.number_of_correct_answers = 0
        self.last_frame_index = 0
        self.setLayout(self.layout)


    def run(self):
        '''
        Creates frames, that contains question and navigation widgets
        in random order.

        Parameters:
        -----------
            Doesn't have
        '''
        self.show()

        vocabulary_words = self.get_vocabulary_words(language='pl')
        random_questions_indexes = random.sample(range(len(vocabulary_words)), len(vocabulary_words))
        sequence_entry_points = ListPoints(random_questions_indexes)
        self.last_frame_index = sequence_entry_points.stop_index

        for frame_index, random_question_index in enumerate(random_questions_indexes):
            question = vocabulary_words[random_question_index]['foreign_word']
            answer = vocabulary_words[random_question_index]['translation']
            match frame_index:
                case 0:
                    self.create_question_frame(question = question, answer = answer,
                                               is_first = True, current_frame_index = frame_index)
                    self.layout.itemAt(0).widget().show()
                case self.last_frame_index:
                    self.create_question_frame(question = question, answer = answer,
                                               is_last = True, current_frame_index = frame_index)
                case _:
                    self.create_question_frame(question = question, answer = answer, current_frame_index = frame_index)
        

    def get_vocabulary_words(self, language: str) -> List:
        '''
        Passes language abbreviature,
        returns deserialized dictionary from json to py-dict,
        which dynamically changes the type to "list" that contains
        dictionaries with next keys:
            question: text
            answer: text

        Parameters:
            language: str
                language abbreviature, such as: (en, pl, ru, ua etc.)
        '''
        try:
            with open('%s/vocabulary_%s.json' % (os.getcwd(), language)) as vocabulary:
                vocabulary: Dict = json.load(vocabulary)
            return list(
                        vocabulary.values()
                        )[0]
        except FileNotFoundError:
            logging.exception("Vocabulary with this language doesn't exist.")

    
    def create_question_frame(self, current_frame_index, question: str, answer: str,
                         is_first: bool = False, is_last: bool = False) -> None:
        '''
        '''
        frame = QuestionFrame(question = question, answer = answer,
                              is_first = is_first, is_last = is_last,
                              currect_frame_index = current_frame_index,
                              main_window = self)
        self.layout.addWidget(frame)
        frame.hide()

    
    def create_results_frame(self):
        ...


class QuestionFrame(QtWidgets.QFrame):
    '''
    Class, that represents 
    separate question frame.

    Attributes:
    -----------
        is_first: bool
            represents boolean value, if parent frame is first question

        is_last: bool
            represents boolean value, if parent frame is last question

        current_frame_index: int
            integer value, that represents number of the displayed frame in order

        question: str
            string value, that represets question for current frame

        answer: str
            string value, that represets answer to question for current frame

        main_window: MainWindow
            represents link to main window

    Methods:
    --------
        init_variables() -> None:
            inits passed variables to class instance.

        init_frame_widgets(self):
            inits widgets for current frame instance.

        init_question_label(self):
            creates label, that contains question text; pins current frame instance as parent for this widget
            by default.

        init_input_line(self):
            creates input line for answers; pins current frame instance as parent for this widget
            by default.

        init_response_label(self):
            creates label, that contains message meaning:
            "is user answer was correct?";
            pins current frame instance as parent for this widget by default.

        init_nav_menu(self):
            calls initializations for all necessary navigation menu buttons.

        init_button_ok(self):
            creates "ok" button; pins main window as parent for this widget.

        init_button_next(self):
            creates "next" button; pins current frame as a parent for this widget
            by default.

        init_button_back(self):
            creates "back" button; pins current frame as a parent for this widget
            by default.
        
        init_button_results(self):
            creates "results" button; pins current frame as a parent for this widget
            by default.
    '''
    def __init__(self, main_window: MainWindow, question: str, answer: str,
                       currect_frame_index: int, is_first: bool = False,
                       is_last: bool = False, is_results_frame: bool = False) -> None:
        super().__init__()
        self.layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(self)
        self.init_variables(is_first, is_last,
                            currect_frame_index,
                            question, answer)
        self.init_frame_widgets()
        self.setWindowTitle(question)
        Callbacker(frame = self,
                   answer = answer,
                   is_first = is_first,
                   is_last = is_last,
                   main_window = main_window,
                   is_results_frame = is_results_frame).init_callbacks()


    def init_variables(self, is_first: bool, is_last: bool,
                             current_frame_index: int,
                             question: str, answer: str):
        '''
        Inits passed variables
        to class instance.

        Parameters:
        -----------
            is_first: bool
                represents boolean value, if parent frame is first question
            is_last: bool
                represents boolean value, if parent frame is last question
            current_frame_index: int
                integer value, that represents number of the displayed frame in order
            question: str
                string value, that represets question for current frame
            answer: str
                string value, that represets answer to question for current frame
        '''
        self.is_first = is_first
        self.is_last = is_last
        self.question = question
        self.answer = answer
        self.current_frame_index = current_frame_index
        self.is_answer_correct = False

    
    def init_frame_widgets(self):
        '''
        Inits widgets for current frame instance.

        Parameters:
        -----------
            Doesn't have
        '''
        self.init_question_label()
        self.init_input_line()
        self.init_response_label()
        self.init_nav_menu()
    

    def init_question_label(self):
        '''
        Creates label, that contains question text;
        pins current frame instance as parent for this widget
        by default.

        Parameters:
        -----------
            Doesn't have
        '''
        self.question_label = QtWidgets.QLabel(parent = self)
        self.question_label.setText(self.question)
        self.layout.addWidget(self.question_label, alignment = QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignCenter)


    def init_input_line(self):
        '''
        Creates input line for answers;
        pins current frame instance as parent for this widget
        by default.

        Parameters:
        -----------
            Doesn't have
        '''
        self.input_line = QtWidgets.QLineEdit()
        self.layout.addWidget(self.input_line, alignment = QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignCenter)


    def init_response_label(self):
        '''
        Creates label, that contains message meaning:
        "is user answer was correct?";
        pins current frame instance as parent for this widget
        by default.

        Parameters:
        -----------
            Doesn't have
        '''
        self.response_label = QtWidgets.QLabel(parent = self)
        self.layout.addWidget(self.response_label, alignment = QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignCenter)


    def init_nav_menu(self):
        '''
        Calls initializations for all necessary
        navigation menu buttons.

        Parameters:
        -----------
            Doesn't have
        '''
        self.nav_menu = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.LeftToRight)
        self.layout.addLayout(self.nav_menu, stretch = 0)
        
        match self.is_first, self.is_last:
            case True, False:
                self.init_button_ok()
                self.init_button_next()

            case False, True:
                self.init_button_back()
                self.init_button_ok()
                self.init_button_results()

            case _:
                self.init_button_back()
                self.init_button_ok()
                self.init_button_next()
        

    def init_button_ok(self):
        '''
        Creates "ok" button,
        pins main window as parent for this widget.

        Parameters:
        -----------
            Doesn't have
        '''
        self.button_ok = QtWidgets.QPushButton(parent = self)
        self.button_ok.setText("Ok")
        match self.is_first, self.is_last:
            case True, False:
                self.nav_menu.addWidget(self.button_ok, alignment = QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignLeft)

            case False, True:
                self.nav_menu.addWidget(self.button_ok, alignment = QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignCenter)
    
            case _:
                self.nav_menu.addWidget(self.button_ok, alignment = QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignCenter)
            

    def init_button_next(self):
        '''
        Creates "next" button;
        pins current frame as a parent for this widget
        by default.

        Parameters:
        -----------
            Doesn't have
        '''
        self.button_next = QtWidgets.QPushButton(parent = self)
        self.button_next.setText("Next")
        self.nav_menu.addWidget(self.button_next, alignment = QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)


    def init_button_back(self):
        '''
        Creates "back" button;
        pins current frame as a parent for this widget
        by default.

        Parameters:
        -----------
            Doesn't have
        '''
        self.button_back = QtWidgets.QPushButton(parent = self)
        self.button_back.setText("Back")
        self.nav_menu.addWidget(self.button_back, alignment = QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignLeft)

    
    def init_button_results(self):
        '''
        Creates "results" button;
        pins current frame as a parent for this widget
        by default.

        Parameters:
        -----------
            Doesn't have
        '''
        self.button_results = QtWidgets.QPushButton(parent = self)
        self.button_results.setText("Results")
        self.nav_menu.addWidget(self.button_results, alignment = QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)

    
    def __repr__(self) -> str:
        return self.windowTitle()


class ResultsFrame(QtWidgets.QFrame):
    def __init__(self, current_frame_index: int,
                       main_window: MainWindow) -> None:
        super().__init__()
        self.current_frame_index = current_frame_index
        self.main_window = main_window
        self.layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(self)
        self.init_frame_widgets()
        
        self.setWindowTitle('Rezultaty')
        Callbacker(main_window = main_window,
                   frame = self,
                   is_results_frame = True).init_callbacks()


    def init_frame_widgets(self):
        self.init_results_label()
        self.init_nav_menu()

    
    def init_results_label(self):
        self.results_label = QtWidgets.QLabel(parent = self)
        self.results_label.setText("Ilość poprawnych odpowiedzi: %s" % self.main_window.number_of_correct_answers)
        self.layout.addWidget(self.results_label, alignment = QtCore.Qt.AlignmentFlag.AlignCenter)

    
    def init_nav_menu(self):
        self.nav_menu = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.nav_menu, stretch = 0)
        self.init_button_back()
        self.init_button_close()


    def init_button_back(self):
        '''
        Creates "back" button;
        pins current frame as a parent for this widget
        by default.

        Parameters:
        -----------
            Doesn't have
        '''
        self.button_back = QtWidgets.QPushButton(parent = self)
        self.button_back.setText("Back")
        self.nav_menu.addWidget(self.button_back, alignment = QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignLeft)
    

    def init_button_close(self):
        self.button_close = QtWidgets.QPushButton(parent = self)
        self.button_close.setText("Close")
        self.nav_menu.addWidget(self.button_close, alignment = QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)


class Callbacker:
    '''
    Class, that implements initialization of
    callbacks for buttons on one or the other frame.
    Also contains secondary functions.

    Attributes:
    -----------
    main_window: MainWindow
        represents link to main window
    frame: QuestionFrame
        represents link to parent frame
    is_first: bool
        represents boolean value, if parent frame is first question
    is_last: bool
        represents boolean value, if parent frame is last question


    Methods:

    init_variables(main_window, frame, answer, is_first, is_last) -> None:
        Constructs all the necessary attributes for the person object.

    init_callbacks() -> None:
        Inits all the necessary callbacks for buttons of parent frame
        depending on the information if parent frame is first, last or results frame.

    
    '''
    def __init__(self, main_window: MainWindow,
                       frame: QuestionFrame,
                       answer: str = None,
                       is_first: bool = False,
                       is_last: bool = False,
                       is_results_frame = False) -> None:
        self.init_variables(main_window = main_window,
                            frame = frame,
                            answer = answer,
                            is_first = is_first,
                            is_last = is_last,
                            is_results_frame = is_results_frame)
    

    def init_variables(self, main_window,
                             frame,
                             answer,
                             is_first,
                             is_last,
                             is_results_frame) -> None:
        '''
        Constructs all the necessary attributes for the person object.

        Parameters
        ----------
            main_window: MainWindow
                represents link to main window
            frame: QuestionFrame
                represents link to parent frame
            is_first: bool
                represents boolean value, if parent frame is first question
            is_last: bool
                represents boolean value, if parent frame is last question
        '''
        self.main_window = main_window
        self.frame = frame
        self.answer = answer
        self.is_first = is_first
        self.is_last = is_last
        self.is_results_frame = is_results_frame


    def init_callbacks(self) -> None:
        '''
        Inits all the necessary callbacks for buttons of parent frame
        depending on the information if parent frame is first, last or results frame.

        Parameters:
        -----------
            Doesn't have
        '''

        match self.is_results_frame:
            case False:
                match self.is_first, self.is_last:
                    case True, False:
                        self.set_callback_for_button_ok()
                        self.set_callback_for_button_next()
                    
                    case False, True:
                        self.set_callback_for_button_back()
                        self.set_callback_for_button_ok()
                        self.set_callback_for_button_results()
                    
                    case _:
                        self.set_callback_for_button_back()
                        self.set_callback_for_button_ok()
                        self.set_callback_for_button_next()
            
            case True:
                self.set_callback_for_button_close()
                self.set_callback_for_button_back()
        

    def set_callback_for_button_next(self) -> None:
        '''
        Inits callback for button "Next"
        Meaning of callback:
            hide current frame, show next frame.

        Parameters:
        -----------
            Doesn't have
        '''
        self.frame.button_next.clicked.connect(
            lambda: (
                    self.frame.hide(),
                    self.main_window.layout.itemAt(self.frame.current_frame_index + 1).widget().show()
            )
        )


    def set_callback_for_button_back(self) -> None:
        '''
        Inits callback for button "Back"
        Meaning of callback:
            hide current frame, show previous frame.


        Parameters:
        -----------
            Doesn't have
        '''
        self.frame.button_back.clicked.connect(
            lambda: (
                    self.frame.hide(),
                    self.main_window.layout.itemAt(self.frame.current_frame_index - 1).widget().show()
            )
        )


    def set_callback_for_button_ok(self) -> None:
        '''
        Inits callback for button "Ok"
        Meaning of callback:
            set response label for answer.

        Parameters:
        -----------
            Doesn't have
        '''
        text_callback = self.define_text_callback_for_ok_button
        self.frame.button_ok.clicked.connect(
            lambda: self.frame.response_label.setText(
                text_callback()
            )
        )


    def set_callback_for_button_results(self):
        '''
        Inits callback for button "Results"
        Meaning of callback:
            hide current frame, show frame with results.

        Parameters:
        -----------
            Doesn't have
        '''
        number_of_question_frames = self.main_window.layout.count()
        self.frame.button_results.clicked.connect(
            lambda: (
                self.count_correct_answers(number_of_question_frames = number_of_question_frames),
                self.frame.hide(),
                self.create_results_frame()
            )
        )

    def set_callback_for_button_close(self):
        self.frame.button_close.clicked.connect(self.main_window.close)

    
    def create_results_frame(self):
        result_frame = ResultsFrame(self.main_window.last_frame_index + 1, self.main_window)
        self.main_window.layout.addWidget(result_frame)
    

    def define_text_callback_for_ok_button(self) -> str:
        '''
        Returns response label text depending on information if user answer is correct
        or is filled.

        Parameters:
        -----------
            Doesn't have
        '''
        match self.is_user_translation_correct(self.frame, answer = self.answer):
            case True:
                return "Odpowiedź jest poprawna"
            case False:
                return "Odpowiedź nie jest poprawna"
            case None:
                return "Pole jest nieuzupełnione"

    
    def count_correct_answers(self, number_of_question_frames) -> None:
        '''
        Returns number of correct answers

        Parameters:
        -----------
            Doesn't have
        '''
        
        number_of_correct_answers = 1
        for frame_index in range(number_of_question_frames):
            question_frame: QuestionFrame = self.main_window.layout.itemAt(frame_index).widget()
            if question_frame.is_answer_correct:
                number_of_correct_answers += 1
        self.main_window.number_of_correct_answers = number_of_correct_answers
    

    def is_user_translation_correct(self, frame: QuestionFrame,
                                          answer: str) -> bool:
        '''
        Checks user translation with original word
        from vocabulary.
        '''
        user_answer = frame.input_line.text()
        if user_answer == answer:
            self.frame.is_answer_correct = True
            return True
        if not user_answer:
            return None
        return False


def main() -> None:
    app = QtWidgets.QApplication()
    window = MainWindow()
    window.run()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
