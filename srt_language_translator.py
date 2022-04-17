import srt_writer_reader as swr
import translators as ts

def printArray(array):
    for line in array:
        print(line)

def translateString(string,from_language,to_langueage):
    translation = ts.google(string,from_language=from_language,to_language=to_langueage)
    return translation

def translateListToList(from_list,from_lang,to_lang):
    translatedList = []
    for text in from_list:
        translatedList.append(translateString(text,from_lang,to_lang))
    return translatedList

def timeTextToTimeInt(time_string):
    time_string = str(time_string).strip()
    time_string_list = time_string.split(":")
    time_milisecond = 0
    time_milisecond += int(time_string_list[0])*60*60*1000
    time_milisecond += int(time_string_list[1])*60*1000
    edit_list = time_string_list[2].split(",")
    time_milisecond += int(edit_list[0])*1000 + int(edit_list[1])
    return time_milisecond

def timeTextToTimeList(time_object):
    time_object = str(time_object).replace(" --> ","½")
    time_object_list = time_object.split("½")
    final_object = [timeTextToTimeInt(time_object_list[0]),timeTextToTimeInt(time_object_list[1])]
    return final_object

def calculateDialogTime(time_details,string):
    start,finish = time_details[0]/1000,time_details[1]/1000
    time_diff = finish - start
    string_words = str(string).split(' ')
    respond_time_list = []
    respond_string_list = []

    if len(string_words) <= 5:
        return {"texts":[string],"times":[time_details]}

    constant = 2
    
    split_string_count = 0

    while split_string_count == 0:
        constant += 1
        if time_diff < constant:
            respond_time_list.append(time_details)
        while time_diff >= constant:
            start += constant
            time_diff = finish - start
            if time_diff < 1 and time_diff > 0:
                respond_time_list.append([int((start-constant)*1000),int(finish*1000)])
            else:
                respond_time_list.append([int((start-constant)*1000),int(start*1000)])
                
        split_string_count = int(len(string_words)/len(respond_time_list))
        if split_string_count == 0:
            start -= constant
            respond_time_list = []
            time_diff = finish - start
    
    total_string = ""
    counter = 1
    for index,elm in enumerate(string_words,0):
        if index < (counter*split_string_count)-1:
            total_string += elm + " "
        elif index == (counter*split_string_count)-1:
            total_string += elm + " "
            counter += 1
            respond_string_list.append(total_string.strip())
            total_string = ""
    
    if total_string != "" and total_string != respond_string_list[-1]:
        respond_string_list.append(total_string.strip())

    return {"texts":respond_string_list,"times":respond_time_list}

def make_three_number(number):
    number = str(number)
    while len(number) < 3:
        number += "0"
    return number

def make_two_number(number):
    number = str(number)
    while len(number) < 2:
        number = "0" + number
    return number

def timeIntToTimeString(array):
    start,finish = array[0],array[1]
    startDict = {}
    finishDict = {}

    startDict["Milisecond"] = make_three_number(start%1000)
    start = int(start/1000)
    startDict["Second"] = make_two_number(start%60)
    startDict["Minute"] = make_two_number(int(start/60)%60)
    startDict["Hour"] = make_two_number(int(start/60/60))

    finishDict["Milisecond"] = make_three_number(finish%1000)
    finish = int(finish/1000)
    finishDict["Second"] = make_two_number(finish%60)
    finishDict["Minute"] = make_two_number(int(finish/60)%60)
    finishDict["Hour"] = make_two_number(int(finish/60/60))

    time_string = f'{startDict["Hour"]}:{startDict["Minute"]}:{startDict["Second"]},{startDict["Milisecond"]} --> '
    time_string += f'{finishDict["Hour"]}:{finishDict["Minute"]}:{finishDict["Second"]},{finishDict["Milisecond"]}'
    return time_string

def fixRowForWordCount(main_list,times_list):
    editted_times_list = []
    final_text_list = []
    final_time_list = []
    for i in times_list:
        editted_times_list.append(timeTextToTimeList(i))

    for i in range(len(main_list)):
        respond_obj = calculateDialogTime(editted_times_list[i],main_list[i])
        for j in range(len(respond_obj["times"])):
                    final_time_list.append(timeIntToTimeString(respond_obj["times"][j]))
                    final_text_list.append(str(respond_obj["texts"][j]).strip())
    return {"time_list":final_time_list,"text_list":final_text_list}


def srtTranslator(file_name,from_language,to_languages):
    print("Language Translating Started")

    from_lang = from_language
    to_langs = to_languages
    first_list = swr.readSRTFile(file_name)

    second_list = []

    for i in first_list:
        i = i.strip("\n")
        if i[-6:] == "&nbsp;":
            i = i[:-6]
        i = i.replace("\n","")
        if i != "":
            second_list.append(i)

    if str(second_list[0]) != "1":
        second_list[0] = "1"

    counter_for_third_list = 1
    main_time_list = []
    third_list = []

    while_index = 0

    while while_index < len(second_list):
        if str(second_list[while_index]) == str(counter_for_third_list):
            main_time_list.append(second_list[while_index+1])
            third_list.append(str(counter_for_third_list))
            third_list.append(second_list[while_index+1])
            j = while_index+2
            total_text = ""
            while j < len(second_list):
                if str(second_list[j]) == str(counter_for_third_list+1):
                    break
                else:
                    total_text += " " + second_list[j]
                    j += 1
            total_text = total_text.strip()
            third_list.append(total_text)
            third_list.append("")
            while_index = j
            if while_index >= len(second_list):
                break
            counter_for_third_list += 1


    translate_texts_list = []
    translate_item_list = []


    for counter_modify in range(len(third_list)):
        if counter_modify%4 == 2:
            translate_item_list.append(third_list[counter_modify])

    counter_translate = 0

    for i in range(len(translate_item_list)):
        if len(translate_texts_list) < counter_translate + 1:
            translate_texts_list.append("")
        if len(translate_texts_list[counter_translate]) + len(translate_item_list[i]) < 5000:
            translate_texts_list[counter_translate] += translate_item_list[i] + ' \n '
        else:
            translate_texts_list[counter_translate] = translate_texts_list[counter_translate][:-3]
            counter_translate += 1
            translate_texts_list.append("")
            translate_texts_list[counter_translate] += translate_item_list[i] + ' \n '

    translate_texts_list[counter_translate] = translate_texts_list[counter_translate][:-3]

    for lang in to_langs:
        translated_list = translateListToList(translate_texts_list,from_lang,lang)
        total_list = []
        for line in translated_list:
            line = str(line).replace("\n","  ").split('   ')
            total_list.extend(line)
        final_obj = fixRowForWordCount(total_list,main_time_list)
        printed_list = []

        for i in range(len(final_obj["time_list"])):
            printed_list.append(str(i+1))
            printed_list.append(final_obj["time_list"][i])
            printed_list.append(final_obj["text_list"][i])
            printed_list.append("")

        swr.writeSRTFile(f'[{str(lang).upper()}] - {file_name}',printed_list,True)
    
    print("Language Translating Finished")
