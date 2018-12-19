# coding=utf-8
import csv
import sys
import json
import datetime
import fileinput
sys.setrecursionlimit(100000)
CityList = []
ProvidersList = []
StationsList = []
Ticket_Data_List = []
CoursesList = []
AverageList=[]
PricesList=[]
MinDurationPerCourse=[]
Count = 0
with open("cities.csv") as cities :
	csv_reader_cities = csv.reader(cities)
	header_cities = next(cities)
	for row in csv_reader_cities :
		CityList.append(row)
with open("providers.csv") as providers : 
	csv_reader_provider = csv.reader(providers)
	header_providers = next(providers)
	for row in csv_reader_provider :
		ProvidersList.append(row)
with open("stations.csv") as stations :
	csv_reader_stations = csv.reader(stations)
	header_stations = next(stations)
	for row in csv_reader_stations :
		StationsList.append(stations)
with open("ticket_data.csv") as ticket_data :
	csv_reader_ticket_data = csv.reader(ticket_data)
	header_ticket_data = next(ticket_data)	
	for row in csv_reader_ticket_data :			
		Ticket_Data_List.append(row)
with open("Courses.csv") as Courses :
	csv_reader_Courses = csv.reader(Courses)
	header_Courses = next(Courses)	
	for row in csv_reader_Courses :			
		CoursesList.append(row)		
# We have all providers, stations, cities, ticket data

#Getting the city by name
def GetCityName(id):
	for i in range(len(CityList)):
		if int(CityList[i][0]) == id :			
			Name=CityList[i][2]			
			return Name
#Getting Transport_type by Id_company
def GetTransportType(id_company):
	for i in range(len(ProvidersList)):
		if int(ProvidersList[i][1]) == id_company:
			Transport_type=ProvidersList[i][-1]
			return Transport_type
#Calculating the average price of each course
def AverageMinMaxPriceCourse(Count = 0, St_city = Ticket_Data_List[Count][10], Ed_City = Ticket_Data_List[Count][-1]):	
	PricesList=[]
	Start_Checker = St_city
	End_Checker = Ed_City
	Sum = 0
	Counter = 0		
	Data=[]
	if Count==0:
		Data.append('St_city')
		Data.append('Ed_city')
		Data.append('Average_price')
		Write2Csv('AveragePriceCourse',Data)
	if Count <= 2500 :
		while Start_Checker==Ticket_Data_List[Count][10] and End_Checker==Ticket_Data_List[Count][11] :
				Data=[]
				Counter+=1
				PricesList.append(Ticket_Data_List[Count][6])
				Sum =Sum + int(Ticket_Data_List[Count][6])
				Count+=1
		if Counter != 0:			
			Average	= Sum/Counter				
			print("Pour start : ", GetCityName(int(St_city))," et la destination ", GetCityName(int(Ed_City))," La moyenne est ", Average, " Le max est :", max(PricesList), " le min est :",min(PricesList))
		
		else :
			pass			
		Data.append(GetCityName(int(St_city)))
		Data.append(GetCityName(int(Ed_City)))
		Data.append(Average)
		Write2Csv('AveragePriceCourse',Data)
		AverageMinMaxPriceCourse(Count,Ticket_Data_List[Count][10],Ticket_Data_List[Count][-1])
	else : 
		print "fin"		
#Getting Courses by Transport type (Start city, destination, Type transport, Prix)
def CoursesByTrasType(Count = 0, St_city = Ticket_Data_List[Count][10], Ed_City = Ticket_Data_List[Count][-1]):
	Start_Checker = St_city
	End_Checker = Ed_City
	TransType = ""
	if Count <= 25000 :
		while Start_Checker == Ticket_Data_List[Count][10] and End_Checker == Ticket_Data_List [Count][11] :
			TransType = GetTransportType(int(Ticket_Data_List[Count][1]))
			Prix = Ticket_Data_List[Count][6]			
			print("Pour start : ", GetCityName(int(St_city))," et la destination ", GetCityName(int(Ed_City))," avec un ",TransType," Avec le prix de", Prix)
			Count+=1
		CoursesByTrasType(Count, Ticket_Data_List[Count][10], Ticket_Data_List[Count][-1])
	else :
		print "fin"
