import os
import sys
import json
import random
import logging
from typing import Dict, List
from dataclasses import dataclass

from PySide6 import QtWidgets

from frames import (QuestionFrame,
                    ResultsFrame)


@dataclass
class SequenceIndexes:
    def __init__(self, list) -> None:
        self.list = list
        self.init_indexes()
    
    def init_indexes(self):
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
        self.number_of_question_frames = 0
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

        vocabulary = self.get_vocabulary(language = 'pl')
        random_sequence_of_question = random.sample(
                                                    range(len(vocabulary)),
                                                    len(vocabulary)
                                                    )
        sequence_entry_points = SequenceIndexes(random_sequence_of_question)
        self.last_frame_index = sequence_entry_points.stop_index
        self._create_frames_by_words_in_vocabulary(random_sequence_of_question = random_sequence_of_question,
                                                   vocabulary = vocabulary,
                                                   sequence_entry_points = sequence_entry_points)
    

    def get_vocabulary(self, language: str) -> List:
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

    
    def _create_question_frame(self, current_frame_index,
                                     question: str,
                                     answer: str,
                                     is_first: bool = False,
                                     is_last: bool = False) -> None:
        '''
        '''
        frame = QuestionFrame(question = question, answer = answer,
                              is_first = is_first, is_last = is_last,
                              currect_frame_index = current_frame_index,
                              main_window = self)
        self.layout.addWidget(frame)
        frame.hide()

    
    def _create_results_frame(self):
        self.results_frame = ResultsFrame(self.last_frame_index + 1, self)
        self.results_frame.hide()
        self.layout.addWidget(self.results_frame)

    
    def _create_frames_by_words_in_vocabulary(self, random_sequence_of_question: List,
                                                    vocabulary: Dict,
                                                    sequence_entry_points: SequenceIndexes):
        '''
        Extracts foreign word, its translation from vocabulary.
        Creates a new frame based on its index.
        '''
        for frame_index, random_question_index in enumerate(random_sequence_of_question):
            
            question = vocabulary[random_question_index]['foreign_word']
            answer = vocabulary[random_question_index]['translation']
            match frame_index:
                case sequence_entry_points.start_index:
                    self._create_question_frame(question = question,
                                                answer = answer,
                                                is_first = True,
                                                current_frame_index = frame_index)
                    self.layout.itemAt(sequence_entry_points.start_index).widget().show()

                case sequence_entry_points.stop_index:
                    self._create_question_frame(question = question,
                                                answer = answer,
                                                is_last = True,
                                                current_frame_index = frame_index)

                case _:
                    self._create_question_frame(question = question,
                                                answer = answer,
                                                current_frame_index = frame_index)
            self.number_of_question_frames += 1
        self._create_results_frame()


def main() -> None:
    app = QtWidgets.QApplication()
    window = MainWindow()
    window.run()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
