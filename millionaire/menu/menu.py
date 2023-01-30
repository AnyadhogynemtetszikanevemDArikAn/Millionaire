import msvcrt
import os
import sys
import time
import json
import threading
import keyboard
from sty import Style, RgbFg, fg, bg, rs
import millionaire.quiz_game.quiz_game as quiz
import millionaire.util.util as util
import millionaire.menu.helpers as helpers

fg.purple = Style(RgbFg(148, 0, 211))
bg.orange = bg(255, 150, 50)
language_dictionary = util.language_dictionary
default_width = 40
screen_distance = 60

def intro():
    bg.purple = bg(148, 0, 211)
    util.clear_screen()
    if util.game_language == util.Language.HUNGARIAN.name:
        util.play_sound("intro", 0, volume=1)
    else:
        util.play_sound("intro", 0)

    ## 109 normal 1 liner question
    # quiz.print_quiz_table("Mely állítási ódák nem kapcsolódnak a közgazdász szerepéhez?aa111111111111111111111111aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    #                      {"a": "A t1á1rs",
    #                      "b": "A kormányphhhhhhhhhhh4444444444444444444222222222222222hhhhhhhhhhhhhhhhh11111111111111111111111111111111111111111111101234567890123311111111111111111111111112222222222222222222222113",
    #                          "c": "Kísérlet",
    #                     "d": "Általános"})
    width = 48
    i = 0
    if util.game_language == util.Language.HUNGARIAN.name:
        text_millionaire = bg.rs + fg.white + "   M     I     L     L     I     O     M     O     S    " + bg.rs + fg.rs
        text_who =  "  LEGYEN   ÖN   IS  "
        text_who2 = "   LEGYEN   ÖN  IS "
    else:
        text_millionaire = bg.rs + fg.white + "  M    I    L    L    I    O    N    A    I    R    E   " + bg.rs + fg.rs
        text_who =  " WHO WANTS  TO BE A "
        text_who2 = " WHO WANTS TO BE A "

    for i in range(width):
        line = ""
        if i < width / 3:
            len_spaces = int(width / 3) - i
            if i == 0 or i == 1:
                line = bg.purple + ((2 * (int(width / 3)) + i * 2) + 4) * "X"
            elif i == 12:
                line = bg.blue + fg.blue + int((2 * (int(width / 3)) + i * 2) / 3) * "X" + fg.rs + bg.rs + text_who + bg.blue + fg.blue + int(
                    (2 * (int(width / 3)) + i * 2) / 3) * "X"
            # elif i == 7:
            #    line= int((2*(int(width / 3)) + i*2)/3) * "X" + text_wants + bg.purple + int((2*(int(width / 3)) + i*2)/3) * "X"+ bg.rs
            # elif i == 9:
            #    line= int((2*(int(width / 3)) + i*2)/3) * "X" + text_to_be + bg.purple + int((2*(int(width / 3)) + i*2)/3) * "X"+ bg.rs
            # elif i == 11:
            #    line= int((2*(int(width / 3)) + i*2)/3) * "X" + text_a + bg.purple + int((2*(int(width / 3)) + i*2)/3) * "X"+ bg.rs
            else:
                line = bg.blue + fg.blue + (2 * (int(width / 3)) + i * 2) * "X"
        elif i < width - width / 3:
            len_spaces = 0
            if i == width / 2:
                line = bg.blue + fg.blue + int(width / 10) * "X" + int(
                    ((width - int(width / 3)) - len(text_millionaire)) / 2) * " " + fg.rs + bg.rs + text_millionaire + bg.blue + fg.blue + int(
                    ((width - int(width / 3)) - len(text_millionaire)) / 2) * " " + int(width / 10) * "X"
            else:
                line =  bg.blue  + fg.blue + (width - int(width / 3)) * "X" + (width - int(width / 3)) * "X" + bg.rs
        else:
            len_spaces = i - (width - int(width / 3)) - 1
            if i == 36:
                line = bg.blue + fg.blue + int((width * 2 - (i - (width - (int(width / 3)) - 1)) - i) / 3) * "X" + fg.rs + bg.rs + text_who2 + bg.blue + fg.blue + int(
                    (width * 2 - (i - (width - (int(width / 3)) - 1)) - i) / 3) * "X"
            elif i == 46 or i == 47:
                line = bg.purple + ((width * 2 - (i - (width - (int(width / 3)) - 1)) - i) + 4) * "X" + bg.rs
            else:
                line =  bg.blue + fg.blue + (width * 2 - (i - (width - (int(width / 3)) - 1)) - i) * "X"
        if i not in [0, 1, 46, 47]:
            print(bg.rs + fg.rs + len_spaces * " " + bg.purple + fg.purple + "XX" + bg.rs + line + bg.purple + fg.purple + line[-2:] + bg.rs)
        else:
            print(len_spaces * " " + fg.purple+ line + bg.rs + fg.rs)

        time.sleep(0.1)


        i += 1

    timeout = 15
    startTime = time.time()
    inp = None

    print( screen_distance * "   " + language_dictionary[util.game_language].menu.skip_prompt)
    #time.sleep(1)
    #util.clear_screen()
    while True:
        # TODO: only works on win
        if msvcrt.kbhit():
            inp = msvcrt.getch()
            break
        elif time.time() - startTime > timeout:
            break

    if inp:
        util.stop_sound()
        return
    else:
        return


