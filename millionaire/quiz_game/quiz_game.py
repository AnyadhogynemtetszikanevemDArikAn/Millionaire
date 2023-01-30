import os
import random
import json
import time
from sty import Style, RgbFg, fg, bg, rs
import millionaire.menu.menu as menu
import millionaire.util.util as util
import millionaire.menu.helpers as helpers
operating_system = os.name
fg.purple = Style(RgbFg(148, 0, 211))
fg.orange = Style(RgbFg(255, 150, 50))
fg.green = Style(RgbFg(0, 255, 0))
bg.orange = bg(255, 150, 50)
languages = util.available_languages
language_dictionary = util.language_dictionary
table_length = 113
game_levels = 15
screen_distance = 60


def play():
    global game_language, question_lines_easy, question_lines_medium, question_lines_hard
    game_language = util.game_language
    global question_topics
    question_topics = util.question_topics
    global question_difficulty
    question_difficulty = util.question_difficulty
    global help_types
    help_types = {"halving": True, "telephone": True, "audience": True}
    question_lines = []
    question_lines_easy = []
    question_lines_medium = []
    question_lines_hard = []
    if question_topics == util.Topics.ALL.name:
        for topic in util.Topics:
            if topic.name != util.Topics.ALL.name and question_difficulty != util.Difficulty.ALL.name:
                for level in util.Difficulty:
                    if question_difficulty == level.name:
                        for line in util.open_file(str(level.name).lower(), "r", ";",
                                                   "/text_files/topics/" + str(game_language).lower() + "/" + str(topic.name).lower() + "/" + str(level.name).lower() + "/"):
                            question_lines.append(line)
            else:
                if topic.name != util.Topics.ALL.name:
                    for line in util.open_file(str(util.Difficulty.EASY.name).lower(), "r", ";",
                                               "/text_files/topics/" + str(game_language).lower() + "/" + str(topic.name).lower() + "/" + str(util.Difficulty.EASY.name).lower() + "/"):
                        question_lines_easy.append(line)
                    for line in util.open_file(str(util.Difficulty.MEDIUM.name).lower(), "r", ";",
                                               "/text_files/topics/" + str(game_language).lower() + "/" + str(topic.name).lower() + "/" + str(util.Difficulty.MEDIUM.name).lower() + "/"):
                        question_lines_medium.append(line)
                    for line in util.open_file(str(util.Difficulty.HARD.name).lower(), "r", ";",
                                               "/text_files/topics/" + str(game_language).lower() + "/" + str(topic.name).lower() + "/" + str(util.Difficulty.HARD.name).lower() + "/"):
                        question_lines_hard.append(line)
    else:
        for level in util.Difficulty:
            if question_difficulty == level.name and level.name != util.Difficulty.ALL.name:
                for line in util.open_file(str(level.name).lower(), "r", ";",
                                           "/text_files/topics/" + str(game_language).lower() + "/" + str(question_topics).lower() + "/" + str(level.name).lower() + "/"):
                    question_lines.append(line)
            else:
                if level.name != util.Difficulty.ALL.name:
                    for line in util.open_file(str(util.Difficulty(level).name).lower(), "r", ";",
                                               "/text_files/topics/" + str(game_language).lower() + "/" + str(question_topics).lower() + "/" + str(level.name).lower() + "/"):
                        if level.name == util.Difficulty.EASY.name:
                            question_lines_easy.append(line)
                        if level.name == util.Difficulty.MEDIUM.name:
                            question_lines_medium.append(line)
                        if level.name == util.Difficulty.HARD.name:
                            question_lines_hard.append(line)
    random.shuffle(question_lines)
    random.shuffle(question_lines_easy)
    random.shuffle(question_lines_medium)
    random.shuffle(question_lines_hard)
    player_name = input(" "*screen_distance + language_dictionary[game_language].quiz.player_name_prompt)
    score = 0
    util.clear_screen()
    if game_language == util.Language.ENGLISH:
        util.play_sound("start", 0)
    show_game_structure()
    for i in range(game_levels):
        if question_difficulty == util.Difficulty.ALL.name:
            if i < 5:
                question_lines = question_lines_easy
            elif i < 10:
                question_lines = question_lines_medium
            else:
                question_lines = question_lines_hard
        question = question_lines[i][0]
        answers = {"a": question_lines[i][1], "b": question_lines[i][2], "c": question_lines[i][3],
                   "d": question_lines[i][4]}
        answer_list = list(answers.values())
        random.shuffle(answer_list)
        shuffled_answers = dict(zip(answers, answer_list))
        print_quiz_table(question, shuffled_answers, game_level=i)
        play_music(i)
        if game_language == util.Language.HUNGARIAN.name:
            print("\n\n   " + fg.grey + language_dictionary[game_language].quiz.select_answer + fg.rs)
            answer = handle_user_input(question, shuffled_answers, i)
            if answer == "esc":
                quit_game(i, player_name, question_topics)
                return
        else:
            answer = safe_input(
                fg.grey + language_dictionary[game_language].quiz.select_answer + fg.rs,
                ["a", "b", "c", "d", "h", "t"])
        correct_answer_key = get_dictionary_key_by_value(shuffled_answers, question_lines[i][1])
        correct_answer_value = question_lines[i][1]
        util.stop_sound()
        while answer not in list(answers.keys()):
            if answer == "t":
                util.clear_screen()
                print_quiz_table(question, shuffled_answers, game_level=i)
                if util.game_language == util.Language.HUNGARIAN.name:
                    util.play_sound("music_off", 0)
                if game_language == util.Language.HUNGARIAN.name:
                    print("\n\n  ", fg.grey + language_dictionary[game_language].quiz.select_answer_out + fg.rs)
                    answer = handle_user_input(question, shuffled_answers, i, final_color="blue", out_of_game=True)
                else:
                    answer = safe_input(
                        fg.grey + language_dictionary[game_language].quiz.select_answer_out + fg.rs,
                        ["a", "b", "c", "d"])
                    util.clear_screen()
                    print_quiz_table(question, shuffled_answers, answer, "blue", "", game_level=i)
                    util.play_sound("marked", 0)
                    time.sleep(2)
                is_correct = check_answer(answer, correct_answer_key)
                if is_correct:
                    util.clear_screen()
                    print_quiz_table(question, shuffled_answers, answer, "green", "", game_level=i)
                    time.sleep(2)
                    if i > 0:
                        print_prizes_with_quizmaster(level=i-1)
                    else:
                        print_prizes_with_quizmaster(level=i, nullprize=True)
                    print(fg.orange + "\n   " + language_dictionary[game_language].quiz.correct_answer_out + fg.rs)
                    util.play_sound("time_end_horn", 0)
                    time.sleep(1)
                else:
                    util.play_sound("bad_answer", 0)
                    util.clear_screen()
                    print_quiz_table(question, shuffled_answers, answer, "blue", correct_answer=correct_answer_key, game_level=i)
                    time.sleep(2)
                    if i > 9:
                        print_prizes_with_quizmaster(9)
                    elif i > 4:
                        print_prizes_with_quizmaster(4)
                    else:
                        print_prizes_with_quizmaster(0, nullprize=True)
                    print(fg.red + "\n   " + language_dictionary[game_language].quiz.incorrect_answer + fg.rs)
                    if util.game_language == util.Language.HUNGARIAN.name:
                        util.play_sound("so_sorry", 0)
                    time.sleep(1)
                quit_game(i, player_name, question_topics)
                util.clear_screen()
                return
            if answer == "h" or "s":
                if list(help_types.values()).count(True) == len(
                        help_types) and game_language == util.Language.HUNGARIAN.name:
                    util.play_sound("still_have_all_helps", 0, timer=True)
                    play_music(i)
                util.clear_screen()
                print_quiz_table(question, shuffled_answers, game_level=i)
                help_functions = {"halving": halving, "telephone": telephone_help, "audience": audience_help}
                chosen_help_type = safe_input("\n\n  " + fg.grey+language_dictionary[game_language].quiz.help_selection+fg.rs,
                                              [language_dictionary[game_language].quiz.audience_help[0].lower(),
                                               language_dictionary[game_language].quiz.telephone_help[0].lower(),
                                               language_dictionary[game_language].quiz.halving_help[0].lower()])
                chosen_help = ""
                if chosen_help_type.lower() == "k":
                    chosen_help = "a"
                if chosen_help_type.lower() == "f":
                    chosen_help = "h"
                if chosen_help_type.lower() == "t":
                    chosen_help = "t"
                for x in range(len(help_types)):
                    if chosen_help == list(help_types)[x][0]:
                        if help_types[list(help_types)[x]]:
                            if list(help_types)[x] == "halving":
                                shuffled_answers = list(help_functions.values())[x](question, shuffled_answers,
                                                                                    correct_answer_value)
                                for a in range(len(answer_list)):
                                    answer_list[a] = list(shuffled_answers.values())[a]
                                print_quiz_table(question, shuffled_answers, game_level=i)
                                time.sleep(2)
                            elif list(help_types)[x] == "audience":
                                audience_help(question, shuffled_answers, correct_answer_value, game_level=i)
                            else:
                                list(help_functions.values())[x](question, shuffled_answers, correct_answer_value)
                            help_types[list(help_types)[x]] = False
                            break
                        else:
                            if list(help_types)[x] == "audience":
                                print("  " + language_dictionary[game_language].quiz.audience_help_disabled)
                            elif list(help_types)[x] == "halving":
                                print("  " + language_dictionary[game_language].quiz.halving_help_disabled)
                            else:
                                print("  " + language_dictionary[game_language].quiz.phone_help_disabled)
                play_music(i)
                if game_language == util.Language.HUNGARIAN.name:
                    print("\n\n  ", fg.grey + language_dictionary[game_language].quiz.select_answer + fg.rs)
                    answer = handle_user_input(question, shuffled_answers, i)
                else:
                    answer = safe_input(
                        fg.grey + language_dictionary[game_language].quiz.select_answer + fg.rs,
                        ["a", "b", "c", "d", "h", "t"])
                time.sleep(2)
        util.clear_screen()
        if game_language == util.Language.ENGLISH:
            print_quiz_table(question, shuffled_answers, answer, "orange", game_level=i)
            util.play_sound("marked", 0)
            time.sleep(2)
        is_correct = check_answer(answer, correct_answer_key)
        if is_correct:
            score += 1
            if i < 14:
                util.play_sound("correct_answer", 0)
                util.clear_screen()
                print_quiz_table(question, shuffled_answers, answer, "green", game_level=i)
                time.sleep(2)
                util.clear_screen()
                if len(question) % 2 == 0:
                    question = question + " "
                if i == 4:
                    print("\n" + " " * 20 + fg.yellow + language_dictionary[
                        game_language].quiz.guaranteed_prize + show_prize(i) + fg.rs)
                    util.play_sound("won_hundred_bucks", 0)
                    print_prizes_with_quizmaster(i)
                    time.sleep(7)
                elif i == 9:
                    print("\n" + " " * 20 + fg.yellow + language_dictionary[
                        game_language].quiz.guaranteed_prize + show_prize(i) + fg.rs)
                    if util.game_language == util.Language.HUNGARIAN.name:
                        util.play_sound("now_comes_hard_part", 0)
                    print_prizes_with_quizmaster(i)
                    time.sleep(3)
                else:
                    print_prizes_with_quizmaster(i)
                    time.sleep(2)
            else:
                if util.game_language == util.Language.HUNGARIAN.name:
                    util.play_sound("after_marking", 0)
                    time.sleep(4)
                    util.play_sound("great_logic", 0)
                    print_prizes_with_quizmaster(i)
                time.sleep(1)
                util.clear_screen()
                print("\n" + " " * 20 + fg.purple + language_dictionary[game_language].quiz.won_prize + show_prize(
                    i) + " !" + fg.rs)
                util.play_sound("winning_theme", 0)
                time.sleep(35)
                quit_game(i, player_name, question_topics)
        else:
            util.play_sound("bad_answer", 0)
            util.clear_screen()
            print_quiz_table(question, shuffled_answers, answer, "orange", correct_answer=correct_answer_key, game_level=i)
            time.sleep(2)
            if game_language == util.Language.HUNGARIAN.name:
                util.play_sound("so_sorry", 0)
                time.sleep(1)
            util.clear_screen()
            if i > 9:
                print_prizes_with_quizmaster(9)
            elif i > 4:
                print_prizes_with_quizmaster(4)
            else:
                print_prizes_with_quizmaster(0, nullprize=True)
            print("\n   " + fg.orange + language_dictionary[game_language].quiz.incorrect_answer + fg.rs)
            quit_game(i, player_name, question_topics)
            util.clear_screen()

            return
        util.clear_screen()
    quit_game(score, player_name, question_topics)

    return


