import shelve
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import pandas
import json
import os
from persiantools.jdatetime import JalaliDate
import datetime
import gc

tarikh_shamsi = "1399-03-27"
tarikh_miladi = JalaliDate(int(tarikh_shamsi.split("-")[0]), int(tarikh_shamsi.split("-")[1]),\
                        int(tarikh_shamsi.split("-")[2])).to_gregorian().strftime("%Y-%m-%d")




buffer_data_dir = "C:/Users/Administrator/Desktop/New folder/buffer_data/"
main_data_dir = "C:/Users/Administrator/Desktop/New folder/main_data/"
final_depos_dir = "C:/Users/Administrator/Desktop/New folder/final_depos/"
test_txt_dir = "C:/Users/Administrator/Desktop/New folder/test.txt"
names_dir = "C:/Users/Administrator/Desktop/New folder/names/"
# files = os.listdir(buffer_data_dir)
# for file in files:
#     os.remove(buffer_data_dir + file)
f = open("passed stocks.txt",'w')
f.close()
def convert_to(x):
    if x == "":
        return 0
    else:
        return x

def start_update():
    global buffer_data_dir,main_data_dir,final_depos_dir,test_txt_dir
    db = shelve.open('links_new')
    links = db['links']
    db.close()
    db = shelve.open('stock_names')
    stock_names = db['stock_names']
    db.close()
    
    options = Options()