def old_intro():
    util.clear_screen()
    if util.game_language == util.Language.HUNGARIAN.name:
        util.play_sound("intro", 0, volume=1)
    else:
        util.play_sound("intro", 0)
    file = (util.open_file("intro_" + str(util.game_language).lower(), 'r'))


    first_line = threading.Timer(6.0, print_intro_lines, args=(file[0][0], ""))
    second_line = threading.Timer(9.0, print_intro_lines, args=(file[3][0], "purple"))
    third_line = threading.Timer(11.0, print_intro_lines, args=(file[1][0], ""))
    fourth_line = threading.Timer(13.0, print_intro_lines, args=(file[2][0], ""))

    first_line.start()
    second_line.start()
    third_line.start()
    fourth_line.start()

    timeout = 15
    startTime = time.time()
    inp = None

    print("\n"*default_width + screen_distance * "   "  +language_dictionary[util.game_language].menu.skip_prompt)
    time.sleep(1)
    util.clear_screen()
    while True:
        # TODO: only works on win
        if msvcrt.kbhit():
            inp = msvcrt.getch()
            break
        elif time.time() - startTime > timeout:
            break

    if inp:
        threading.Timer.cancel(first_line)
        threading.Timer.cancel(second_line)
        threading.Timer.cancel(third_line)
        threading.Timer.cancel(fourth_line)
        util.stop_sound()
        return
    else:
        return


def print_intro_lines(text: "", text_color: ""):
    if text_color == "purple":
        print(fg.purple + text + fg.rs)
        return
    else:
        print(text)
        return


def user_pressed_space():
    if util.operating_system == "posix":
        user_input = helpers.return_user_input_linux()
    else:
        user_input = helpers.return_user_input_windows()
    if user_input not in [b' ', '<SPACE>']:
        return

    util.stop_sound()
    return


def show_title():
    line_length = default_width + 3
    util.clear_screen()
    print(screen_distance*" " + "=" * line_length)
    print(screen_distance*" " + fg.purple + language_dictionary[util.game_language].menu.title_first_line + fg.rs)
    print(screen_distance*" " + "=" * line_length)
    print(screen_distance*" " + fg.yellow + "|" * line_length + fg.rs)
    print(screen_distance*" " + fg.purple + language_dictionary[util.game_language].menu.title_second_line + fg.rs)
    print(screen_distance*" " + fg.yellow + "|" * line_length + fg.rs)
    print(screen_distance*" " + "=" * line_length)
    print(screen_distance*" " + fg.purple + language_dictionary[util.game_language].menu.title_first_line + fg.rs)
    print(screen_distance*" " + "=" * line_length + "\n\n")


def show_options(options: list, max_options_length: int, chosen_option=0):
    show_title()
    fore_string = "| "
    after_string = " |"
    line_length = max_options_length
    option_length = max_options_length
    for i in range(len(options)):
        option = options[i]
        number_of_spaces = int((option_length - len(options[i]) - len(fore_string) - len(after_string)) / 2)
        if len(option) % 2 != 0:
            option = option + " "
        print(screen_distance*" " +  "  " + "_" * line_length)
        if i == chosen_option:
            string_to_print = "  " + fore_string + bg.orange + number_of_spaces * " " + fg.black + option + fg.rs + number_of_spaces * " " + bg.rs + after_string
        else:
            string_to_print = "  " + fore_string + number_of_spaces * " " + option + number_of_spaces * " " + after_string
        print(screen_distance*" " +  string_to_print)
        print(screen_distance*" " +  "  " + "‾" * line_length + "\n")