def fastest_finger_first():
    global game_language, question_lines_easy, question_lines_medium, question_lines_hard
    game_language = util.game_language
    global question_topics
    question_topics = util.question_topics
    global question_difficulty
    question_difficulty = util.question_difficulty
    global help_types
    help_types = {"halving": True, "telephone": True, "audience": True}
    question_lines = []
    question_lines_easy = []
    question_lines_medium = []
    question_lines_hard = []
    for line in util.open_file("questions", "r", ";",
                               "/text_files/fastest_fingers_first/" + str(game_language).lower() + "/"):
        question_lines.append(line)
    random.shuffle(question_lines)
    player_name = input(" "*screen_distance + language_dictionary[game_language].quiz.player_name_prompt)
    score = 0
    total_answer = ""
    util.clear_screen()
    if game_language == util.Language.ENGLISH:
        util.play_sound("start", 0)
    question = question_lines[0][0]
    answers = {"a": question_lines[0][1], "b": question_lines[0][2], "c": question_lines[0][3],
               "d": question_lines[0][4]}
    answer_list = list(answers.values())
    random.shuffle(answer_list)
    #shuffled_answers = dict(zip(answers, answer_list))
    shuffled_answers = answers
    print_quizmaster()
    if game_language == util.Language.HUNGARIAN.name:
        util.play_sound("lets_look_at_the_fastest_fingers_question", 0)
        time.sleep(2)
    start = time.time()
    util.clear_screen()
    print_fastest_fingers_table(question, shuffled_answers, game_level=0,quizmaster=True,prizes=False)
    util.play_sound("fastest_fingers_first", 0)
    print("\n\n   " + fg.grey + language_dictionary[game_language].quiz.select_answer_out + fg.rs)
    for i in range(4):
        answer = handle_fastest_fingers_first_input(question, shuffled_answers, 0, total_answer)
        if answer == "esc":
            quit_game(0, player_name, question_topics)
            return
        total_answer += answer
    correct_answer_keys =question_lines[0][5]
    util.clear_screen()
    end = time.time()
    is_correct = check_answer(total_answer, correct_answer_keys)
    util.stop_sound()
    print_fastest_fingers_table(question, answers, total_answer, "orange", game_level=0, quizmaster=True, prizes=False)
    if game_language == util.Language.HUNGARIAN.name:
        if os.path.isfile("./data/sound_files/hungarian/" + correct_answer_keys + ".wav"):
            util.play_sound(correct_answer_keys, 0)
        time.sleep(1)
        util.play_sound("lets_see_who_is_correct", 0)
    time.sleep(2)
    if is_correct:
        util.play_sound("fastest_fingers_correct", 0)
        util.clear_screen()
        if len(question) % 2 == 0:
            question = question + " "
        print_prizes_with_quizmaster(0,False, special_text = "♦ " + player_name + " : " + str(end-start)[:5] +" ♦", bg_color=bg.green)
        time.sleep(2)
        util.play_sound("fastest_fingers_win", 0)
    else:
        util.play_sound("fastest_fingers_bad", 0)
        util.clear_screen()
        print("\n   " + fg.orange + language_dictionary[game_language].quiz.incorrect_answer + fg.rs)
        quit_game(score, player_name, question_topics)
        return

    quit_game(score, player_name, question_topics)

    return


