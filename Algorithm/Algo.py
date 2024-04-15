import random
import re
import time
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
        self.Tutor_tracking=list()
        self.TimeTable = {
            "MON": [],
            "TUE": [],
            "WED": [],
            "THUR": [],
            "FRI": [],
            "SAT": [],
            "SUN": [],
        }
        self.list_ = list()
        self.list_Merged_Time_dict = dict()
        self.timeslots_lst = list()
        self.class_rooms_lst = list()
        self.created_lectures_details_lst = list()

    def random_generator(self, timeslots_lst, created_lectures_details_lst, class_rooms_lst, title, creator):
        """
        This method generates the time table through the combiation of the functions in this class
        :param timeslots_lst:
        :param created_lectures_details_lst:
        :param class_rooms_lst:
        :param title:
        :param creator:
        :return None:
        """


        self.class_rooms_lst = class_rooms_lst
        self.created_lectures_details_lst = created_lectures_details_lst
        self.list_.clear()
        self.is_merge_timeslots = False
        count_created_lectures = len(self.created_lectures_details_lst)

        # Making  copy of lists from the time
        # Every subgroup has to be with its own timeslots to prvent overlapping of time
        for item in self.Groups.get_sub_groups():
                self.list_Merged_Time_dict[str(f'{re.findall(r"<(.*?)>", item)[1]}')]=list()

        # TODO: Give each subgroup its own timeslots so that they don't overlap or share the same Reference from  timeslots_lst(Also check others to see)
        for item in self.Groups.get_sub_groups():
            # print("item,", str(f'{re.findall(r"<(.*?)>", item)[1]}'))
            for value in timeslots_lst:
                self.list_Merged_Time_dict[str(f'{re.findall(r"<(.*?)>", item)[1]}')].append(value)
                self.timeslots_lst.append(value)
        # print("self.list_Merged_Time_dict", self.list_Merged_Time_dict)

        for i in range(count_created_lectures):
            # print("DIP CS 1===", self.list_Merged_Time_dict["DIP CS 1"])
            # print("BSC IT 1===", self.list_Merged_Time_dict["BSC IT 1"])
            # print("BSC CS 1===", self.list_Merged_Time_dict["BSC CS 1"])
            # print("Self.timeslots_lst",  self.timeslots_lst)
            # print("timeslots_lst", timeslots_lst)
            time_picked = ""
            lecture_picked = ""
            space_picked = ""


            # TODO this is where if a lecturer has already got or picked time first priority
            lecture_picked = random.choice(self.created_lectures_details_lst)

            # Randomly Picking time  from the corresponding timeslot
            # TODO MANAGE TIME
            sep_ = str(f'{re.findall(r"<(.*?)>", lecture_picked)[1]}').split(',', -1)

            if len(sep_) <= 1:

                try:
                  time_picked = random.choice(
                    self.list_Merged_Time_dict[str(f'{re.findall(r"<(.*?)>", lecture_picked)[1]}')])
                except:
                    # print("So this is the problem==", lecture_picked,self.list_Merged_Time_dict[str(f'{re.findall(r"<(.*?)>", lecture_picked)[1]}')])
                    return

            else:
                self.is_merge_timeslots = True
                # print("SET =", self.intersection_of_n_sets(self.set_list_of_sets(sep_)))
                inter_set = self.intersection_of_n_sets(self.set_list_of_sets(sep_))
                # Handle the empty set in case there is no intersection.

                if len(inter_set) == 0:
                    # TODO what if no intersection
                    pass
                else:
                    time_picked = random.choice(list(inter_set))

            # TODO if the rooms are over go get a brand new class rooms
            space_picked = random.choice(self.class_rooms_lst)



            tutor_and_time=f'<{re.findall(r"<(.*?)>", lecture_picked)[3]}><{time_picked}>'
            # Check if the Tutor is already in the tutor tracking list
            if tutor_and_time in self.Tutor_tracking:
                # Find free time for the Tutor
                if len(sep_) <= 1:
                    # print("Ohh Ohh Tutor overlaping <=1")
                    for new_time in self.list_Merged_Time_dict[str(f'{re.findall(r"<(.*?)>", lecture_picked)[1]}')]:
                        if new_time != time_picked:
                            time_picked=new_time
                else:
                    # print("Ohh Ohh Tutor overlaping >1")
                    # TODO something if the more groups share the same Tutor and Tutor is occupied at that time
                    pass
            else:
                # Add the Tutor and timeslot to the tutor tracking list if there is no overlap
                self.Tutor_tracking.append(tutor_and_time)





            # Packing the values into a list to hold all the occurrences
            self.Full_Time_table_list.append(
                f'<{re.findall(r"<(.*?)>", lecture_picked)[2]}><{re.findall(r"<(.*?)>", lecture_picked)[0]}><{space_picked}><{re.findall(r"<(.*?)>", lecture_picked)[1]}><{re.findall(r"<(.*?)>", time_picked)[0]}><{re.findall(r"<(.*?)>", time_picked)[1]}><{re.findall(r"<(.*?)>", lecture_picked)[3]}>'
            )

            self.TimeTable[re.findall(r'<(.*?)>', time_picked)[0]].append(
                str(f'<{re.findall(r"<(.*?)>", lecture_picked)[2]}><{re.findall(r"<(.*?)>", lecture_picked)[0]}><{space_picked}><{re.findall(r"<(.*?)>", lecture_picked)[1]}><{re.findall(r"<(.*?)>", time_picked)[1]}><{re.findall(r"<(.*?)>", lecture_picked)[3]}>'))

            if self.is_merge_timeslots == True:
                # print("Reaching ................................................")
                self.remove_time_slot(sep_, time_picked)
                self.is_merge_timeslots = False
                # print("POPPED-- :", self.list_Merged_Time_dict,
                #       lecture_picked)

            else:
                self.list_Merged_Time_dict[str(f'{re.findall(r"<(.*?)>", lecture_picked)[1]}')].remove(time_picked)
                # print("POPPED :",self.list_Merged_Time_dict[str(f'{re.findall(r"<(.*?)>", lecture_picked)[1]}')],lecture_picked)

            self.created_lectures_details_lst.remove(lecture_picked)
            self.class_rooms_lst.remove(space_picked)

            self.progress_var = int((((count_created_lectures - len(
                self.created_lectures_details_lst)) / count_created_lectures)) * 100)
            # print("Progress:", self.progress_var)

            # TODO: Check all the timeslots to see if the list are not empty

            # time.sleep(3)

        generate_pdf_schedule(self.get__pdf_resources(), title=title, creator=creator)
        time.sleep(3)


    def get__pdf_resources(self) -> list:
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

                                a, b, c, d, e, f, g = re.findall(r'<(.*?)>', item)
                                # print("+++",self.TimeTable[key][i])
                                name = d + "," + " " + a + "," + " " + g + "," + " " + c
                                dict_['name'] = name
                                dict_['days'] = day
                                dict_['time'] = f
                                dict_['color'] = "FF94EF"

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

                            a, b, c, d, e, f, g = re.findall(r'<(.*?)>', item)
                            # print("+++",self.TimeTable[key][i])
                            name = d + "," + " " + a + "," + " " + g + "," + " " + c
                            dict_['name'] = name
                            dict_['days'] = day
                            dict_['time'] = f
                            dict_['color'] = "FF94EF"

                            self.Full_Time_table_dict[faculty][txt_item].append(dict_)

        # print("This fine")
        # print(self.Full_Time_table_dict)
        return self.Full_Time_table_dict

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
        :return:
        """
        print("These are the groups",subgroups)
        for group in subgroups:
            for index, time_slot_ in enumerate(self.list_Merged_Time_dict[group]):
                if time_slot_ == time_slot:
                    self.list_Merged_Time_dict[group].remove(time_slot_)