def select_exit():
    sys.exit(0)


def select_help():
    quiz.show_game_structure()
    util.clear_screen()
    file = (util.open_file("tutorial_" + str(util.game_language).lower(), 'r'))
    print("\n")
    for line in file:
        print("   " + line[0])
    print("\n")
    return_prompt()


def select_credits():
    util.clear_screen()
    file = (util.open_file("credits_" + str(util.game_language).lower(), 'r'))
    print("\n" + fg.purple + rs.italic)
    print("   $$$$   $$$$  $  $     $     $  $$$$$  $$   $     $$$     $  $$$$  $$$$$")
    print("   $  $   $  $  $  $     $     $  $   $  $$   $     $ $     $  $  $  $")
    print("   $   $$    $  $  $     $     $  $   $  $ $  $    $   $    $  $  $  $$$$")
    print("   $         $  $  $     $     $  $   $  $  $ $   $$$$$$$   $  $$$   $")
    print("   $         $  $  $$$$  $$$$  $  $$$$$  $   $$  $       $  $  $  $  $$$$$")
    print("\n" + fg.rs)

    for line in file:
        print("   " + line[0])
    print("\n")
    return_prompt()


def select_scores():
    util.clear_screen()
    print("\n" + fg.purple + rs.italic)
    if util.game_language == util.Language.HUNGARIAN.name:
        print("\n" + fg.purple + rs.italic)
        print("   $$$$$$$$$$$  $$$$$$$$$$   $$      $  $$$$$$$$  $$$$$$$$$$  $       $$")
        print("   $         $  $        $   $ $$    $     $      $        $  $     $$")
        print("   $$$$$$$$$$$  $        $   $   $$  $     $      $        $  $$$$$$")
        print("   $            $        $   $    $$ $     $      $        $  $     $$")
        print("   $            $$$$$$$$$$   $     $$$     $      $$$$$$$$$$  $       $$")
        print("\n" + fg.rs)
    else:
        print("\n" + fg.purple + rs.italic)
        print("   $$$$$  $$$$   $$$$$$   $$$$    $$$$  $$$$$$")
        print("   $      $      $    $   $   $   $     $")
        print("   $$$$$  $      $    $   $ $$    $$$$  $$$$$")
        print("       $  $      $    $   $   $   $         $")
        print("   $$$$$  $$$$$  $$$$$$   $    $  $$$$  $$$$$")
        print("\n" + fg.rs)
    if os.path.isfile("scores.json"):
        f = open("scores.json")
        data = json.load(f)
        scores_sorted = sorted(data, key=lambda d: d['score'], reverse=True)
        len_val = 0
        len_player = 0
        index = 0
        for item in scores_sorted:
            i = 0
            for k, v in item.items():
                if i == 0:
                    if len(v) > len_player:
                        len_player = len(v)
                if i == 1:
                    index = list(
                        language_dictionary[util.Language.ENGLISH.name].menu.settings_menu_question_topics).index(
                        str(v).capitalize())
                    if len(language_dictionary[util.game_language].menu.settings_menu_question_topics[index]) > len_val:
                        len_val = len(language_dictionary[util.game_language].menu.settings_menu_question_topics[index])
                i += 1
        if len_val > len(language_dictionary[util.game_language].menu.scores[1]):
            score_space = len_val - len(language_dictionary[util.game_language].menu.scores[1])
        else:
            score_space = len(language_dictionary[util.game_language].menu.scores[1]) - len_val

        table_len = len(language_dictionary[util.game_language].menu.scores[0]+language_dictionary[util.game_language].menu.scores[1] +
                        language_dictionary[util.game_language].menu.scores[2] + language_dictionary[util.game_language].menu.scores[3])+\
                    score_space+24-len(language_dictionary[util.game_language].menu.scores[3]) + 13
        print("   " + "_" * table_len)
        print("   " +"| " + fg.orange + language_dictionary[util.game_language].menu.scores[0] + fg.rs +" | " + fg.orange + language_dictionary[util.game_language].menu.scores[1] + score_space*" " + fg.rs +" | " + fg.orange +
              language_dictionary[util.game_language].menu.scores[2] + fg.rs +" | " + fg.orange + language_dictionary[util.game_language].menu.scores[3] + (24-len(language_dictionary[util.game_language].menu.scores[3]))*" "+ fg.rs + " |")
        print("   " +"‾" * table_len)
        print("   " +"—" * table_len)

        for item in scores_sorted:
            i = 0
            for k, v in item.items():
                if i == 0:
                    if len(v) > len_player:
                        print("   " +"| " +v + " "*(len(v)-len_player), end=" | ")
                    else:
                        print("   " +"| " +v + " "*(len_player-len(v)), end=" | ")
                if i == 1:
                    index = list(
                        language_dictionary[util.Language.ENGLISH.name].menu.settings_menu_question_topics).index(
                        str(v).capitalize())
                    print(
                          language_dictionary[util.game_language].menu.settings_menu_question_topics[index] +
                          (len_val-len(language_dictionary[util.game_language].menu.settings_menu_question_topics[index]))*" ", end=" | ")
                if i == 2:
                    print(str(v) + " " * (len(language_dictionary[util.game_language].menu.scores[1])-len(str(v))+1), end=" | ")
                if i == 3:
                    print(v, end=" | ")

                i += 1
            print("\n"+ "   " +"—" * table_len)
        f.close()
    else:
        print("\n\n   " + language_dictionary[util.game_language].menu.empty_scores)
    return_prompt()


