from PySide6 import (QtWidgets,
                     QtCore)

from callbacks import Callbacker


class QuestionFrame(QtWidgets.QFrame):
    '''
    Class, that represents 
    separate question frame.

    Attributes:
    -----------
        is_first: bool
            represents boolean value, if parent frame is first question
            used only for the correct location of the "OK" and "Next" buttons

        is_last: bool
            represents boolean value, if parent frame is last question
            used only for the correct location of the "Back", "OK" and "Results" buttons

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

        init_correctness_label(self):
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
    def __init__(self, main_window, question: str,
                       answer: str,
                       currect_frame_index: int,
                       is_first: bool = False,
                       is_last: bool = False,
                       is_results_frame: bool = False) -> None:
        super().__init__()
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


    def init_variables(self, is_first: bool,
                             is_last: bool,
                             current_frame_index: int,
                             question: str, answer: str):
        '''
        Inits passed variables
        to class instance.

        Parameters:
        -----------
            is_first: bool
                represents boolean value, if parent frame is first question
                used only for the correct location of the "OK" and "Next" buttons
    
            is_last: bool
                represents boolean value, if parent frame is last question
                used only for the correct location of the "Back", "OK" and "Results" buttons

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
        self.layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(self)

    
    def init_frame_widgets(self):
        '''
        Inits widgets for current frame instance.

        Parameters:
        -----------
            Doesn't have
        '''
        self.init_question_label()
        self.init_input_line()
        self.init_correctness_label()
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


    def init_correctness_label(self):
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
        self.nav_menu.addWidget(self.button_back,  alignment = QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignLeft)

    
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
                       main_window) -> None:
        '''
        Parameters:
        -----------
            current_frame_index: int
                index for current instance of frame

            main_window: MainWindow
                represents link to main window
        '''
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
        '''
        Inits widgets for current frame instance.

        Parameters:
        -----------
            Doesn't have
        '''
        self.init_results_label()
        self.init_nav_menu()

    
    def init_results_label(self):
        '''
        Creates label, that contains results message:
        pins current frame instance as parent for this widget
        by default.

        Parameters:
        -----------
            Doesn't have
        '''
        self.results_label = QtWidgets.QLabel(parent = self)
        self.results_label.setObjectName('results_label')
        self.layout.addWidget(self.results_label, alignment = QtCore.Qt.AlignmentFlag.AlignCenter)

    
    def init_nav_menu(self):
        '''
        Calls initializations for all necessary
        navigation menu buttons.

        Parameters:
        -----------
            Doesn't have

        '''
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