#     PROXY = "192.168.192.2:3128" # IP:PORT or HOST:PORT
#     options.add_argument('--proxy-server=http://%s' % PROXY)
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    driver = webdriver.Chrome(options = options)
    files = stock_names
    links_2 = {}
    for item in files:
        links_2[item] = links[item]
    links = links_2
    files = [name.replace(".csv","") for name in os.listdir(buffer_data_dir)]
    for item in files:
        del links[item]
    names = list(links.keys())
    for item in names:
        if item[-1:] == "ح":
            del links[item]
    names = list(links.keys())
    
    driver.get(links[names[0]])
    time.sleep(10)

    for i in range(len(links)):
        print(names[i])
        skip = False
        counter = 0
        driver.get(links[names[i]])
        start_time = time.time()
        start_time_initial = time.time()
        print("dow")
        driver.find_element_by_id('tabs').find_element_by_tag_name('div').find_element_by_tag_name('ul').find_elements_by_tag_name('li')[8].find_element_by_tag_name('a').click()
        
        while True:
            try:
                ct_Buy_CountI = (driver.find_element_by_id('ClientTypeBody').find_element_by_tag_name('tr').find_elements_by_tag_name('td')[2].text.replace(",","").replace(" ",""))
                break
            except:
                if (time.time() - start_time) > 2:
                    #x_forget = int("a")
                    driver.get(links[names[i]])
                    start_time = time.time()
                    driver.find_element_by_id('tabs').find_element_by_tag_name('div').find_element_by_tag_name('ul').find_elements_by_tag_name('li')[8].find_element_by_tag_name('a').click()
                    counter += 1
                    if counter > 2:
                        print(names[i],"passed in cts")
                        skip = True
                        break
        date_today = int(driver.find_element_by_id('ClientTypeBody').find_element_by_tag_name('tr').find_elements_by_tag_name('td')[0].find_elements_by_tag_name('div')[1].text)
        if skip or date_today != int(tarikh_shamsi.split('-')[2]):
            print(date_today , tarikh_shamsi.split('-')[2],"  passed cuz of date")
            continue
        counter = 0
        ct_Buy_CountI = (driver.find_element_by_id('ClientTypeBody').find_element_by_tag_name('tr').find_elements_by_tag_name('td')[2].text.replace(",","").replace(" ",""))
        ct_Buy_CountN = (driver.find_element_by_id('ClientTypeBody').find_element_by_tag_name('tr').find_elements_by_tag_name('td')[3].text.replace(",","").replace(" ",""))
        ct_Buy_I_Volume = (driver.find_element_by_id('ClientTypeBody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].find_element_by_tag_name('div').text.replace(",","").replace(" ",""))
        ct_Buy_N_Volume = (driver.find_element_by_id('ClientTypeBody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[2].find_element_by_tag_name('div').text.replace(",","").replace(" ",""))
        ct_Sell_CountI = (driver.find_element_by_id('ClientTypeBody').find_element_by_tag_name('tr').find_elements_by_tag_name('td')[4].text.replace(",","").replace(" ",""))
        ct_Sell_CountN = (driver.find_element_by_id('ClientTypeBody').find_element_by_tag_name('tr').find_elements_by_tag_name('td')[5].text.replace(",","").replace(" ",""))
        ct_Sell_I_Volume = (driver.find_element_by_id('ClientTypeBody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[3].find_element_by_tag_name('div').text.replace(",","").replace(" ",""))
        ct_Sell_N_Volume = (driver.find_element_by_id('ClientTypeBody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[4].find_element_by_tag_name('div').text.replace(",","").replace(" ",""))
        arzesh_kharid_haghighi = (driver.find_element_by_id('ClientTypeBody').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[1].find_element_by_tag_name('div').text.replace(",","").replace(" ",""))
        arzesh_kharid_hughughi = (driver.find_element_by_id('ClientTypeBody').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[2].find_element_by_tag_name('div').text.replace(",","").replace(" ",""))
        arzesh_furush_haghighi = (driver.find_element_by_id('ClientTypeBody').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[3].find_element_by_tag_name('div').text.replace(",","").replace(" ",""))
        arzesh_furush_hughughi = (driver.find_element_by_id('ClientTypeBody').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[4].find_element_by_tag_name('div').text.replace(",","").replace(" ",""))
        taghir_malekiate_hughughi_be_haghighi = (driver.find_element_by_id('ClientTypeBody').find_elements_by_tag_name('tr')[4].find_elements_by_tag_name('td')[2].find_element_by_tag_name('div').text.replace(",","").replace(" ",""))

        
        driver.find_element_by_id('tabs').find_element_by_tag_name('div').find_element_by_tag_name('ul').find_elements_by_tag_name('li')[0].find_element_by_tag_name('a').click()

        while True:
            try:
                if driver.find_element_by_id('dbp').text == "undefined" or driver.find_element_by_id('d01').text=="ممنوع-متوقف":
                    break
                x = (driver.find_element_by_id('d02').find_elements_by_tag_name('span')[0].text.replace(",","").replace(" ","").split('(')[0])

                break
            except:
                if (time.time() - start_time) > 10:
                    driver.get(links[names[i]])
                    start_time = time.time()
                    counter += 1
                    if counter > 3:
                        skip = True
                        print(names[i],"passed in first load")
                        break
#         if driver.find_element_by_id('dbp').text == "undefined" or skip or len(driver.find_element_by_id('d02').find_elements_by_tag_name('span')) == 0 or driver.find_element_by_id('d01').text=="ممنوع-متوقف":
#             continue
        if skip or len(driver.find_element_by_id('d02').find_elements_by_tag_name('span')) == 0:
            continue
        counter = 0
        tno = (driver.find_element_by_id('d08').text.replace(",","").replace(" ",""))
        tvol = (driver.find_element_by_id('d09').find_element_by_tag_name('div').text.replace(",","").replace(" ",""))
        tval = (driver.find_element_by_id('d10').find_element_by_tag_name('div').text.replace(",","").replace(" ",""))
        py = (driver.find_element_by_id('d05').text.replace(",","").replace(" ",""))
        pf = (driver.find_element_by_id('d04').text.replace(",","").replace(" ",""))
        pmin = (driver.find_element_by_id('d07').text.replace(",","").replace(" ",""))
        pmax = (driver.find_element_by_id('d06').text.replace(",","").replace(" ",""))
        pc = (driver.find_element_by_id('d03').text.split(" ")[0].replace(",","").replace(" ",""))
        try:
            plc = (driver.find_element_by_id('d02').find_elements_by_tag_name('span')[0].text.replace(",","").replace(" ","").split('(')[0])
        except:
            plc = 0
        try:
            pcc = (driver.find_element_by_id('d03').find_elements_by_tag_name('span')[1].text.replace(",","").replace(" ","").split('(')[0])
        except:
            pcc = 0
        try:
            pcp = (driver.find_element_by_id('d03').find_elements_by_tag_name('span')[1].text.replace(",","").replace("%","").replace(")","").replace(" ","").split('(')[1])
        except:
            pcp = 0
        try:
            plp = (driver.find_element_by_id('d02').find_elements_by_tag_name('span')[0].text.replace(",","").replace(" ","").split('(')[1]).replace(")","").replace("%","")
        except:
            plp = 0
        try:
            if driver.find_element_by_id('d02').find_elements_by_tag_name('span')[0].get_attribute('style').split(":")[-1].replace(";","").replace(" ","") == "red":
                plc = "-" + plc
                plp = "-" + plp
        except:
            pass
        try: 
            if driver.find_element_by_id('d03').find_elements_by_tag_name('span')[1].get_attribute('style').split(":")[-1].replace(";","").replace(" ","") == "red":    
                pcc = "-" + pcc
                pcp = "-" + pcp
        except:
            pass
        pl = driver.find_element_by_id('d02').text.split(" ")[0].replace(",","")
        print("yek")
        while True:
            try:
                eps = (driver.find_elements_by_tag_name('table')[9].find_element_by_tag_name('tr').find_elements_by_tag_name('td')[1].text.replace(",","").replace(" ",""))
                break
            except:
                if (time.time() - start_time) > 1:
                    #x_forget = int("a")
                    driver.get(links[names[i]])
                    start_time = time.time()
                    counter += 1
                    print("eps counter value : ",counter)
                    if counter > 6:
                        print(names[i],"passed in eps")
                        skip = True
                        
                        break
        if skip:
            continue
        counter = 0
        
        eps = (driver.find_elements_by_tag_name('table')[9].find_element_by_tag_name('tr').find_elements_by_tag_name('td')[1].text.replace(",","").replace(" ",""))
        pe = (driver.find_element_by_id('d12').text.replace(",","").replace(" ",""))
        pe_guruh = (driver.find_elements_by_tag_name('table')[9].find_element_by_tag_name('tr').find_elements_by_tag_name('td')[5].text.replace(",","").replace(" ",""))
        tmin = (driver.find_element_by_id('PRange2').text.replace(",","").replace(" ",""))
        tmax = (driver.find_element_by_id('PRange1').text.replace(",","").replace(" ",""))
        z = (driver.find_elements_by_tag_name('table')[7].find_element_by_tag_name('tbody').find_element_by_tag_name('tr').find_elements_by_tag_name('td')[1].find_element_by_tag_name('div').text.replace(",","").replace(" ",""))
        mv = (driver.find_element_by_id('d11').find_element_by_tag_name('div').text.replace(",","").replace(" ",""))
        pmin_hafte = driver.find_element_by_id('TopBox').find_elements_by_tag_name('div')[1].find_elements_by_tag_name('div')[2].find_element_by_tag_name("table").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")[2].find_elements_by_tag_name("td")[2].text.replace(",","")
        pmax_hafte = driver.find_element_by_id('TopBox').find_elements_by_tag_name('div')[1].find_elements_by_tag_name('div')[2].find_element_by_tag_name("table").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")[2].find_elements_by_tag_name("td")[1].text.replace(",","")
        pmin_sal = driver.find_element_by_id('TopBox').find_elements_by_tag_name('div')[1].find_elements_by_tag_name('div')[2].find_element_by_tag_name("table").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")[3].find_elements_by_tag_name("td")[2].text.replace(",","")
        pmax_sal = driver.find_element_by_id('TopBox').find_elements_by_tag_name('div')[1].find_elements_by_tag_name('div')[2].find_element_by_tag_name("table").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")[3].find_elements_by_tag_name("td")[1].text.replace(",","")
        darsad_shenavar = driver.find_element_by_id('TopBox').find_elements_by_tag_name('div')[1].find_elements_by_tag_name('div')[7].find_element_by_tag_name('table').find_element_by_tag_name('tbody').find_elements_by_tag_name("tr")[2].find_elements_by_tag_name("td")[1].text.replace(",","")
        miangin_hajme_mah = driver.find_element_by_id('TopBox').find_elements_by_tag_name('div')[1].find_elements_by_tag_name('div')[7].find_element_by_tag_name('table').find_element_by_tag_name('tbody').find_elements_by_tag_name("tr")[3].find_elements_by_tag_name("td")[1].find_element_by_tag_name("div").text.replace(",","")
        print(miangin_hajme_mah)

        pd1 = (driver.find_element_by_id('bl').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[2].text.replace(",","").replace(" ",""))
        zd1 = (driver.find_element_by_id('bl').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[0].text.replace(",","").replace(" ",""))
        qd1 = (driver.find_element_by_id('bl').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].text.replace(",","").replace(" ",""))
        po1 = (driver.find_element_by_id('bl').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[3].text.replace(",","").replace(" ",""))
        zo1 = (driver.find_element_by_id('bl').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[5].text.replace(",","").replace(" ",""))
        qo1 = (driver.find_element_by_id('bl').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[4].text.replace(",","").replace(" ",""))

        pd2 = (driver.find_element_by_id('bl').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[2].text.replace(",","").replace(" ",""))
        zd2 = (driver.find_element_by_id('bl').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[0].text.replace(",","").replace(" ",""))
        qd2 = (driver.find_element_by_id('bl').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[1].text.replace(",","").replace(" ",""))
        po2 = (driver.find_element_by_id('bl').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[3].text.replace(",","").replace(" ",""))
        zo2 = (driver.find_element_by_id('bl').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[5].text.replace(",","").replace(" ",""))
        qo2 = (driver.find_element_by_id('bl').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[4].text.replace(",","").replace(" ",""))

        pd3 = (driver.find_element_by_id('bl').find_elements_by_tag_name('tr')[3].find_elements_by_tag_name('td')[2].text.replace(",","").replace(" ",""))
        zd3 = (driver.find_element_by_id('bl').find_elements_by_tag_name('tr')[3].find_elements_by_tag_name('td')[0].text.replace(",","").replace(" ",""))
        qd3 = (driver.find_element_by_id('bl').find_elements_by_tag_name('tr')[3].find_elements_by_tag_name('td')[1].text.replace(",","").replace(" ",""))
        po3 = (driver.find_element_by_id('bl').find_elements_by_tag_name('tr')[3].find_elements_by_tag_name('td')[3].text.replace(",","").replace(" ",""))
        zo3 = (driver.find_element_by_id('bl').find_elements_by_tag_name('tr')[3].find_elements_by_tag_name('td')[5].text.replace(",","").replace(" ",""))
        qo3 = (driver.find_element_by_id('bl').find_elements_by_tag_name('tr')[3].find_elements_by_tag_name('td')[4].text.replace(",","").replace(" ",""))

        bvol = (driver.find_elements_by_tag_name('table')[7].find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].find_element_by_tag_name('div').text.replace(",","").replace(" ",""))
        l = [tno,tvol,tval,py,pf,pmin,pmax,pc,plc,pl,eps,pe,pe_guruh,tmin,tmax,z,mv,pd1,zd1,qd1,po1,zo1,qo1,pd2\
             ,zd2,qd2,po2,zo2,qo2,pd3,zd3,qd3,po3,zo3,qo3]
        l = list(map(convert_to,l))

    #     while not driver.find_element_by_id('e5').text.replace(",","").replace(" ","").isnumeric():
    #         if (time.time() - start_time) > 20:
    #             skip = True
    #             break
    #         pass
    #     if skip:
    #         continue
    #     ct_Buy_CountI = (driver.find_element_by_id('e5').text.replace(",","").replace(" ",""))
    #     ct_Buy_CountN = (driver.find_element_by_id('e6').text.replace(",","").replace(" ",""))
    #     ct_Buy_I_Volume = (driver.find_element_by_id('e0').find_element_by_tag_name('div').text.replace(",","").replace(" ",""))
    #     ct_Buy_N_Volume = (driver.find_element_by_id('e1').find_element_by_tag_name('div').text.replace(",","").replace(" ",""))
    #     ct_Sell_CountI = (driver.find_element_by_id('e8').text.replace(",","").replace(" ",""))
    #     ct_Sell_CountN = (driver.find_element_by_id('e9').text.replace(",","").replace(" ",""))
    #     ct_Sell_I_Volume = (driver.find_element_by_id('e3').find_element_by_tag_name('div').text.replace(",","").replace(" ",""))
    #     ct_Sell_N_Volume = (driver.find_element_by_id('e4').find_element_by_tag_name('div').text.replace(",","").replace(" ",""))

        driver.find_element_by_id('tabs').find_element_by_tag_name('div').find_element_by_tag_name('ul').find_elements_by_tag_name('li')[12].find_element_by_tag_name('a').click()


        while True:
            try:
                is1 = driver.find_element_by_id('InstPartition5').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
                break
            except:
                if (time.time() - start_time) > 40:
                    driver.get(links[names[i]])
                    driver.find_element_by_id('tabs').find_element_by_tag_name('div').find_element_by_tag_name('ul').find_elements_by_tag_name('li')[12].find_element_by_tag_name('a').click()
                    start_time = time.time()
                    counter += 1
                    if counter > 2:
                        print(names[i],"passed in amar")
                        skip = True                       
                        break

        print("se")
        if skip:
            continue
        counter = 0
        try:
            is1 = driver.find_element_by_id('InstPartition5').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is1  = ''
        try:
            is2 = driver.find_element_by_id('InstPartition5').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is2  = ''
        try:
            is3 = driver.find_element_by_id('InstPartition5').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[3].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is3  = ''
        try:
            is4 = driver.find_element_by_id('InstPartition5').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[4].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is4  = ''
        try:
            is5 = driver.find_element_by_id('InstPartition7').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is5  = ''
        try:
            is6 = driver.find_element_by_id('InstPartition7').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is6  = ''
        try:
            is7 = driver.find_element_by_id('InstPartition7').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[3].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is7  = ''
        try:
            is8 = driver.find_element_by_id('InstPartition7').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[4].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is8  = ''
        try:
            is9 = driver.find_element_by_id('InstPartition4').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is9  = ''
        try:
            is10 = driver.find_element_by_id('InstPartition4').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is10 = ''
        try:
            is11 = driver.find_element_by_id('InstPartition4').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[3].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is11 = ''
        try:
            is12 = driver.find_element_by_id('InstPartition4').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[4].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is12 = ''
        try:
            is13 = driver.find_element_by_id('InstPartition8').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is13 = ''
        try:
            is14 = driver.find_element_by_id('InstPartition8').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is14 = ''
        try:
            is15 = driver.find_element_by_id('InstPartition5').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[5].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is15 = ''
        try:
            is16 = driver.find_element_by_id('InstPartition7').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[5].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is16 = ''
        try:
            is17 = driver.find_element_by_id('InstPartition4').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[5].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is17 = ''
        try:
            is18 = driver.find_element_by_id('InstPartition1').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is18 = ''
        try:
            is19 = driver.find_element_by_id('InstPartition1').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is19 = ''
        try:
            is20 = driver.find_element_by_id('InstPartition1').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[3].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is20 = ''
        try:
            is21 = driver.find_element_by_id('InstPartition1').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[4].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is21 = ''
        try:
            is22 = driver.find_element_by_id('InstPartition1').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[5].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is22 = ''
        try:
            is23 = driver.find_element_by_id('InstPartition1').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[6].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is23 = ''
        try:
            is24 = driver.find_element_by_id('InstPartition3').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is24 = ''
        try:
            is25 = driver.find_element_by_id('InstPartition3').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is25 = ''
        try:
            is26 = driver.find_element_by_id('InstPartition2').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is26 = ''
        try:
            is27 = driver.find_element_by_id('InstPartition2').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is27 = ''
        try:
            is28 = driver.find_element_by_id('InstPartition2').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[3].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is28 = ''
        try:
            is29 = driver.find_element_by_id('InstPartition2').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[4].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is29 = ''
        try:
            is30 = driver.find_element_by_id('InstPartition2').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[5].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is30 = ''
        try:
            is31 = driver.find_element_by_id('InstPartition2').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[6].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is31 = ''
        try:
            is32 = driver.find_element_by_id('InstPartition3').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[3].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is32 = ''
        try:
            is33 = driver.find_element_by_id('InstPartition3').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[4].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is33 = ''
        try:
            is34 = driver.find_element_by_id('InstPartition3').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[5].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is34 = ''
        try:
            is35 = driver.find_element_by_id('InstPartition3').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[6].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is35 = ''
        try:
            is36 = driver.find_element_by_id('InstPartition6').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is36 = ''
        try:
            is37 = driver.find_element_by_id('InstPartition6').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is37 = ''
        try:
            is38 = driver.find_element_by_id('InstPartition9').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is38 = ''
        try:
            is39 = driver.find_element_by_id('InstPartition9').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is39 = ''
        try:
            is40 = driver.find_element_by_id('InstPartition9').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[3].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is40 = ''
        try:
            is41 = driver.find_element_by_id('InstPartition9').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[4].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is41 = ''
        try:
            is42 = driver.find_element_by_id('InstPartition9').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[5].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is42 = ''
        try:
            is43 = driver.find_element_by_id('InstPartition9').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[6].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is43 = ''
        try:
            is44 = driver.find_element_by_id('InstPartition9').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[7].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is44 = ''
        try:
            is45 = driver.find_element_by_id('InstPartition9').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[8].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is45 = ''
        try:
            is46 = driver.find_element_by_id('InstPartition9').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[9].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is46 = ''
        try:
            is47 = driver.find_element_by_id('InstPartition9').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[10].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is47 = ''
        try:
            is48 = driver.find_element_by_id('InstPartition9').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[11].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is48 = ''
        try:
            is49 = driver.find_element_by_id('InstPartition9').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[12].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is49 = ''
        try:
            is50 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is50 = ''
        try:
            is51 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is51 = ''
        try:
            is52 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[3].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is52 = ''
        try:
            is53 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[4].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is53 = ''
        try:
            is54 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[5].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is54 = ''
        try:
            is55 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[6].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is55 = ''
        try:
            is56 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[7].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is56 = ''
        try:
            is57 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[8].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is57 = ''
        try:
            is58 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[9].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is58 = ''
        try:
            is59 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[10].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is59 = ''
        try:
            is60 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[11].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is60 = ''
        try:
            is61 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[12].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is61 = ''
        try:
            is62 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[13].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is62 = ''
        try:
            is63 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[14].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is63 = ''
        try:
            is64 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[15].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is64 = ''
        try:
            is65 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[16].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is65 = ''
        try:
            is66 = driver.find_element_by_id('InstPartition10').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is66 = ''
        try:
            is67 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is67 = ''
        try:
            is68 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[3].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is68 = ''
        try:
            is69 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[4].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is69 = ''
        try:
            is70 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[17].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is70 = ''
        try:
            is71 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[18].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is71 = ''
        try:
            is72 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[19].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is72 = ''
        try:
            is73 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[20].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is73 = ''
        try:
            is74 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[21].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is74 = ''
        try:
            is75 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[22].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is75 = ''
        try:
            is76 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[23].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is76 = ''
        try:
            is77 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[24].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is77 = ''
        try:
            is78 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[25].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is78 = ''
        try:
            is79 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[26].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is79 = ''
        try:
            is80 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[27].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is80 = ''
        try:
            is81 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[28].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is81 = ''
        try:
            is82 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[29].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is82 = ''
        try:
            is83 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[30].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is83 = ''
        try:
            is84 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[31].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is84 = ''
        try:
            is85 = driver.find_element_by_id('InstPartition11').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[32].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is85 = ''
        try:
            is86 = driver.find_element_by_id('InstPartition10').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[5].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is86 = ''
        try:
            is87 = driver.find_element_by_id('InstPartition10').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[6].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is87 = ''
        try:
            is88 = driver.find_element_by_id('InstPartition10').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[7].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is88 = ''
        try:
            is89 = driver.find_element_by_id('InstPartition10').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[8].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').find_element_by_tag_name('div').text.replace(",","").replace(" ","")
        except:
            is89 = ''

        driver.find_element_by_id('tabs').find_element_by_tag_name('div').find_element_by_tag_name('ul').find_elements_by_tag_name('li')[9].find_element_by_tag_name('a').click()
        while True:
            try:
                is1_forget = driver.find_element_by_id('PureData').find_element_by_tag_name('table').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[0].text
                break
            except:
                if (time.time() - start_time) > 40:
                    driver.get(links[names[i]])
                    driver.find_element_by_id('tabs').find_element_by_tag_name('div').find_element_by_tag_name('ul').find_elements_by_tag_name('li')[9].find_element_by_tag_name('a').click()
                    start_time = time.time()
                    counter += 1
                    if counter > 2:
                        print(names[i],"passed in sahamdaran")
                        skip = True                       
                        break
                pass
        sahamdaran = []
        counter = 0
        if skip:
            continue
        for k in range(len(driver.find_element_by_id('PureData').find_element_by_tag_name('table').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr'))):
            sahamdaran.append(driver.find_element_by_id('PureData').find_element_by_tag_name('table').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[k].text)
        sahamdaran = json.dumps(sahamdaran)
        f = open(test_txt_dir,'r')
        x = str(f.read()).split(",")
        for k in range(1,90):
            x.append("is" + str(k))
        x.append("sahamdaran")
        x.append("miangin_hajme_mah")
        h = []
        for item in x:
            h.append(eval(item))
        df = pandas.DataFrame(columns = x , data = [h])
        df.to_csv(buffer_data_dir + names[i] + ".csv")
        print(i,"/",len(links))
        print("--- %s seconds ---" % (time.time() - start_time_initial))
        gc.collect()

#start_update()   
for i in range(3):
    while True:
        try:
            start_update()
            break
        except:
            pass

#os.system('shutdown -s')