def select_settings():
    start_index = 0
    util.clear_screen()
    show_options(language_dictionary[util.game_language].menu.settings_menu_options, default_width)
    while True:
        chosen_option = get_user_input(language_dictionary[util.game_language].menu.settings_menu_options,
                                       language_dictionary[util.game_language].menu.settings_menu_options,
                                       default_width, start_index)
        if chosen_option == language_dictionary[util.game_language].menu.settings_menu_options[0]:
            langs = [language_dictionary[util.game_language].en, language_dictionary[util.game_language].hu]
            show_options(langs, 20, util.available_languages.index(util.game_language))
            chosen_lang_option = get_user_input(langs, util.available_languages, 20,
                                                util.available_languages.index(util.game_language), False)
            util.set_game_language(util.available_languages[util.available_languages.index(chosen_lang_option)])
            show_options(language_dictionary[util.game_language].menu.settings_menu_options, 40)
            start_index = 0
        elif chosen_option == language_dictionary[util.game_language].menu.settings_menu_options[1]:
            if util.system_volume:
                util.system_volume = False
            else:
                util.system_volume = True
            show_options(language_dictionary[util.game_language].menu.settings_menu_options, default_width,
                         chosen_option=1)
            start_index = 1
        elif chosen_option == language_dictionary[util.game_language].menu.settings_menu_options[2]:
            if os.name == "nt":
                keyboard.press('f11')
            start_index = 2
        elif chosen_option == language_dictionary[util.game_language].menu.settings_menu_options[3]:
            show_options(language_dictionary[util.game_language].menu.settings_menu_question_topics, default_width,
                         util.topics.index(util.question_topics))
            chosen_question_topic = get_user_input(
                language_dictionary[util.game_language].menu.settings_menu_question_topics, util.topics, default_width,
                util.topics.index(util.question_topics), False)
            util.set_question_topics(chosen_question_topic)
            show_options(language_dictionary[util.game_language].menu.settings_menu_options, 40, chosen_option=3)
            start_index = 3
        elif chosen_option == language_dictionary[util.game_language].menu.settings_menu_options[4]:
            if util.question_difficulty != util.Difficulty.ALL.name:
                show_options(language_dictionary[util.game_language].menu.question_difficulty_levels, 20,
                             util.difficulty_levels.index(util.question_difficulty))
                chosen_difficulty_option = get_user_input(
                    language_dictionary[util.game_language].menu.question_difficulty_levels, util.difficulty_levels, 20,
                    util.difficulty_levels.index(util.question_difficulty), False)
            else:
                show_options(language_dictionary[util.game_language].menu.question_difficulty_levels, 20)
                chosen_difficulty_option = get_user_input(
                    language_dictionary[util.game_language].menu.question_difficulty_levels, util.difficulty_levels, 20,
                    0, False)
            if chosen_difficulty_option != language_dictionary[util.game_language].menu.question_difficulty_levels[0]:
                util.set_question_difficulty(chosen_difficulty_option)
            else:
                util.set_question_difficulty(util.Difficulty.ALL.name)
            show_options(language_dictionary[util.game_language].menu.settings_menu_options, 40, chosen_option=4)
            start_index = 4
        elif chosen_option == language_dictionary[util.game_language].menu.settings_menu_options[5]:
            util.init_settings(util.Language.ENGLISH.name, reset_settings=True)
            start_index = 5
        else:
            update_settings_file()
            return