def safe_input(input_text: str, allowed_list_of_letters: list) -> str:
    answer = input(input_text)
    if answer not in allowed_list_of_letters:
        print("  " + language_dictionary[game_language].quiz.allowed_letters_error + ' '.join(allowed_list_of_letters) +
              language_dictionary[game_language].quiz.allowed)
    while answer not in allowed_list_of_letters:
        answer = input(input_text)
    time.sleep(1)

    return answer


def get_dictionary_key_by_value(dictionary: {}, value: str) -> str:
    for choice, answerValue in dict.items(dictionary):
        if answerValue == value:
            return choice


def check_answer(answer: str, correct_answer: str) -> bool:
    return answer == correct_answer


def show_prize(round_number: int) -> str:
    prizes = util.open_file("prizes_" + str(game_language).lower(), "r")
    return prizes[round_number][0]


def halving(question: str, answers: {}, correct_answer: str) -> dict:
    if util.game_language == util.Language.HUNGARIAN.name:
        util.play_sound("lets_take_two", 0)
    util.clear_screen()
    time.sleep(2)
    util.play_sound("halving", 0)
    halved_answers = calculate_halved_answers(answers, correct_answer)
    return halved_answers


def calculate_halved_answers(answers: {}, correct_answer: str) -> {}:
    halved_answers = {}
    correct_value = get_dictionary_key_by_value(answers, correct_answer)
    second_answer = random.choice([x for x in answers if x != correct_value])
    for i in answers:
        if answers[i] == correct_answer:
            halved_answers[i] = answers[i]
        elif i == second_answer:
            halved_answers[i] = answers[second_answer]
        else:
            halved_answers[i] = ""

    return halved_answers


def get_chances(answers: {}, correct_value: str) -> dict:
    answers_list = list(answers.keys())
    chances_dict = {}
    correct_answer = get_dictionary_key_by_value(answers, correct_value)
    chances_dict[correct_answer] = random.randrange(40, 89)
    answers_list.pop(answers_list.index(correct_answer))
    if list(answers.values()).count("") == 2:
        for k in range(len(list(answers.keys()))-1):
            if list(answers.values())[k] != "":
                chances_dict[answers_list[k]] = 100 - sum(chances_dict.values())
            else:
                chances_dict[answers_list[k]] = 0
        return chances_dict

    for k in range(len(answers_list)):
        if k == len(answers_list) - 1:
            chances_dict[answers_list[k]] = 100 - sum(chances_dict.values())
        else:
            chances_dict[answers_list[k]] = random.randrange(0, 100 - sum(chances_dict.values()))

    return chances_dict


def write_content_to_file(filename: str, content: {}):
    if os.path.isfile(filename):
        with open(filename, 'r+') as file:
            file_data = json.load(file)
            file_data.append(content)
            file.seek(0)
            json.dump(file_data, file)

    else:
        with open(filename, "w", encoding="UTF-8") as outfile:
            json.dump([content], outfile)


def divide_question(question: str) -> list:
    question_parts = []
    basic_question_length = 109
    if len(question) >= basic_question_length:
        for i in range(int(len(question) / basic_question_length) + 1):
            index = basic_question_length * i
            question_parts.append(question[index:basic_question_length * (i + 1)])

    return question_parts


def divide_answer(answer: str, number_of_parts: float) -> list:
    answer_parts = []
    basic_question_length = 109
    basic_answer_length = int((basic_question_length / 2) - 5)
    for i in range(int(number_of_parts) + 1):
        if len(answer[i:basic_answer_length * (i + 1)]) > 0:
            index = basic_answer_length * i
            answer_parts.append(answer[index:basic_answer_length * (i + 1)])
        else:
            answer_parts.append("")
    return answer_parts


