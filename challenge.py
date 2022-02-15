from select import select
from RPA.Browser.Selenium import Selenium
from RPA.PDF import PDF
import sys, os
from time import sleep
import pandas as pd

browser_lib = Selenium()



def open_the_website(url):
    browser_lib.open_available_browser(url)


def search_for(term):
    input_field = "css:input"
    
    all_money = browser_lib.find_elements("xpath://span[@class=' h1 w900']")
    print(all_money)

def remove_blank_spaces(ls):
    return [i for i in ls if i]

#Create excel file and save it
def store_file(filename):
    return None

#Gets the Agency name from the file and then returns it
def recieve_agency_name():
    #Right now this just uses a static name but will add functionality to add more later today. 
    agency_name = "Department of Agriculture"
    return agency_name

def write_to_excel_sheet(department_dict,filename="file"):
    df = pd.DataFrame(data=department_dict, index=[0])
    #Flips it so it uses rows instead of columns 
    df = df.transpose()
    #df.head()
    
    #print (df)
    df.to_excel(f"{filename}.xlsx")
# Define a main() function that calls the other functions in order:

def convert_elements_to_text(ls):
    return [i.text for i in ls]

def download_pdfs(list_of_hrefs):
    
    for i in list_of_hrefs:
        browser_lib.go_to(i)
        sleep(3)
        browser_lib.click_link("#")
        sleep(3)



    

def main():
    agency_spending_dict = {}
    try:
        open_the_website("https://itdashboard.gov/")
        #dive in button is actually a link so go by href
        browser_lib.click_link("#home-dive-in")
        sleep(2)
        #all_money = browser_lib.find_elements("xpath://span[@class=' h1 w900']")

        #Go into the html to find the elements and the first span is the name and second is the amount of money

        #Not using convert function here because issues with out of range errors. 
        all_department_names_elements = browser_lib.find_elements('//*[@class="col-sm-12"]/div[1]/a/span[1]')
        all_department_hrefs = browser_lib.find_elements('//*[@class="col-sm-12"]/div[1]/a')
        all_department_money_elements= browser_lib.find_elements('//*[@class="col-sm-12"]/div[1]/a/span[2]')
        #all_department_elements = browser_lib.find_elements("//*[@id='agency-tiles-widget']/div/div[4]/div[2]/div/div/div/div[1]")
        
        all_department_names = [i.text for i in all_department_names_elements]
        all_department_money = [i.text for i in all_department_money_elements]
        all_department_hrefs = [i.get_attribute('href') for i in all_department_hrefs]

        #dictionary comprehension to associate name and department.
        department_dict = {all_department_names[i]: all_department_money[i] for i in range(len(all_department_money))}

        write_to_excel_sheet(department_dict,"department_spend")
        ##### CLick into Agency

        agency_location = {all_department_names[i]: all_department_hrefs[i] for i in range(len(all_department_money))}
        agency = recieve_agency_name()
        browser_lib.go_to(agency_location[agency])
        
        #Temporary, would add a browser implicit wait in the future. 
        sleep(10)

        #Dynamic Waiting wasn't working for me
        #browser_lib.wait_until_location_contains('//*[@id="block-itdb-custom--5"]/div/div/div/div[2]/div/div[1]/div',15)

        #Need to set focus to get access to the widget. 
        browser_lib.set_focus_to_element('//*[@id="block-itdb-custom--5"]/div/div/div/div[2]/div/div[1]/div')
        #browser_lib.wait_until_location_contains('//*[@id="investments-table-object_length"]',15)
        #browser_lib.set_focus_to_element('//*[@id="block-itdb-custom--5"]/div/div/div/div[2]/div/div[1]/div')
        select_list = browser_lib.find_element('//*[@id="investments-table-object_length"]/label/select')
        #print(select_list)
        browser_lib.select_from_list_by_value(select_list, "-1")
        #Need to wait 10 seconds to make sure that everything in the table loads after selecting show all entries. 
        sleep(10)

        all_uni = convert_elements_to_text(browser_lib.find_elements('//*["@role=row"]/td[1]'))
        #removing all empty elements from list
        all_uni = [i for i in all_uni if i]
        #all_uni_non_hyper_links = browser_lib.find_elements('//*["@role=row"]/td[1]')
        #all_uni_non_hyper_links = all_uni_non_hyper_links[len(all_uni_hyper_links):]
        #all_uni_non_hyper_links = convert_elements_to_text(all_uni_non_hyper_links)

        #combine the two lists
        #all_uni_hyper_links.extend(all_uni_non_hyper_links)

        all_bureau = remove_blank_spaces(convert_elements_to_text(browser_lib.find_elements('//*["@role=row"]/td[2]')))
        all_investment_title = remove_blank_spaces(convert_elements_to_text(browser_lib.find_elements('//*["@role=row"]/td[3]')))
        all_spendings = remove_blank_spaces(convert_elements_to_text(browser_lib.find_elements('//*["@role=row"]/td[3]')))
        all_types = remove_blank_spaces(convert_elements_to_text(browser_lib.find_elements('//*["@role=row"]/td[4]')))
        all_CIO_rating = remove_blank_spaces(convert_elements_to_text(browser_lib.find_elements('//*["@role=row"]/td[5]')))
        all_project_numbers = remove_blank_spaces(convert_elements_to_text(browser_lib.find_elements('//*["@role=row"]/td[6]')))

        #Creates a panda dataframe, joins lists together. 
        new_excel_sheet = pd.DataFrame(
            {'UII' : all_uni,
             'Bureau' : all_bureau,
             'Investment Title': all_investment_title,
             'Total FY2021 Spending ($M)' : all_spendings,
             'Type' : all_types,
             'CIO Rating' : all_CIO_rating,
             '# of Projects' : all_project_numbers
            }
        )

        #print(new_excel_sheet)
        new_excel_sheet.to_excel("individual_investments.xlsx")



        

        #print(all_uni)
        #print(len(all_uni))

        all_uni_hyper_links = browser_lib.find_elements('//*["@role=row"]/td[1]/a')
        all_pdf_href = [i.get_attribute("href") for i in all_uni_hyper_links]

        download_pdfs(all_pdf_href)


    finally:
        browser_lib.close_all_browsers()


# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    main()