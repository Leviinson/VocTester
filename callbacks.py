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
    def __init__(self, main_window,
                       frame,
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
                    self.main_window.layout.itemAt(self.frame.current_frame_index + 1).widget().show(),
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
        self.frame.button_ok.clicked.connect(
            lambda: self.frame.response_label.setText(
                self.define_text_callback_for_ok_button(),
            )
        )

    
    def define_text_callback_for_ok_button(self) -> str:
        '''
        Returns response label text depending on information if user answer is correct
        or is filled.
        Inits boolean value for frame class variable: self.frame.is_answer_correct

        Parameters:
        -----------
            Doesn't have
        '''
        is_answer_correct = self.is_user_translation_correct(self.frame, self.answer)
        match is_answer_correct:
            case True:
                self.frame.is_answer_correct = True
                return "Odpowiedź jest poprawna"
            case False:
                self.frame.is_answer_correct = False
                return "Odpowiedź nie jest poprawna"
            case _:
                self.frame.is_answer_correct = False
                return "Pole jest nieuzupełnione"

    
    def is_user_translation_correct(self, frame,
                                          answer: str) -> bool:
        '''
        Checks user translation with original word
        from vocabulary.
        '''
        user_answer = frame.input_line.text()
        if user_answer == answer:
            return True
        if not user_answer:
            return None
        return False


    def set_callback_for_button_results(self):
        '''
        Inits callback for button "Results"
        Meaning of callback:
            hide current frame, show frame with results.

        Parameters:
        -----------
            Doesn't have
        '''
        self.frame.button_results.clicked.connect(
            lambda: (
                self.frame.hide(),
                self.main_window.results_frame.results_label.setText(
                    "Ilość poprawnych odpowiedzi: %s z %s" % (self.get_number_of_correct_answers(),
                                                              self.main_window.number_of_question_frames)),
                self.main_window.results_frame.show()
            )
        )


    def set_callback_for_button_close(self):
        self.frame.button_close.clicked.connect(self.main_window.close)

    
    def get_number_of_correct_answers(self) -> None:
        '''
        Returns number of correct answers

        Parameters:
        -----------
            Doesn't have
        '''
        number_of_correct_answers = 0 
        for frame_index in range(self.main_window.number_of_question_frames):
            question_frame = self.main_window.layout.itemAt(frame_index).widget()
            if question_frame.is_answer_correct:
                number_of_correct_answers += 1
        return number_of_correct_answers