def print_quiz_table(question: str, answers_: {}, selected="", color="", correct_answer="", game_level=0, quizmaster=True, prizes=True):
    global table_length
    basic_question_length = 109
    answer_values = list(answers_.values())
    longest_string = list(sorted(answers_.values(), key=len))[-1]
    spaces_after_question = table_length - len(question) - 3
    if len(question) > basic_question_length:
        question_list = divide_question(question)
        question = ""
        for i in range(len(question_list)):
            if i < len(question_list) - 1:
                spaces_after_question = table_length - (len(question_list[i])) - 4
                question = question + question_list[i] + spaces_after_question * " " + "    ►\n ◄  "
            else:
                question = question + question_list[i]
                spaces_after_question = table_length - (len(question_list[i])) - 3
        number_of_spaces = int((table_length / 2) - 6)
    else:
        number_of_spaces = int((table_length / 2) - 6)
    if quizmaster:
        if prizes:
            print_quizmaster_with_prizes(game_level)
        else:
            print_quizmaster()
    print("  /" + "‾" * (table_length) + "\\")
    print(" ◄  " + question + " " * spaces_after_question + "   ►")
    print("  \\" + "_" * (table_length) + "/")
    print("\n")
    if len(longest_string) > number_of_spaces:
        print("   " + "_" * (number_of_spaces + 3) + "     " + "_" * (number_of_spaces + 5))
        number_of_spaces = number_of_spaces + 7
        number_of_parts = len(longest_string) / number_of_spaces
        if type(number_of_parts) == float:
            number_of_parts += 1
        answer_list_a = divide_answer(answer_values[0], number_of_parts)
        answer_list_b = divide_answer(answer_values[1], number_of_parts)
        answer_list_c = divide_answer(answer_values[2], number_of_parts)
        answer_list_d = divide_answer(answer_values[3], number_of_parts)
        answers_lists = [answer_list_a, answer_list_b, answer_list_c, answer_list_d]
        longest_string_divided = int(number_of_parts)
        answer = ""
        index = 0
        for i in range(4):
            if i == 0 or i == 2:
                for j in range(longest_string_divided + 1):
                    if j == 0:
                        first_string = " " +list(answers_.items())[i][j].upper() + ": " + answers_lists[index][j]
                        second_string = " " +list(answers_.items())[i + 1][j].upper() + ": " + answers_lists[index + 1][j]
                    else:
                        first_string = " " * 3 + answers_lists[index][j]
                        second_string = " " * 3 + answers_lists[index + 1][j]
                    first_spaces = number_of_spaces - len(first_string) - 4
                    second_spaces = number_of_spaces - len(second_string) - 4
                    first_string = first_string + " " * first_spaces
                    second_string = second_string + " " * second_spaces
                    if selected != "":
                        for answer_ in answers_:
                            if correct_answer != "" and correct_answer == list(answers_.keys())[index]:
                                first_string = bg.green + fg.black + first_string + fg.rs + bg.rs
                            if correct_answer != "" and correct_answer == list(answers_.keys())[index + 1]:
                                second_string = bg.green + fg.black + second_string + fg.rs + bg.rs
                            if list(answers_.keys())[index] == selected:
                                if color == "orange":
                                    first_string = bg.orange + fg.black + first_string + fg.rs + bg.rs
                                if color == "green":
                                    first_string = bg.green + fg.black + first_string + fg.rs + bg.rs
                                if color == "blue":
                                    first_string = bg.blue + fg.black + first_string + fg.rs + bg.rs
                                if color == "li_grey":
                                    first_string = bg.li_grey + fg.black + first_string + fg.rs + bg.rs
                            if list(answers_.keys())[index + 1] == selected :
                                if color == "orange":
                                    second_string = bg.orange + fg.black + second_string + fg.rs + bg.rs
                                if color == "green":
                                    second_string = bg.green + fg.black + second_string + fg.rs + bg.rs
                                if color == "blue":
                                    second_string = bg.blue + fg.black + second_string + fg.rs + bg.rs
                                if color == "li_grey":
                                    second_string = bg.li_grey + fg.black + second_string + fg.rs + bg.rs
                    answer = answer + " ◄|" + first_string + "|►━◄|" + second_string + "  |►"
                    if j < longest_string_divided:
                        answer = answer + "\n"
            if i == 0:
                answer = answer + "\n" + "   " + "‾" * (number_of_spaces  - 4)  + "     " + "‾" * (number_of_spaces - 2) +\
                         "\n" + "   " +  "_" * (number_of_spaces  - 4)  + "     " + "_" * (number_of_spaces - 2) + "\n"
            index += 1
        print(answer)
        print("   "  + "‾" * (number_of_spaces -4) + "     " + "‾" * (number_of_spaces-2))
    else:
        print("   " + "_" * (number_of_spaces + 4) + "     " + "_" * (number_of_spaces + 4))
        if selected != "":
            index = 0
            for i in answers_:
                if i == selected:
                    if color == "orange":
                        answer_values[list(answers_).index(i)] = bg.orange + fg.black + " " +list(answers_.items())[index][
                            0].upper() + ": " + answers_[i] + " " * (number_of_spaces - len(
                            list(answers_.items())[index][1])) + fg.rs + bg.rs
                    if color == "green":
                        answer_values[list(answers_).index(i)] = bg.green + fg.black + " " + list(answers_.items())[index][
                            0].upper() + ": " + answers_[i] + " " * (number_of_spaces - len(
                            list(answers_.items())[index][1])) + fg.rs + bg.rs
                    if color == "blue":
                        answer_values[list(answers_).index(i)] = bg.blue + fg.black + " " + list(answers_.items())[index][
                            0].upper() + ": " + answers_[i] + " " * (number_of_spaces - len(
                            list(answers_.items())[index][1])) + fg.rs + bg.rs
                    if color == "li_grey":
                        answer_values[list(answers_).index(i)] = bg.li_grey + fg.black + " " + list(answers_.items())[index][
                            0].upper() + ": " + answers_[i] + " " * (number_of_spaces - len(
                            list(answers_.items())[index][1])) + fg.rs + bg.rs
                elif correct_answer != "" and i == correct_answer:
                    answer_values[list(answers_).index(i)] = bg.green + fg.black + " " +  list(answers_.items())[index][
                        0].upper() + ": " + answers_[i] + " " * (number_of_spaces - len(
                        list(answers_.items())[index][1])) + fg.rs + bg.rs
                else:
                    answer_values[list(answers_).index(i)] = " " + list(answers_.items())[index][0].upper() + ": " + answers_[
                        i] + " " * (number_of_spaces - len(list(answers_.items())[index][1]))
                index += 1
        else:
            for i in range(len(answers_)):
                answer_values[i] = " " + list(answers_.items())[i][0].upper() + ": " + answer_values[i] + " " * (
                            number_of_spaces - len(list(answers_.items())[i][1]))

        print(" ◄|" + answer_values[0] + "|►━◄|" + answer_values[1] + "|►")
        print("   " + "‾" * (number_of_spaces  + 4) + "     " + "‾" * (number_of_spaces + 4))
        print("   " + "_" * (number_of_spaces  + 4) + "     " + "_" * (number_of_spaces + 4))
        print(" ◄|" + answer_values[2] + "|►━◄|" + answer_values[3] + "|►")
        print("   "  + "‾" * (number_of_spaces + 4) + "     " + "‾" * (number_of_spaces+4))