def update_settings_file():
    filename = "settings.json"
    content = {"language": util.game_language, "topic": util.question_topics, "difficulty": util.question_difficulty,
               "volume": util.system_volume}
    with open(filename, "w", encoding="UTF-8") as outfile:
        json.dump(content, outfile)


def return_prompt():
    esc_keys = [b'\x1b', '<ESC>']
    print(fg.grey + "\n\n   " + language_dictionary[util.game_language].menu.return_prompt + fg.rs)
    if util.operating_system == "posix":
        user_input = helpers.return_user_input_linux()
    else:
        user_input = helpers.return_user_input_windows()
    while user_input not in esc_keys:
        if util.operating_system == "posix":
            user_input = helpers.return_user_input_linux()
        else:
            user_input = helpers.return_user_input_windows()
        if user_input in esc_keys:
            return


def get_user_input(option_list: [], values_list: [], max_option_length: int, start_index=0, esc=True) -> str:
    i = start_index
    while True:
        if util.operating_system == "posix":
            user_input = helpers.return_user_input_linux()
        else:
            user_input = helpers.return_user_input_windows()
        first_char = user_input
        # escape
        if first_char == b'\x1b' or first_char == '<ESC>':
            if esc == True:
                return values_list[-1]
            else:
                return values_list[start_index]
        # enter
        if first_char == b'\r' or first_char == '<Ctrl-j>':
            return values_list[i]
        # up
        if first_char == b'H' or first_char == '<UP>':
            if i == 0:
                i = len(option_list) - 1
                show_options(option_list, max_option_length, len(option_list) - 1)
            else:
                i -= 1
                show_options(option_list, max_option_length, i)
            # enter
            if user_input == b'\r' or user_input == '<Ctrl-j>':
                return values_list[i]
        # down
        if first_char == b'P' or first_char == '<DOWN>':
            if i == len(option_list) - 1:
                i = 0
                show_options(option_list, max_option_length)
            else:
                i += 1
                show_options(option_list, max_option_length, i)
            # enter
            if user_input == b'\r' or user_input == '<Ctrl-j>':
                return values_list[i]


def handle_main_menu():
    start_index = 0
    options_length = default_width
    show_options(language_dictionary[util.game_language].menu.main_menu_options, options_length)
    while True:
        chosen_option = get_user_input(language_dictionary[util.game_language].menu.main_menu_options,
                                       language_dictionary[util.game_language].menu.main_menu_options, options_length,
                                       start_index)
        if chosen_option == language_dictionary[util.game_language].menu.main_menu_options[0]:
            quiz.play()
            show_options(language_dictionary[util.game_language].menu.main_menu_options, options_length)
            start_index = 0
        if chosen_option == language_dictionary[util.game_language].menu.main_menu_options[1]:
            quiz.fastest_finger_first()
            show_options(language_dictionary[util.game_language].menu.main_menu_options, options_length,
                         chosen_option=1)
            start_index = 1
        if chosen_option == language_dictionary[util.game_language].menu.main_menu_options[2]:
            select_help()
            show_options(language_dictionary[util.game_language].menu.main_menu_options, options_length,
                         chosen_option=2)
            start_index = 2
        if chosen_option == language_dictionary[util.game_language].menu.main_menu_options[3]:
            select_settings()
            show_options(language_dictionary[util.game_language].menu.main_menu_options, options_length,
                         chosen_option=3)
            start_index = 3
        if chosen_option == language_dictionary[util.game_language].menu.main_menu_options[4]:
            select_credits()
            show_options(language_dictionary[util.game_language].menu.main_menu_options, options_length,
                         chosen_option=4)
            start_index = 4
        if chosen_option == language_dictionary[util.game_language].menu.main_menu_options[5]:
            select_scores()
            show_options(language_dictionary[util.game_language].menu.main_menu_options, options_length,
                         chosen_option=5)
            start_index = 5
        if chosen_option == language_dictionary[util.game_language].menu.main_menu_options[6]:
            select_exit()
