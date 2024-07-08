import random
import re
import time
from typing import Dict, Any

from Models.Listener import Listener
from Pdf_Generator.pdf_generator import main as generate_pdf_schedule


class TtGenerator:
    """
    This class generates the actual timetable using the resources passed to it as
    parameters and also provides methods to do this task.
    """

    instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance

    def __init__(self, *cls):
        """
        This is TtGenerator constructor that  accepts n parameters
        :param cls:
        """
        self.is_merge_timeslots = None
        self.Groups = None
        for arg in cls:
            self.Groups = arg

        self.progress_var = 0
        self.Full_Time_table_dict = dict()
        self.Full_Time_table_list = list()
        self.Tutor_tracking = list()
        self.cu_division_box = list()

        self.list_ = list()
        self.list_Merged_Time_dict = dict()
        self.Tutor_group_list = list()
        self.tutor_lst = list()
        self.class_rooms_lst = list()
        self.created_lectures_details_lst_progress_var = list()
        self.created_lectures_details_lst = list()
        self.list_of_groups_by_Tutor = list()

    def random_generator(self, timeslots_lst, created_lectures_details_lst, class_rooms_lst, title, creator, tutor_lst,tutor_lst_email):
        """
        This method generates the time table through the combiation of the functions in this class
        :param timeslots_lst:
        :param created_lectures_details_lst:
        :param class_rooms_lst:
        :param title:
        :param creator:
        :param tutor_lst:
        :return None:
        """
        # First clear / refresh these variables
        self.list_.clear()
        self.list_Merged_Time_dict = dict()
        self.Tutor_group_list.clear()
        self.tutor_lst.clear()
        self.class_rooms_lst.clear()
        self.created_lectures_details_lst.clear()
        self.progress_var = 0
        self.Full_Time_table_dict = dict()
        self.Full_Time_table_list = list()
        self.Tutor_tracking = list()
        self.cu_division_box.clear()
        self.list_of_groups_by_Tutor.clear()
        self.created_lectures_details_lst_progress_var.clear()

        # Assign the values to the  class variables
        self.class_rooms_lst = class_rooms_lst
        self.created_lectures_details_lst = created_lectures_details_lst
        self.list_.clear()
        self.is_merge_timeslots = False
        count_created_lectures = len(self.created_lectures_details_lst)
        self.tutor_lst = tutor_lst

        # Making  copy of lists from the time
        # Every subgroup has to be with its own timeslots to prvent overlapping of time
        for item in self.Groups.get_sub_groups():
            self.list_Merged_Time_dict[str(f'{re.findall(r"<(.*?)>", item)[1]}')] = list()


        for item in self.Groups.get_sub_groups():
            # print("item,", str(f'{re.findall(r"<(.*?)>", item)[1]}'))
            for value in timeslots_lst:
                self.list_Merged_Time_dict[str(f'{re.findall(r"<(.*?)>", item)[1]}')].append(value)

        # get a copy of cu lists for progress_var purposes
        for i in self.created_lectures_details_lst:
            self.created_lectures_details_lst_progress_var.append(i)


        # TODO getting the Grouping started
        self.advanced_optimal_generator(tutor_lst, timeslots_lst)


        llt= self.break_resources()

        try:
            # print("self.Full_Time_table_list ===", self.Full_Time_table_list)
              Listener.ispdf_generated = generate_pdf_schedule(self.get__pdf_resources(), title=title, creator=creator,
                                                             no_weekends=Listener.isWeekendInclusive,breaks_list=llt,contact_info=tutor_lst_email)
            # print("ISPDF generated====", Listener.ispdf_generated)
        except:
            print("Exception occurred in the algorithm",)
        time.sleep(3)

    def get__pdf_resources(self) -> dict[Any, Any]:
        """
        This function generates the PDF resources, after the timetable has been created.
        :return dict():
        """
        # print(self.Full_Time_table_list)
        for faculty in self.Full_Time_table_list:
            self.Full_Time_table_dict[str(f'{re.findall(r"<(.*?)>", faculty)[1]}')] = dict()  # the faculty dict

        for faculty in self.Full_Time_table_dict.keys():
            for item in self.Full_Time_table_list:
                txt_item = str(f'{re.findall(r"<(.*?)>", item)[3]}')
                if str(f'{re.findall(r"<(.*?)>", item)[1]}') == faculty:
                    sep_ = txt_item.split(',')
                    if len(sep_) > 1:
                        for i, text in enumerate(sep_):
                            self.Full_Time_table_dict[faculty][text] = list()
                    else:
                        self.Full_Time_table_dict[faculty][txt_item] = list()

        for faculty in self.Full_Time_table_dict.keys():
            for sub_group in self.Full_Time_table_dict[faculty].keys():
                for item in self.Full_Time_table_list:
                    if str(f'{re.findall(r"<(.*?)>", item)[1]}') == faculty:
                        txt_item = str(f'{re.findall(r"<(.*?)>", item)[3]}')
                        sep_ = txt_item.split(',', -1)
                        # print("Before", txt_item)
                        # print("Sep", sep_)
                        if len(sep_) > 1:

                            for i, text in enumerate(sep_):
                                key = str(f'{re.findall(r"<(.*?)>", item)[4]}')
                                day = None
                                if key == "MON":
                                    day = "Monday"
                                elif key == "TUE":
                                    day = "Tuesday"
                                elif key == "WED":
                                    day = "Wednesday"
                                elif key == "THUR":
                                    day = "Thursday"
                                elif key == "FRI":
                                    day = "Friday"
                                elif key == "SAT":
                                    day = "Saturday"
                                elif key == "SUN":
                                    day = "Sunday"
                                else:
                                    day = None

                                dict_ = {
                                }

                                a, b, c, d, e, f, g,link= re.findall(r'<(.*?)>', item)
                                # print("+++",self.TimeTable[key][i])
                                name = d + "," + " " + a + "," + " " + g + "," + " " + c
                                dict_['name'] = f'<{name}><{link}>'
                                dict_['days'] = day
                                dict_['time'] = f
                                dict_['color'] = "eb8f8f"

                                self.Full_Time_table_dict[faculty][text].append(dict_)

                        else:
                            key = str(f'{re.findall(r"<(.*?)>", item)[4]}')
                            day = None
                            if key == "MON":
                                day = "Monday"
                            elif key == "TUE":
                                day = "Tuesday"
                            elif key == "WED":
                                day = "Wednesday"
                            elif key == "THUR":
                                day = "Thursday"
                            elif key == "FRI":
                                day = "Friday"
                            elif key == "SAT":
                                day = "Saturday"
                            elif key == "SUN":
                                day = "Sunday"
                            else:
                                day = None

                            dict_ = {
                            }

                            a, b, c, d, e, f, g,link= re.findall(r'<(.*?)>', item)
                            # print("+++",self.TimeTable[key][i])
                            name = d + "," + " " + a + "," + " " + g + "," + " " + c
                            dict_['name'] = f'<{name}><{link}>'
                            dict_['days'] = day
                            dict_['time'] = f
                            dict_['color'] = "eb8f8f"

                            self.Full_Time_table_dict[faculty][txt_item].append(dict_)

        # print(self.Full_Time_table_dict)
        return self.Full_Time_table_dict

    def break_resources(self)->list():
        self.list_breaks_ = list()
        day_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for b in Listener.breaks_entry_list:
            for day in day_list:
                dict_ = dict()
                dict_['name'] = "BREAK"
                dict_['days'] = day
                dict_['time'] = b
                dict_['color'] = "eb8f8f"
                self.list_breaks_.append(dict_)
        return self.list_breaks_

    def intersection_of_n_sets(self, list_of_sets):
        """
        This method take in  a list of sets in order to get the intersection points
        :param list_of_sets:
        :return set():
        """
        if not list_of_sets:
            return set()  # If there are no sets, return an empty set

        intersection_set = list_of_sets[0]  # Start with the first set

        for s in list_of_sets[1:]:  # Iterate over the remaining sets
            intersection_set = intersection_set.intersection(s)  # Take the intersection

            # If the intersection becomes empty at any point, return an empty set
            if not intersection_set:
                return set()

        return intersection_set

    def set_list_of_sets(self, subgroups):
        """
        This method takes in subgroups, gets their corresponding lists from
        the list_Merged_Time_dict and returns them as a set each,then appends them to a list.
        :param subgroups:
        :return list():
        """
        list_ = list()
        for group in subgroups:
            list_.append(set(self.list_Merged_Time_dict[group]))
        return list_

    def remove_time_slot(self, subgroups, time_slot):
        """
        This function removes the time_slot from the list of subgroups
        :param subgroups:
        :param time_slot:
        :return None:
        """

        # print("These are the groups", subgroups)
        for group in subgroups:
            for index, time_slot_ in enumerate(self.list_Merged_Time_dict[group]):
                if time_slot_ == time_slot:
                    self.list_Merged_Time_dict[group].remove(time_slot_)

    def check_tutor_overlap(self):
        """
        This function checks for tutor overlap and immediately corrects the overlap if necessary or else the resources are not available.
        :return None:
        """

        for tutor in self.tutor_lst:
            temp_lst = list()
            temp_lst.clear()

            for pos, session_ in enumerate(self.Full_Time_table_list):
                # print("Full_Time_table_list ==",self.Full_Time_table_list[0],pos)
                # print(str(f'{re.findall(r"<(.*?)>", session_)[6]}'))
                if tutor == str(f'{re.findall(r"<(.*?)>", session_)[6]}'):
                    temp_lst.append(
                        str(f'<{re.findall(r"<(.*?)>", session_)[6]}><{re.findall(r"<(.*?)>", session_)[4]}><{re.findall(r"<(.*?)>", session_)[5]}><{re.findall(r"<(.*?)>", session_)[3]}><{pos}>'))

            # print("temp_lst == ", set(temp_lst))

            # This loop iterates over th temp_lst storing the tutor sessions
            for index, item in enumerate(list(set(temp_lst))):
                # item={NAME DAY TIME SUBGROUP,POS}

                for j in list(set(temp_lst))[index + 1:]:
                    if str(f'<{re.findall(r"<(.*?)>", item)[1]}><{re.findall(r"<(.*?)>", item)[2]}>') == str(
                            f'<{re.findall(r"<(.*?)>", j)[1]}><{re.findall(r"<(.*?)>", j)[2]}>'):
                        sep_ = str(f'{re.findall(r"<(.*?)>", item)[3]}').split(',', -1)

                        # Implement here the logic to swap the timeslot
                        if len(sep_) <= 1:
                            # print('less== ', item)

                            # check if there is any free time slot
                            len_of_subgroup_timeslot = len(self.list_Merged_Time_dict[sep_[0]])
                            if len_of_subgroup_timeslot > 0:
                                # print(f'LENGTH== {sep_[0]}', len_of_subgroup_timeslot,)

                                # pick new time
                                time_picked = random.choice(
                                    self.list_Merged_Time_dict[str(sep_[0])])
                                # Original string
                                original_string = self.Full_Time_table_list[int(re.findall(r"<(.*?)>", j)[-1])]

                                # New time to replace the existing time
                                new_time = time_picked

                                # old time
                                old_time = f'<{re.findall(r"<(.*?)>", j)[1]}><{re.findall(r"<(.*?)>", j)[2]}>'

                                # Find the position of the existing time within the string
                                start_index = original_string.find(
                                    f'<{re.findall(r"<(.*?)>", j)[1]}><{re.findall(r"<(.*?)>", j)[2]}>')
                                end_index = start_index + len(
                                    f'<{re.findall(r"<(.*?)>", j)[1]}><{re.findall(r"<(.*?)>", j)[2]}>')

                                # Construct the modified string with the new time
                                modified_string = original_string[:start_index] + new_time + original_string[end_index:]

                                # print("ORI ==", original_string, " MOD ==", modified_string)

                                # put it back to the list at that position
                                self.Full_Time_table_list.insert(int(re.findall(r"<(.*?)>", j)[-1]), modified_string)
                                # print("FF NOW", self.Full_Time_table_list[int(re.findall(r"<(.*?)>", j)[-1])])

                                # remove the newly picked time from the subgroup
                                self.list_Merged_Time_dict[str(sep_[0])].remove(time_picked)

                                # Now insert the time back into its original subgroup
                                self.list_Merged_Time_dict[str(sep_[0])].append(old_time)

                            # To handle what if the time slots are empty maybe make the timeslots for each group more by 1 in the UI GenerateTimeTable  command
                            else:
                                pass

                        else:
                            # TODO : TO BE CONTINUED
                            # What if the groups are many
                            pass
                            # print('More== ', item)

                        # Have to break to prevent repetition
                        break

    def divide_and_remainder(self, num_timeslots, num_tutors_high):
        # Perform the division
        quotient = num_timeslots // num_tutors_high
        # Calculate the remainder
        remainder = num_timeslots % num_tutors_high
        return quotient, remainder

    # Test the function with a number

    def advanced_optimal_generator(self, tutor_lst_, timeslots):
        """
        This get the list of Tuotrs random then make groups out of them
        :param tutor_lst_:
        :return None:
        """

        random.shuffle(self.created_lectures_details_lst)
        random.shuffle(tutor_lst_)

        for index, tutor in enumerate(tutor_lst_):
            self.Tutor_tracking.append(list())
            for item in self.created_lectures_details_lst:
                if str(f'{re.findall(r"<(.*?)>", item)[3]}') == tutor:
                    self.Tutor_tracking[index].append(item)

        div_decider = 0
        if Listener.tutor_with_highest_session_ > Listener.group_with_highest_session_:
            div_decider = Listener.tutor_with_highest_session_

        elif Listener.tutor_with_highest_session_ < Listener.group_with_highest_session_:
            div_decider = Listener.group_with_highest_session_

        else:
            div_decider = Listener.group_with_highest_session_

        #  based on the available timeslot make a list that includes them
        num_of_div, rem = self.divide_and_remainder(len(timeslots), div_decider)

        # check if  rem is 0 if not the add 1 to the divisions
        if rem == 0:
            pass
        else:
            num_of_div = num_of_div + 1

        # make the necessary divisions based on the num_of_div
        for big_div in range(num_of_div):
            self.cu_division_box.append(list())

        # if its 0 just add the small lists in them
        if rem == 0:
            for big_div_ in self.cu_division_box:
                for i in range(div_decider):
                    big_div_.append(list())
        # if not then make room for the last session
        else:
            for i, big_div_ in enumerate(self.cu_division_box):
                if i != num_of_div - 1:
                    for i in range(div_decider):
                        big_div_.append(list())
                else:
                    for i in range(rem):
                        big_div_.append(list())

        # start to randomly generate [pick one tutor list ]
        for tutors_sessions in self.Tutor_tracking:
            # Now we are in the tutors_sessions list
            for lecture in tutors_sessions:
                # pick a random index for timeslot
                rand_list = list()
                rand_list.clear()
                for i in range(num_of_div):
                    rand_list.append(i)

                random.shuffle(rand_list)

                is_lec_fit_for_insert = True

                # use a for loop for backtracking purposes
                is_still_in_for_loop = True

                for index_tm_slot in rand_list:
                    if not is_still_in_for_loop:
                        break

                    for index_timeslot__, timeslot__ in enumerate(self.cu_division_box[index_tm_slot]):
                        # check if the lecture is already in that zone
                        if not is_still_in_for_loop:
                            break

                        # check if the zone is empty at 1st
                        if len(timeslot__) == 0:
                            self.cu_division_box[index_tm_slot][index_timeslot__].append(lecture)
                            is_still_in_for_loop = False
                            break
                        else:
                            for in_zone_lec in timeslot__:
                                # check if the lecture is already
                                if str(f'{re.findall(r"<(.*?)>", lecture)[3]}') == str(
                                        f'{re.findall(r"<(.*?)>", in_zone_lec)[3]}'):
                                    is_lec_fit_for_insert = False
                                    break

                                # checking also for the groups
                                sep_ = str(f'{re.findall(r"<(.*?)>", in_zone_lec)[1]}').split(',', -1)
                                sep__ = str(f'{re.findall(r"<(.*?)>", lecture)[1]}').split(',', -1)
                                # print("SEP", sep__)

                                for sepp in sep__:
                                    if sepp in sep_:
                                        # print("TRUE sep in ")
                                        is_lec_fit_for_insert = False
                                        break

                            # check if the lecture is fit then append it to the timeslot
                            if is_lec_fit_for_insert:
                                self.cu_division_box[index_tm_slot][index_timeslot__].append(lecture)
                                is_still_in_for_loop = False
                                break
                            else:
                                # Reset the  lecture to true
                                is_lec_fit_for_insert = True
                            # TODO else statement to see who is not added in

                self.created_lectures_details_lst_progress_var.remove(lecture)

                self.progress_var = int((((len(self.created_lectures_details_lst) - len(
                    self.created_lectures_details_lst_progress_var)) / len(
                    self.created_lectures_details_lst))) * 100)

        # Adding the Rooms and actual timeslot to the timeslot__
        random.shuffle(timeslots)
        timeslots_count = 0
        # print("Timeslots",timeslots)
        for divi__ in self.cu_division_box:
            for i in divi__:
                new_class_list = list()
                for class_ in self.class_rooms_lst:
                    new_class_list.append(class_)

                for lecture in i:
                    # print("HEHEHEHE=====",lecture)
                    # TODO if the rooms are over go get a brand new class rooms
                    if str(re.findall(r"<(.*?)>", lecture)[-3])=="ONLINE":
                        space_picked="ONLINE"
                    else:
                        try:
                            space_picked="HOLD-ON"
                            for spaceZ in new_class_list:
                                num=int(re.findall(r"<(.*?)>", spaceZ)[1])
                                # print("SPACE: " ,num  ,int(re.findall(r"<(.*?)>", lecture)[-1]))
                                if int(re.findall(r"<(.*?)>", spaceZ)[1]) >= int(re.findall(r"<(.*?)>", lecture)[-1]):
                                    space_picked=str(re.findall(r"<(.*?)>", spaceZ)[0])
                                    if str(re.findall(r"<(.*?)>", lecture)[-3]) == "BLENDED":
                                        space_picked = space_picked + "(BLENDED)"
                                    if len(new_class_list) != 0:
                                        new_class_list.remove(spaceZ)
                                    break
                            if space_picked=="HOLD-ON":
                                space_picked_ = random.choice(new_class_list)
                                space_picked=str(re.findall(r"<(.*?)>", space_picked_)[0])
                                if len(new_class_list) != 0:
                                    new_class_list.remove(space_picked_)
                                if str(re.findall(r"<(.*?)>", lecture)[-3]) == "BLENDED":
                                    space_picked = space_picked + "(BLENDED)"

                        except:
                            space_picked = "VIRTUAL ROOM"
                            # print("Space limit exceeded!!!!")
                    # print(space_picked)






                    self.Full_Time_table_list.append(
                        # Packing the values into a list to hold all the occurrences
                        f'<{re.findall(r"<(.*?)>", lecture)[2]}><{re.findall(r"<(.*?)>", lecture)[0]}><{space_picked}><{re.findall(r"<(.*?)>", lecture)[1]}><{re.findall(r"<(.*?)>", timeslots[timeslots_count])[0]}><{re.findall(r"<(.*?)>", timeslots[timeslots_count])[1]}><{re.findall(r"<(.*?)>", lecture)[3]}><{re.findall(r"<(.*?)>", lecture)[6]}>'
                    )
                    # print(">>>>>>",f'<{re.findall(r"<(.*?)>", lecture)[2]}><{re.findall(r"<(.*?)>", lecture)[0]}><{space_picked}><{re.findall(r"<(.*?)>", lecture)[1]}><{re.findall(r"<(.*?)>", timeslots[timeslots_count])[0]}><{re.findall(r"<(.*?)>", timeslots[timeslots_count])[1]}><{re.findall(r"<(.*?)>", lecture)[3]}><{re.findall(r"<(.*?)>", lecture)[6]}>')
                # print("Timeslots", timeslots_count)
                # print(
                #     f'<{re.findall(r"<(.*?)>", lecture)[2]}><{re.findall(r"<(.*?)>", lecture)[0]}><{space_picked}><{re.findall(r"<(.*?)>", lecture)[1]}><{re.findall(r"<(.*?)>", timeslots[timeslots_count])[0]}><{re.findall(r"<(.*?)>", timeslots[timeslots_count])[1]}><{re.findall(r"<(.*?)>", lecture)[3]}>')
                timeslots_count = timeslots_count + 1