def print_fastest_fingers_table(question: str, answers_: {}, selected="", color="", correct_answer="", game_level=0, quizmaster=True, prizes=True):
    global table_length
    basic_question_length = 109
    answer_values = list(answers_.values())
    longest_string = list(sorted(answers_.values(), key=len))[-1]
    spaces_after_question = table_length - len(question) - 3
    if len(question) > basic_question_length:
        question_list = divide_question(question)
        question = ""
        for i in range(len(question_list)):
            if i < len(question_list) - 1:
                spaces_after_question = table_length - (len(question_list[i])) - 4
                question = question + question_list[i] + spaces_after_question * " " + "    ►\n ◄  "
            else:
                question = question + question_list[i]
                spaces_after_question = table_length - (len(question_list[i])) - 3
        number_of_spaces = int((table_length / 2) - 6)
    else:
        number_of_spaces = int((table_length / 2) - 6)
    if quizmaster:
        if prizes:
            print_quizmaster_with_prizes(game_level)
        else:
            print_quizmaster()
    print("  /" + "‾" * (table_length) + "\\")
    print(" ◄  " + question + " " * spaces_after_question + "   ►")
    print("  \\" + "_" * (table_length) + "/")
    print("\n")
    if len(longest_string) > number_of_spaces:
        print("   " + "_" * (number_of_spaces + 3) + "     " + "_" * (number_of_spaces + 5))
        number_of_spaces = number_of_spaces + 7
        number_of_parts = len(longest_string) / number_of_spaces
        if type(number_of_parts) == float:
            number_of_parts += 1
        answer_list_a = divide_answer(answer_values[0], number_of_parts)
        answer_list_b = divide_answer(answer_values[1], number_of_parts)
        answer_list_c = divide_answer(answer_values[2], number_of_parts)
        answer_list_d = divide_answer(answer_values[3], number_of_parts)
        answers_lists = [answer_list_a, answer_list_b, answer_list_c, answer_list_d]
        longest_string_divided = int(number_of_parts)
        answer = ""
        index = 0
        for i in range(4):
            if i == 0 or i == 2:
                for j in range(longest_string_divided + 1):
                    if j == 0:
                        first_string = " " +list(answers_.items())[i][j].upper() + ": " + answers_lists[index][j]
                        second_string = " " +list(answers_.items())[i + 1][j].upper() + ": " + answers_lists[index + 1][j]
                    else:
                        first_string = " " * 3 + answers_lists[index][j]
                        second_string = " " * 3 + answers_lists[index + 1][j]
                    first_spaces = number_of_spaces - len(first_string) - 4
                    second_spaces = number_of_spaces - len(second_string) - 4
                    first_string = first_string + " " * first_spaces
                    second_string = second_string + " " * second_spaces
                    if selected != "":
                        for answer_ in answers_:
                            if correct_answer != "" and correct_answer == list(answers_.keys())[index]:
                                first_string = bg.green + fg.black + first_string + fg.rs + bg.rs
                            if correct_answer != "" and correct_answer == list(answers_.keys())[index + 1]:
                                second_string = bg.green + fg.black + second_string + fg.rs + bg.rs
                            if list(answers_.keys())[index] == selected or list(answers_.keys())[index] in selected:
                                if list(answers_.keys())[index] in selected:
                                    first_string = str(selected.index(list(answers_.items())[index][
                            0])+1) + ": " + first_string
                                if color == "orange":
                                    first_string = bg.orange + fg.black + first_string + fg.rs + bg.rs
                                if color == "green":
                                    first_string = bg.green + fg.black + first_string + fg.rs + bg.rs
                                if color == "blue":
                                    first_string = bg.blue + fg.black + first_string + fg.rs + bg.rs
                                if color == "li_grey":
                                    first_string = bg.li_grey + fg.black + first_string + fg.rs + bg.rs
                            if list(answers_.keys())[index + 1] == selected and list(answers_.keys())[index] in selected:
                                if list(answers_.keys())[index] in selected:
                                    second_string = str(selected.index(list(answers_.items())[index][
                            0])+1) + ": " + first_string
                                if color == "orange":
                                    second_string = bg.orange + fg.black + second_string + fg.rs + bg.rs
                                if color == "green":
                                    second_string = bg.green + fg.black + second_string + fg.rs + bg.rs
                                if color == "blue":
                                    second_string = bg.blue + fg.black + second_string + fg.rs + bg.rs
                                if color == "li_grey":
                                    second_string = bg.li_grey + fg.black + second_string + fg.rs + bg.rs
                    answer = answer + " ◄|" + first_string + "|►━◄|" + second_string + "  |►"
                    if j < longest_string_divided:
                        answer = answer + "\n"
            if i == 0:
                answer = answer + "\n" + "   " + "‾" * (number_of_spaces  - 4)  + "     " + "‾" * (number_of_spaces - 2) +\
                         "\n" + "   " +  "_" * (number_of_spaces  - 4)  + "     " + "_" * (number_of_spaces - 2) + "\n"
            index += 1
        print(answer)
        print("   "  + "‾" * (number_of_spaces -4) + "     " + "‾" * (number_of_spaces-2))
    else:
        print("   " + "_" * (number_of_spaces + 4) + "     " + "_" * (number_of_spaces + 4))
        if selected != "":
            index = 0
            for i in answers_:
                if i == selected or list(answers_.keys())[index] in selected:
                    if color == "orange":
                        answer_values[list(answers_).index(i)] = bg.orange + fg.black + " " + str(selected.index(list(answers_.items())[index][
                            0])+1) + ": " + answers_[i] + " " * (number_of_spaces - len(
                            list(answers_.items())[index][1])) + fg.rs + bg.rs
                    if color == "green":
                        answer_values[list(answers_).index(i)] = bg.green + fg.black + " " + str(selected.index(list(answers_.items())[index][
                            0])+1) + ": " + answers_[i] + " " * (number_of_spaces - len(
                            list(answers_.items())[index][1])) + fg.rs + bg.rs
                    if color == "blue":
                        answer_values[list(answers_).index(i)] = bg.blue + fg.black + " " + str(selected.index(list(answers_.items())[index][
                            0])+1) + ": " + answers_[i] + " " * (number_of_spaces - len(
                            list(answers_.items())[index][1])) + fg.rs + bg.rs
                    if color == "li_grey":
                        answer_values[list(answers_).index(i)] = bg.li_grey + fg.black + " " + str(selected.index(list(answers_.items())[index][
                            0])+1) + ": " + answers_[i] + " " * (number_of_spaces - len(
                            list(answers_.items())[index][1])) + fg.rs + bg.rs
                elif correct_answer != "" and i == correct_answer:
                    answer_values[list(answers_).index(i)] = bg.green + fg.black + " " + str(selected.index(list(answers_.items())[index][
                            0])+1) + ": " + answers_[i] + " " * (number_of_spaces - len(
                        list(answers_.items())[index][1])) + fg.rs + bg.rs
                else:
                    answer_values[list(answers_).index(i)] = " " + list(answers_.items())[index][0].upper() + ": " + \
                        answers_[i] + " " * (number_of_spaces - len(list(answers_.items())[index][1]))
                index += 1
        else:
            for i in range(len(answers_)):
                answer_values[i] = " " + list(answers_.items())[i][0].upper() + ": " + answer_values[i] + " " * (
                        number_of_spaces - len(list(answers_.items())[i][1]))

        print(" ◄|" + answer_values[0] + "|►━◄|" + answer_values[1] + "|►")
        print("   " + "‾" * (number_of_spaces  + 4) + "     " + "‾" * (number_of_spaces + 4))
        print("   " + "_" * (number_of_spaces  + 4) + "     " + "_" * (number_of_spaces + 4))
        print(" ◄|" + answer_values[2] + "|►━◄|" + answer_values[3] + "|►")
        print("   "  + "‾" * (number_of_spaces + 4) + "     " + "‾" * (number_of_spaces+4))