#Calculating min duration per Course 
def MinDurationCourse(Count = 0, St_city = Ticket_Data_List[Count][10], Ed_City = Ticket_Data_List[Count][-1]):
	Start_Checker = St_city
	End_Checker = Ed_City
	MinDurationPerCourse = []
	Data=[]
	if Count==0 :
		Data.append("Course")		
		Data.append("Min_duration")
	if Count<=25000 :
		while Start_Checker == Ticket_Data_List[Count][10] and End_Checker == Ticket_Data_List [Count][11] :
			Data=[]
			date_time_obj_dest = datetime.datetime.strptime(Ticket_Data_List[Count][5],'%Y-%m-%d %H:%M:%S+%f')
			date_time_obj_dep = datetime.datetime.strptime(Ticket_Data_List[Count][4],'%Y-%m-%d %H:%M:%S+%f')
			duration = date_time_obj_dest - date_time_obj_dep
			duration_minutes=duration.total_seconds()		
			MinDurationPerCourse.append(duration_minutes)				
			Count+=1
		print("Pour start : ", GetCityName(int(St_city))," et la destination ", GetCityName(int(Ed_City)), "Min duration : ",str(min(MinDurationPerCourse)))
		Data.append(getCourseById(int(St_city),int(Ed_City)))
		Data.append(str(min(MinDurationPerCourse)))
		Write2Csv('MinDurationCourse',Data)
		MinDurationCourse(Count, Ticket_Data_List[Count][10], Ticket_Data_List[Count][11])	
	else :
		print "fin"
# Get all courses and their average in a new CSV for measurments
def getAllCourses(Count=0,St_city = Ticket_Data_List[Count][10], Ed_City = Ticket_Data_List[Count][-1],Compteur=0) :
	Start_Checker = St_city
	End_Checker = Ed_City
	Data=[]
	if Count==0 :	
		Data.append("St_city_id")
		Data.append("Ed_city_id")
		Data.append("St_city")
		Data.append("Ed_city")
		Data.append("Course")
		Write2Csv('Courses',Data)
	if Count<=25000 :
		while Start_Checker == Ticket_Data_List[Count][10] and End_Checker == Ticket_Data_List [Count][11] :
			Data=[]
			Count+=1
		Course = GetCityName(int(St_city)) + " |-> " + GetCityName(int(Ed_City))
		print Course
		Compteur+=1
		Data.append(int(St_city))
		Data.append(int(Ed_City))
		Data.append(GetCityName(St_city))
		Data.append(GetCityName(Ed_City))
		Data.append(Course)
		Write2Csv('Courses',Data)
		getAllCourses(Count,Ticket_Data_List[Count][10],Ticket_Data_List[Count][11],Compteur)
	else :
		Removedups()
		print "fin"
		
def Write2Csv(FileName,Data):
	with open(FileName+'.csv','a') as file:
		Writer = csv.writer(file)
		Writer.writerow(Data)
#Mesuration examples 
#Prices for different dates for a given course

def PricesDates(Count = 0, St_city = Ticket_Data_List[Count][10], Ed_City = Ticket_Data_List[Count][-1]):
	Start_Checker = St_city
	End_Checker = Ed_City
	Fields=['St_city','Ed_city','Time','Duration in s']
	Write2Csv('DateDuration',Fields)	
	if Count<=25000 :
		while Start_Checker == Ticket_Data_List[Count][10] and End_Checker == Ticket_Data_List [Count][11] :
			Data=[]
			date_time_obj_dest = datetime.datetime.strptime(Ticket_Data_List[Count][5],'%Y-%m-%d %H:%M:%S+%f')
			date_time_obj_dep = datetime.datetime.strptime(Ticket_Data_List[Count][4],'%Y-%m-%d %H:%M:%S+%f')
			duration = date_time_obj_dest - date_time_obj_dep											
			Data.append(GetCityName(int(St_city)))
			Data.append(GetCityName(int(Ed_City)))
			Data.append(str(date_time_obj_dep))
			duration_minutes=duration.total_seconds()
			Data.append(str(duration_minutes))
			Write2Csv('DateDuration',Data)
			Count+=1			
			print("Pour start : ", GetCityName(int(St_city))," et la destination ", GetCityName(int(Ed_City)), "duration : ",str(duration))
			
	else :
		print "fin"
def getCourseById(St_city,Ed_City):
	for i in range(len(CoursesList)):
		if int(CoursesList[i][0])==int(St_city) and int(CoursesList[i][1])==int(Ed_City):
			print CoursesList[i][4]
			return CoursesList[i][4]
def Removedups():
	seen = set()
	for line in fileinput.FileInput('Courses.csv', inplace=1):
		if line in seen :
			continue
		seen.add(line)
		print line,
#Callings