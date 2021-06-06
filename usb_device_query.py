import requests

def get_vendor_info(VID,PID):    
    try:
        url = "https://the-sz.com/products/usbid/index.php?v="+VID+"&p="+PID+"&n="
        response = requests.get(url, timeout=2.50)        
        #  <div class="usbid-vendor-name"><a href="?v=0x05DC">Lexar Media, Inc.</a></div>
        result_1 = response.text.split('<div class="usbid-vendor-name"><a href="?v=')
        result_1 = result_1[1]        
        result_1 = result_1.split("</a></div>")[0].split('">')[1]
        result_1 = result_1.replace(",","")
    except:
        result_1 = "Error fetching data from website"
        
    try:
        result_2 = response.text.split('<div class="usbid-product-name">')[3].split('</div>')[0]
    except:
        result_2 = "Error fetching data from website"
    
    try:
        result_3 = response.text.split('<div class="usbid-product-name">')[4].split('</div>')[0]
    except:
        result_3 = "Error fetching data from website"
    
    return result_1,result_2,result_3

def parse_vid_pid(line):    
    firstpart = line.split("VID_")
    secondpart = firstpart[1].split("&PID_")
    thirdpart = secondpart[1].split("\\")    
    vid = secondpart[0]
    pid = thirdpart[0]
    serial_num = thirdpart[1]    
    return vid,pid,serial_num

def main():
    #data = "USB\VID_05DC&PID_A81D\AANOW8K0OI6N7AW7"
    with open("device_id.txt","r") as file_object:
        output_lines= []
        output_lines.append("Instance ID,vendor_name,Product Name 1,Product Name 2, VID,PID,S/N\n")        
        lines = file_object.readlines()
        for line in lines:
            try:
                vid , pid, serial_num = parse_vid_pid(line)
                vendor_name1,vendor_name2,vendor_name3 = get_vendor_info(vid,pid)
                output_line = line.strip("\n") + "," +vendor_name1 + "," + vendor_name2 + "," + vendor_name3 + "," + vid + "," + pid + "," + serial_num 
                output_lines.append(output_line)
            except:
                vid , pid, serial_num , vendor_name1,vendor_name2,vendor_name3 = "error","error","error","error","error","error"
                output_line = line.strip("\n") + "," +vendor_name1 + "," + vendor_name2 + "," + vendor_name3 + "," + vid + "," + pid + "," + serial_num 
                output_lines.append(output_line)
                pass
    
    with open("output.csv","a") as file_object2:
        for outputLine in output_lines:
            file_object2.write(outputLine)

def test():
    line = "USB\VID_ABCD&PID_1234\\1312291853131334220303"
    vid,pid,serial_num = parse_vid_pid(line)
    print(vid,pid)
    vendor_name = get_vendor_info(vid,pid)
    print(vendor_name)

main()