def print_quizmaster_with_prizes(level: int):
    prizes = util.open_file("prizes_" + str(game_language).lower(), "r")[::-1]
    prizes_ = util.open_file("prizes_" + str(game_language).lower(), "r")[::-1]
    index = 0
    len_al = 45
    helps = [" 50 : 50 ", "   \_] ", "   ☺ ☺ ☺   "]
    helps_ = [" 50 : 50 ", "   \_] ", "   ☺ ☺ ☺   "]
    i = 0
    for key, value in help_types.items():
        if not value:
            helps_[i] = fg.red + helps[i] + fg.rs
        i += 1
    help_length = len(helps[0] + helps[1] + helps[2])+2
    print(" " * 87 + " " + help_length* "_" )
    print(" " * 87 + "|" + (help_length-2)*" " +"  |")
    print(" " * 87 + "|" + helps_[0] + helps_[1] + helps_[2] +"  |")
    print(" " * 87+ "|" + help_length* "_" + "|")

    for line in util.open_file("quizmaster", "r", ";","/text_files/", strip=False):
        if index < len(prizes):
            missing_space = len_al-len(line[0])
            round_number = str(len(prizes)-index)
            if len(prizes) - index < 10:
                round_number = " " + round_number
            box_space = len(round_number + " ♦ " + prizes[index][0]) + 1
            if len(prizes) - index == level+1:
                prizes_[index][0] = bg.orange + fg.black + prizes[index][0] + fg.rs + bg.rs
            if len(prizes)-index <= level:
                if len(prizes)-index in [5,10,15]:
                    print(line[0] + " "*missing_space + "| " + round_number + " ♦ "  + prizes_[index][0] + fg.rs + " " * (help_length - box_space) + "|")
                else:
                    print(line[0] + " "*missing_space + "| " + round_number + " ♦ "  + fg.orange + prizes_[index][0] + fg.rs + " " * (help_length - box_space) + "|")
            else:
                if len(prizes)-index in [5,10,15]:
                    print(line[0] + " "*missing_space + "| " + round_number + "   " + prizes_[index][0] + " " * (help_length - box_space) + "|")
                else:
                    print(line[0] + " "*missing_space + "| " + round_number + "   " + fg.orange + prizes_[index][0]  + fg.rs +" " * (help_length - box_space) + "|")
        elif index == len(prizes):
            print(line[0] + " " * (missing_space+3) + help_length*"‾")
        else:
            print(line[0])
        index += 1


def print_quizmaster():
    for line in util.open_file("quizmaster", "r", ";","/text_files/", strip=False):
         print(line[0])


def audience_help(question, answers: {}, correct_value: str, game_level):
    len_al = 45
    percent_color = bg(200, 35, 254)
    answers_list = list(answers.keys())
    if util.game_language == util.Language.HUNGARIAN.name:
        util.play_sound("push_your_buttons", 0)
        time.sleep(2)
    else:
        util.play_sound("audience", 0)
    util.clear_screen()
    len_window = 21

    for i in range(len(answers_list)):
        answers_list = list(answers.keys())
        chances = get_chances(answers, correct_value)
        string_value = ""
        values = []
        for key, value in sorted(chances.items()):
            values.append(round(value/10))
            next_value = str(value)
            if len(next_value) == 1:
                next_value = next_value + " "
            string_value = string_value + " " + next_value + "% "
        index = 0
        for line in util.open_file("quizmaster", "r", ";","/text_files/", strip=False):
            percentages = ""
            missing_space = len_al-len(line[0])
            if index == 0:
                print(line[0] + " " * (missing_space+1) + "_"*(len_window-1))
            elif index == 1:
                print(line[0] + " " * missing_space + "|" + string_value + "|")
            elif index == 2:
                print(line[0] + " " * missing_space + "|" + (len_window-1)*" " + "|")
            else:
                if index < 13:
                    for j in range(10):
                        if j == (index -3):
                            if values[0] >= 10-j:
                                percentages = percentages + percent_color + "   " + bg. rs + "  "
                            else:
                                percentages = percentages + "     "
                            if values[1] >= 10-j:
                                percentages = percentages + percent_color + "   " + bg. rs  + "  "
                            else:
                                percentages = percentages + "     "
                            if values[2] >= 10-j:
                                percentages = percentages + percent_color + "   " + bg. rs  + "  "
                            else:
                                percentages = percentages + "     "
                            if values[3] >= 10-j:
                                percentages = percentages + percent_color + "   " + bg. rs
                            else:
                                percentages = percentages + "   "
                    print(line[0]+ " " * (missing_space) + "| " + percentages + " |")
                elif index == 13:
                    print(line[0]+ " " * (missing_space) + "|" + fg.orange + rs.dim_bold +"  A ♦  B ♦  C ♦  D " + fg.rs + " |")
                elif index == 14:
                    print(line[0] + " " * (missing_space+1) + "‾" * (len_window-1))
                else:
                    print(line[0])
            index += 1
        print_quiz_table(question, answers, game_level=game_level, quizmaster=False)
        time.sleep(1)
        if i < len(answers_list)-1:
            util.clear_screen()
            i += 1
        else:
            util.play_sound("audience_end", 0)


def telephone_help(question: str, answers: {}, correct_answer: str):
    phone = safe_input("  " + language_dictionary[game_language].quiz.phone_prompt,
                       ["m", "d", "t", "y"])
    call_text_files = ["mum_phone_" + str(game_language).lower(),
                       "dad_phone_" + str(game_language).lower(),
                       "teacher_phone_" + str(game_language).lower(),
                       "yoda_master_phone_" + str(game_language).lower()
                       ]
    conversation = ""
    for i in range(len(call_text_files)):
        if phone.lower() == call_text_files[i][0]:
            conversation = (util.open_file(call_text_files[i], 'r', separator=";"))
            util.play_sound("phone_ring", 0)
            time.sleep(2)
            util.play_sound("phone_call", 0)
    len_al = 45
    util.clear_screen()
    len_window = 5
    then = time.time()
    text = ""
    now = 0.0
    for i in range(30):
        index = 0
        for line in util.open_file("quizmaster", "r", ";","/text_files/", strip=False):

            missing_space = len_al-len(line[0])
            if index == 0:
                print("\n\n\n\n" + line[0] + " " * (missing_space+1) + "_"*(len_window-1))
            elif index == 1:
                print(line[0] + " " * missing_space + "|" + (len_window-1)*" " + "|")
            else:
                if index == 2:
                    now = time.time()
                    print(line[0]+ " " * (missing_space) + "| " + fg.orange + str(30 - int(now - then)) + fg.rs + " |")
                    print(line[0] + " " * (missing_space) + "|"  + "_" * (len_window - 1)+ "|")
                else:
                    print(line[0])
            index += 1
        print_quiz_table(question, answers, quizmaster=False)
        if i == 0:
            text = "  " +  text + "\n" + "   " + conversation[0][0] + " \n" + "   " + question + " " + ", ".join(list(answers.values()))
        elif i == len(conversation)-1:
            if phone == "y":
                text = "  " + text + "\n" + "   " + conversation[5][0] + " " + correct_answer.upper()
            else:
                text = "  " +  text + "\n" + "   " + conversation[4][0] + " " + correct_answer.upper()
            print(text)
            break
        elif i == len(conversation)-2:
            time.sleep(2)
            text = text + "\n" + "   " +  conversation[i][0]
        else:
            text = text + "\n" + "   " +  conversation[i][0]
        print(text)
        time.sleep(2)
        if i < 30:
            util.clear_screen()
            i += 1
    util.play_sound('phone_call_ends', 0)
    time.sleep(5)
    print("\n   " + language_dictionary[game_language].quiz.call_duration, int(now - then),
          language_dictionary[game_language].quiz.call_seconds)
    util.stop_sound()


def print_prizes_with_quizmaster(level: int, nullprize=False, special_text="", bg_color = bg.blue):
    prizes = util.open_file("prizes_" + str(game_language).lower(), "r")
    util.clear_screen()
    global table_length
    decor_str = " ♦ "
    prize = decor_str + prizes[level][0] + decor_str
    if nullprize == True:
        if util.game_language == util.Language.HUNGARIAN.name:
            prize= "0 Ft"
        if util.game_language == util.Language.ENGLISH.name:
            prize= "£0"
    if special_text != "":
        prize = special_text
    prize_length = len(prize)
    number_of_spaces = int((table_length - prize_length) / 2)
    if prize_length % 2 == 0:
        prize = prize + " "
    for i in range(4):
        print("\r")
    for line in util.open_file("quizmaster", "r", ";", "/text_files/", strip=False):
        print(line[0])
    print("  /" + "‾" * (table_length) + "\\")
    print(" ◄ " + bg_color + fg.orange + number_of_spaces * " " + prize  + fg.rs + " " * number_of_spaces + bg.rs + " ►")
    print("  \\" + "_" * (table_length) + "/")


def show_game_structure():
    import time, msvcrt
    # TODO: only works on win

    timeout = 2
    startTime = time.time()
    inp = None
    print(language_dictionary[util.game_language].quiz.skip_prompt)
    while True:
        if msvcrt.kbhit():
            inp = msvcrt.getch()
            break
        elif time.time() - startTime > timeout:
            break
    util.clear_screen()
    if inp:
        return

    game_language = util.game_language
    prizes = util.open_file("prizes_" + str(game_language).lower(), "r")
    if game_language == util.Language.HUNGARIAN.name:
        util.play_sound("prizes_description", 0)
        print_helps()
        print("\n\n")
        for i in range(len(prizes)):
            for j in range(len(prizes)):
                round_number = str(len(prizes) - j)
                if len(prizes) - j < 10:
                    round_number = " " + round_number
                if i == len(prizes) - j - 1:
                    print(round_number + " ♦ " + bg.orange + fg.black + prizes[::-1][j][0] + fg.rs + bg.rs)
                else:
                    if j == 5 or j == 10 or j == 0:
                        print(round_number + " ♦ " + prizes[::-1][j][0])
                    else:
                        print(round_number + " ♦ " + fg.orange + prizes[::-1][j][0] + fg.rs)
            if os.name == "nt":
                time.sleep(0.3)
            else:
                time.sleep(0.4)
            if i != 14:
                util.clear_screen()
                print_helps()
                print("\n\n")
        if os.name == "posix":
            time.sleep(2)
        else:
            time.sleep(0.7)
        util.clear_screen()
        print_helps()
        print("\n\n")
        for a in range(2):
            for b in range(len(prizes)):
                round_number = str(len(prizes) - b)
                if len(prizes) - b < 10:
                    round_number = " " + round_number
                if a == 0 and b == 10 or a == 1 and b == 5:
                    print(round_number + " ♦ " + bg.orange + fg.black + prizes[::-1][b][0] + fg.rs + bg.rs)
                else:
                    if b == 0 or b == 5 or b == 10:
                        print(round_number + " ♦ " + prizes[::-1][b][0])
                    else:
                        print(round_number + " ♦ " + fg.orange + prizes[::-1][b][0] + fg.rs)
            time.sleep(1)
            if a == 1 and os.name == "nt":
                time.sleep(0.4)
            util.clear_screen()
            print_helps()
            print("\n\n")
        util.play_sound("help_modules", 0)
        util.clear_screen()
        list_helps()
        time.sleep(3)
        util.clear_screen()
        print_helps()
        print("\n\n")
        print_prizes()
        util.play_sound("prologue_end", 0, timer=True)
        util.clear_screen()
    else:
        helps = [" 50 : 50 ", "     \_] ", "  ☺ ☺ ☺  "]
        separator = fg.blue + "|" + fg.rs
        print(fg.blue + 31 * "-" + fg.rs)
        print(separator + helps[0] + separator + helps[1] + separator + helps[2] + separator)
        print(fg.blue + 31 * "-" + fg.rs)
        print("\n\n")
        print_prizes()
        time.sleep(4)
        util.clear_screen()


def print_helps():
    helps = [" 50 : 50 ", "     \_] ", "  ☺ ☺ ☺  "]
    separator = fg.blue + "|" + fg.rs
    print(fg.blue + 31 * "-" + fg.rs)
    print(separator + helps[0] + separator + helps[1] + separator + helps[2] + separator)
    print(fg.blue + 31 * "-" + fg.rs)


def list_helps():
    helps = [" 50 : 50 ", "     \_] ", "  ☺ ☺ ☺  "]
    separator = fg.blue + "|" + fg.rs
    print(fg.blue + 31 * "-" + fg.rs)
    print(separator + bg.orange + fg.black + helps[0] + fg.rs + bg.rs + separator + helps[1] + separator + helps[
        2] + separator)
    print(fg.blue + 31 * "-" + fg.rs)
    print("\n\n")
    print_prizes()
    time.sleep(1.3)
    util.clear_screen()
    print(fg.blue + 31 * "-" + fg.rs)
    print(separator + helps[0] + separator + bg.orange + fg.black + helps[1] + fg.rs + bg.rs + separator + helps[
        2] + separator)
    print(fg.blue + 31 * "-" + fg.rs)
    print("\n\n")
    print_prizes()
    time.sleep(1.3)
    util.clear_screen()
    print(fg.blue + 31 * "-" + fg.rs)
    print(separator + helps[0] + separator + helps[
        1] + separator + bg.orange + fg.black + "  ☻ ☻ ☻  " + fg.rs + bg.rs + separator)
    print(fg.blue + 31 * "-" + fg.rs)
    print("\n\n")
    print_prizes()


def print_prizes():
    game_language = util.game_language
    prizes = util.open_file("prizes_" + str(game_language).lower(), "r")
    for i in range(len(prizes)):
        round_number = str(len(prizes) - i)
        if len(prizes) - i < 10:
            round_number = " " + round_number
        if i == 5 or i == 10 or i == 0:
            print(round_number + " " + prizes[::-1][i][0])
        else:
            print(round_number + " " + fg.orange + prizes[::-1][i][0] + fg.rs)


def play_music(round: int):
    if round < 5:
        util.play_background_music(str(5), 0)
    else:
        util.play_background_music(str(round), 0)


def play_marked_sound(choise: str, level: int):
    sound_files = ["Lets_mark", "mark_" + choise, "mark_" + choise + "_1", "mark_" + choise + "_2"]
    if level == 7:
        util.play_sound("mark_500", 0)
        time.sleep(6)
    else:
        util.play_sound(random.choice(sound_files), 0)
        time.sleep(1)


def handle_user_input(question: str, answers: dict, level: int, final_color="orange", out_of_game = False) -> str:
    select_text = language_dictionary[game_language].quiz.select_answer
    if out_of_game:
        select_text = language_dictionary[game_language].quiz.select_answer_out
    final_sounds = ["final"]
    for i in range(18):
        final_sounds.append("final_" + str(i+1))
    lets_see_sounds = ["lets_see", "lets_see_1", "lets_see_2", "lets_see_3"]
    while True:
        user_input = get_user_input()
        if user_input == b'a' or user_input == "a":
            selected_final_sound = random.choice(final_sounds)
            selected_lets_see_sound = random.choice(lets_see_sounds)
            util.clear_screen()
            print_quiz_table(question, answers, game_level=level, selected="a", color="li_grey")
            print("\n\n   " + fg.grey + select_text + fg.rs)
            util.stop_sound()
            util.play_sound(selected_final_sound, 0, timer=True)
            if not out_of_game:
                play_music(level)
            while True:
                user_input = get_user_input()
                if user_input == b'\r' or user_input == '<Ctrl-j>':
                    util.clear_screen()
                    print_quiz_table(question, answers, "a", final_color, game_level=level)
                    util.stop_sound()
                    play_marked_sound("a", level)
                    util.play_sound("marked", 0)
                    time.sleep(2)
                    util.play_sound(selected_lets_see_sound, 0)
                    time.sleep(3)
                    return "a"
                if user_input not in [b'a', "a"]:
                    break
        if user_input == b'b' or user_input == "b":
            selected_final_sound = random.choice(final_sounds)
            selected_lets_see_sound = random.choice(lets_see_sounds)
            util.clear_screen()
            print_quiz_table(question, answers, game_level=level, selected="b", color="li_grey")
            print("\n\n   " + fg.grey + select_text + fg.rs)
            util.stop_sound()
            util.play_sound(selected_final_sound, 0, timer=True)
            if not out_of_game:
                play_music(level)
            while True:
                user_input = get_user_input()
                if user_input == b'\r' or user_input == '<Ctrl-j>':
                    util.clear_screen()
                    print_quiz_table(question, answers, "b", final_color, game_level=level)
                    util.stop_sound()
                    play_marked_sound("b", level)
                    util.play_sound("marked", 0)
                    time.sleep(2)
                    util.play_sound(selected_lets_see_sound, 0)
                    time.sleep(3)
                    return "b"
                if user_input not in [b'b', "b"]:
                    break
        if user_input == b'c' or user_input == "c":
            selected_final_sound = random.choice(final_sounds)
            selected_lets_see_sound = random.choice(lets_see_sounds)
            util.clear_screen()
            print_quiz_table(question, answers, game_level=level, selected="c", color="li_grey")
            print("\n\n   " + fg.grey + select_text + fg.rs)
            util.stop_sound()
            util.play_sound(selected_final_sound, 0, timer=True)
            if not out_of_game:
                play_music(level)
            while True:
                user_input = get_user_input()
                if user_input == b'\r' or user_input == '<Ctrl-j>':
                    util.clear_screen()
                    print_quiz_table(question, answers, "c", final_color, game_level=level)
                    util.stop_sound()
                    play_marked_sound("c", level)
                    util.play_sound("marked", 0)
                    time.sleep(2)
                    util.play_sound(selected_lets_see_sound, 0)
                    time.sleep(3)
                    return "c"
                if user_input not in [b'c', "c"]:
                    break
        if user_input == b'd' or user_input == "d":
            selected_final_sound = random.choice(final_sounds)
            selected_lets_see_sound = random.choice(lets_see_sounds)
            util.clear_screen()
            print_quiz_table(question, answers, game_level=level, selected="d", color="li_grey")
            print("\n\n   " + fg.grey + select_text + fg.rs)
            util.stop_sound()
            util.play_sound(selected_final_sound, 0, timer=True)
            if not out_of_game:
                play_music(level)
            while True:
                user_input = get_user_input()
                if user_input == b'\r' or user_input == '<Ctrl-j>':
                    util.clear_screen()
                    print_quiz_table(question, answers, "d", final_color, game_level=level)
                    util.stop_sound()
                    play_marked_sound("d", level)
                    util.play_sound("marked", 0)
                    time.sleep(2)
                    util.play_sound(selected_lets_see_sound, 0)
                    time.sleep(3)
                    return "d"
                if user_input not in [b'd', "d"]:
                    break
        if not out_of_game:
            if user_input == b't' or user_input == "t":
                return "t"
            if user_input == b'k' or user_input == "k":
                return "t"
            if user_input == b'h' or user_input == "h":
                return "h"
            if user_input == b's' or user_input == "s":
                return "h"
        if user_input == b'\x1b' or user_input == '<ESC>':
            return "esc"


def handle_fastest_fingers_first_input(question: str, answers: dict, level: int, selected: str, final_color="orange") -> str:
    select_text = language_dictionary[game_language].quiz.select_answer_out
    while True:
        user_input = get_user_input()

        if user_input == b'a' or user_input == "a":
            util.clear_screen()
            print_fastest_fingers_table(question, answers, selected+"a", final_color, game_level=level, quizmaster=True, prizes=False)
            print("\n\n   " + fg.grey + select_text + fg.rs)
            return "a"

        if user_input == b'b' or user_input == "b":
            util.clear_screen()
            print_fastest_fingers_table(question, answers, selected+"b", final_color, game_level=level, quizmaster=True, prizes=False)
            print("\n\n   " + fg.grey + select_text + fg.rs)
            return "b"

        if user_input == b'c' or user_input == "c":
            util.clear_screen()
            print_fastest_fingers_table(question, answers, selected+"c", final_color, game_level=level, quizmaster=True, prizes=False)
            print("\n\n   " + fg.grey + select_text + fg.rs)
            return "c"

        if user_input == b'd' or user_input == "d":
            util.clear_screen()
            print_fastest_fingers_table(question, answers, selected+"d", final_color, game_level=level, quizmaster=True, prizes=False)
            print("\n\n   " + fg.grey + select_text + fg.rs)
            return "d"

        if user_input == b'\x1b' or user_input == '<ESC>':
            return "esc"


def get_user_input() -> bytes:
    if util.operating_system == "posix":
        user_input = helpers.return_user_input_linux()
    else:
        user_input = helpers.return_user_input_windows()

    return user_input


def quit_game(level: int, name, topic):
    if level > 0:
        write_content_to_file("scores.json", {"user": name, "topic": topic, "score": level+1, "time": time.ctime(time.time())})
    menu.return_prompt()
    util.stop_sound()