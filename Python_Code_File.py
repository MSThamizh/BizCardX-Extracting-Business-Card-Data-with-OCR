import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import easyocr
from PIL import Image, ImageDraw
import pandas as pd
import numpy as np
import re
import io

# Create Table
connection = mysql.connector.connect(host='localhost',user='root',password='SQL@2023',
                                     database='bizcard_data',auth_plugin='mysql_native_password')
mycursor = connection.cursor()

query = ''' create table if not exists bizcard_info ( Name varchar(255) PRIMARY KEY,
                                                        Designation varchar(255),
                                                        Company_Name varchar(255),
                                                        Contact_Number_1 varchar(255),
                                                        Contact_Number_2 varchar(255),
                                                        Email varchar(255),
                                                        Website varchar(255),
                                                        Area text,
                                                        City varchar(255),
                                                        State varchar(255),
                                                        Pincode varchar(255),
                                                        Image_Data BLOB) '''
mycursor.execute(query)

# Show Uploaded Image
def img_op(img_path):
    image = Image.open(img_path) 
    return image

def highlight_img_op(image):
    image = image.convert("RGB")
    reader = easyocr.Reader(['en'])
    np_image = np.array(image)
    img_text = reader.readtext(np_image)
    draw = ImageDraw.Draw(image)
    for (bbox, text, prob) in img_text:
        top_left = (int(bbox[0][0]), int(bbox[0][1]))  
        bottom_right = (int(bbox[2][0]), int(bbox[2][1])) 
        draw.rectangle([top_left, bottom_right], outline='red', width=2)    
    return image

# Image to Text
def img_text_op(image):
    reader = easyocr.Reader(['en'])
    image = np.array(image)
    img_text = reader.readtext(image, detail = 0)   
    return img_text

# Extracting the Text from Image
def extract_text(img_text):
    extract_text_dict = {
        'Name':None,
        'Designation':None,
        'Company_Name':None,
        'Contact_Number_1':None,
        'Contact_Number_2':None,
        'Email':None,
        'Website':None,
        'Area':None,
        'City':None,
        'State':None,
        'Pincode':None
    }
    extract_text_dict['Name'] = img_text[0]
    extract_text_dict['Designation'] = img_text[1]

    Contact_Numbers=[]
    Address_Parts=[]
    Company_Name=[]
    for i in img_text:   
        if re.search(r'(\+\d{1,3})?\s?\(?\d{1,4}\)?[\s.-]?\d{3}[\s.-]?\d{4}', i):       
            Contact_Numbers.append(i)
            if len(Contact_Numbers)>1:
                extract_text_dict["Contact_Number_1"] = Contact_Numbers[0]
                extract_text_dict["Contact_Number_2"] = Contact_Numbers[1]
            else:
                extract_text_dict["Contact_Number_1"] = Contact_Numbers[0]   
        elif '@' in i:
            extract_text_dict['Email'] = i        
        elif 'www' in i.lower() or '.com' in i.lower():
            extract_text_dict["Website"] = i.lower().replace('www ','www.') 
        elif re.search(r'([A-Za-z]+)\s*(\d{6})', i) or re.search(r'\d{6}', i):
            Address_Parts.append(i)
            for item in Address_Parts:
                if re.findall(r'\d+', item):
                    extract_text_dict["Pincode"] = [re.findall(r'\d+', item)[0]][0]
                    if re.findall(r'(?i)\b(?:Andhra Pradesh|AP|Arunachal Pradesh|AR|Assam|AS|Bihar|BR|Chhattisgarh|CG|Goa|GA|Gujarat|GJ|Haryana|HR|Himachal Pradesh|HP|Jharkhand|JH|Karnataka|KA|Kerala|KL|Madhya Pradesh|MP|Maharashtra|MH|Manipur|MN|Meghalaya|ML|Mizoram|MZ|Nagaland|NL|Odisha|OR|Punjab|PB|Rajasthan|RJ|Sikkim|SK|TamilNadu|Tamil Nadu|TN|Telangana|TG|Tripura|TR|Uttar Pradesh|UP|Uttarakhand|UK|West Bengal|WB|Andaman and Nicobar Islands|AN|Chandigarh|CH|Dadra and Nagar Haveli and Daman and Diu|DN|Lakshadweep|LD|Delhi|DL|Puducherry|PY)\b', item):
                        extract_text_dict["State"] = [re.findall(r'(?i)\b(?:Andhra Pradesh|AP|Arunachal Pradesh|AR|Assam|AS|Bihar|BR|Chhattisgarh|CG|Goa|GA|Gujarat|GJ|Haryana|HR|Himachal Pradesh|HP|Jharkhand|JH|Karnataka|KA|Kerala|KL|Madhya Pradesh|MP|Maharashtra|MH|Manipur|MN|Meghalaya|ML|Mizoram|MZ|Nagaland|NL|Odisha|OR|Punjab|PB|Rajasthan|RJ|Sikkim|SK|TamilNadu|Tamil Nadu|TN|Telangana|TG|Tripura|TR|Uttar Pradesh|UP|Uttarakhand|UK|West Bengal|WB|Andaman and Nicobar Islands|AN|Chandigarh|CH|Dadra and Nagar Haveli and Daman and Diu|DN|Lakshadweep|LD|Delhi|DL|Puducherry|PY)\b', item)[0]][0]       
        elif re.findall(r'(?i)\b(?:Andhra Pradesh|AP|Arunachal Pradesh|AR|Assam|AS|Bihar|BR|Chhattisgarh|CG|Goa|GA|Gujarat|GJ|Haryana|HR|Himachal Pradesh|HP|Jharkhand|JH|Karnataka|KA|Kerala|KL|Madhya Pradesh|MP|Maharashtra|MH|Manipur|MN|Meghalaya|ML|Mizoram|MZ|Nagaland|NL|Odisha|OR|Punjab|PB|Rajasthan|RJ|Sikkim|SK|TamilNadu|Tamil Nadu|TN|Telangana|TG|Tripura|TR|Uttar Pradesh|UP|Uttarakhand|UK|West Bengal|WB|Andaman and Nicobar Islands|AN|Chandigarh|CH|Dadra and Nagar Haveli and Daman and Diu|DN|Lakshadweep|LD|Delhi|DL|Puducherry|PY)\b', i):         
            extract_text_dict["State"] = [re.findall(r'(?i)\b(?:Andhra Pradesh|AP|Arunachal Pradesh|AR|Assam|AS|Bihar|BR|Chhattisgarh|CG|Goa|GA|Gujarat|GJ|Haryana|HR|Himachal Pradesh|HP|Jharkhand|JH|Karnataka|KA|Kerala|KL|Madhya Pradesh|MP|Maharashtra|MH|Manipur|MN|Meghalaya|ML|Mizoram|MZ|Nagaland|NL|Odisha|OR|Punjab|PB|Rajasthan|RJ|Sikkim|SK|TamilNadu|Tamil Nadu|TN|Telangana|TG|Tripura|TR|Uttar Pradesh|UP|Uttarakhand|UK|West Bengal|WB|Andaman and Nicobar Islands|AN|Chandigarh|CH|Dadra and Nagar Haveli and Daman and Diu|DN|Lakshadweep|LD|Delhi|DL|Puducherry|PY)\b', i)[0]][0]
            extract_text_dict["Area"] = i.split(',')[0].strip() 
            extract_text_dict["City"] = i.split(',')[-2].split(';')[0].strip() 
        elif re.search(r'([A-Za-z\s]+)',i) and re.search(r'\d',i):
            if len(i.split(',')) > 1:
                extract_text_dict["Area"] = i.split(',')[0].strip()
                extract_text_dict["City"] = i.split(',')[1].split(';')[0].strip()
            else:
                extract_text_dict["Area"] = i.split(',')[0].strip()
        elif re.search(r'St ',i) or re.search(r'St',i):
            extract_text_dict['Area'] += ' ' + i.split(',')[0].strip()        
        elif re.search(r',',i) :
            extract_text_dict["City"] = i.split(',')[0].strip()       
        else:
            Company_Name.append(i)
            if len(Company_Name) > 2:
                extract_text_dict['Company_Name'] = ' '.join(Company_Name[2:])
            else:
                extract_text_dict['Company_Name'] = ' '.join(Company_Name)
    return extract_text_dict

# Convert to Dataframe
def extracted_dataframe(extract_text_dict):
    extracted_text = []
    extracted_text.append(extract_text_dict)
    df_extracted_info=pd.DataFrame(extracted_text)
    return df_extracted_info

def image_byte_df(image):
    image_bytes = io.BytesIO()
    img = image
    img.save(image_bytes, format='PNG')
    image_bytes = image_bytes.getvalue()
    
    data = [{'Image_Data':image_bytes}]
    df_image_byte=pd.DataFrame(data)
    return df_image_byte

# Show Extracted Details
def extracted_info(extract_text_dict):
    multiline = f'''
    **Name:** {extract_text_dict['Name']}  
    **Designation:** {extract_text_dict['Designation']}  
    **Contact Number-1:** {extract_text_dict['Contact_Number_1']}  
    **Contact Number-2:** {extract_text_dict['Contact_Number_2']}  
    **Email:** {extract_text_dict['Email']}  
    **Website:** {extract_text_dict['Website']}  
    **Area:** {extract_text_dict['Area']}  
    **City:** {extract_text_dict['City']}  
    **State:** {extract_text_dict['State']}  
    **Pincode:** {extract_text_dict['Pincode']}
    '''    
    return multiline

# Storing Data in SQL
def store_sql(df):
    rows=[]
    for index in df.index:
        row = tuple(df.loc[index].values)
        row = tuple([str(d) for d in row])
        rows.append(row)

    insert_query='''insert ignore into bizcard_info 
                    (Name,Designation,Company_Name,Contact_Number_1,Contact_Number_2,Email,Website,
                    Area,City,State,Pincode,Image_Data) 
                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    mycursor.executemany(insert_query,rows)
    connection.commit()   
    return st.success(':green[Business Card Stored Sucessfully]') 

# Showing Records from SQL
def stored_cards():
    mycursor.execute("select * from bizcard_info")
    result = mycursor.fetchall()
    if result:
        df = pd.DataFrame(result,columns=['Name','Designation','Company_Name','Contact_Number_1',
                                      'Contact_Number_2','Email','Website','Area','City','State',
                                      'Pincode','Image_Data'])
    else:
        df = pd.DataFrame(columns=['Name','Designation','Company_Name','Contact_Number_1',
                                      'Contact_Number_2','Email','Website','Area','City','State',
                                      'Pincode','Image_Data'])
    return df

# Showing Records by Name from SQL
def stored_cards_details(name):
    mycursor.execute(f"select * from bizcard_info where Name='{name}'")
    result = mycursor.fetchall()
    if result:
        df = pd.DataFrame(result,columns=['Name','Designation','Company_Name','Contact_Number_1',
                                      'Contact_Number_2','Email','Website','Area','City','State',
                                      'Pincode','Image_Data'])
    else:
        df = pd.DataFrame(columns=['Name','Designation','Company_Name','Contact_Number_1',
                                      'Contact_Number_2','Email','Website','Area','City','State',
                                      'Pincode','Image_Data'])
    return df

# Streamlit path
st.set_page_config(layout='wide')

st.header("""Welcome to the :orange[BizCardX]""")
st.subheader(':blue[Extracting Business Card Data with OCR]')
st.write('''This application provides a simple and efficient way to manage business card data by 
         extracting key information from card images using Optical Character Recognition (OCR) technology. 
         Whether you're looking to digitize your business contacts or streamline the process of organizing 
         business card information, this tool is designed to make the process easier.''')

uploaded_image = st.file_uploader(":red[Upload a Business Card 👇]", type=["jpg", "jpeg", "png"],)
upload_store_button = st.button('Upload & Store Data', use_container_width=True)

if upload_store_button:
    try:
        cols1,cols2 = st.columns(2)        
        with cols1:
            with st.spinner('Uploading Business Card...'):
                image = img_op(uploaded_image)             
                st.image(image, width=450, use_column_width=True)
                st.success(':green[Business Card Uploaded Sucessfully]')
        with cols2:
            with st.spinner('Extracting Business Card...'):
                highlighted_image = highlight_img_op(image)
                st.image(highlighted_image, width=450, use_column_width=True)
                st.success(':green[Business Card Extracted Sucessfully]')        

        with st.spinner('Fetching Details...'):     
            text_img = img_text_op(image)
            text_extract = extract_text(text_img)
            df_text_extract = extracted_dataframe(text_extract)

            info = extracted_info(text_extract)
            #st.markdown(info)

            df1 = extracted_dataframe(text_extract)
            df2 = image_byte_df(image)        
            concat_df = pd.concat([df1,df2],axis= 1)

            if concat_df is not None:
                st.dataframe(concat_df, hide_index=True,
                            column_config={'Company_Name':'Company Name',
                                        'Contact_Number_1':'Contact Number-1',
                                        'Contact_Number_2':'Contact Number-2',
                                        'Image_Data':'Image'}) 

            store_sql(concat_df)
    except:
         st.error('Please Upload a Business Card')
                   
selected_tab = option_menu(menu_title='',options=['Preview', 'Update', 'Delete'],
                           icons=['wallet2', 'pencil', 'trash3'],menu_icon="menu-button-wide-fill",
                           default_index=0,orientation="horizontal")

# Preview Tab
if selected_tab == 'Preview':
    st.write("### Stored Business Cards") 
    df_show_cards = stored_cards()
    if df_show_cards.empty:
        st.warning('No Business Cards Found. Please Upload and Store a New Card.')
    else:
        st.dataframe(df_show_cards, hide_index=True,
                        column_config={'Company_Name':'Company Name',
                                    'Contact_Number_1':'Contact Number-1',
                                    'Contact_Number_2':'Contact Number-2',
                                    'Image_Data':'Image'}) 

# Update Tab
elif selected_tab == 'Update':
    st.write("### Modify the Records")

    df_1 = stored_cards()
    if df_1.empty:
        st.warning('No Records to Modify. Please Upload and Store a New Card.')
    else:
        col1, col2 = st.columns(2)
        with col1:
            name_selection = st.selectbox('**Select the Name**',df_1['Name'])       

        df_2 = stored_cards_details(name_selection)
        col1, col2, col3 = st.columns(3)
    
        with col1:       
            name = st.text_input('**Name**', df_2['Name'][0])
            contact_number_1 = st.text_input('**Contact Number-1**', df_2['Contact_Number_1'][0])
            website = st.text_input('**Website**', df_2['Website'][0])
            state = st.text_input('**State**', df_2['State'][0])
        with col2:  
            designation = st.text_input('**Designation**', df_2['Designation'][0])
            contact_number_2 = st.text_input('**Contact Number-2**', df_2['Contact_Number_2'][0])
            area = st.text_input('**Area**', df_2['Area'][0])
            pincode = st.text_input('**Pincode**', df_2['Pincode'][0])
        with col3:
            company_name = st.text_input('**Company Name**', df_2['Company_Name'][0])
            email = st.text_input('**Email**', df_2['Email'][0])
            city = st.text_input('**City**', df_2['City'][0])
        
        df_3 = pd.DataFrame({
        'Name': [name],
        'Designation': [designation],
        'Company_Name': [company_name],
        'Contact_Number_1': [contact_number_1],
        'Contact_Number_2': [contact_number_2],
        'Email': [email],
        'Website': [website],
        'Area': [area],
        'City': [city],
        'State': [state],
        'Pincode': [pincode]
        })
        
        st.markdown("### Updated Data")
        st.dataframe(df_3, hide_index=True, use_container_width=True,
                        column_config={'Company_Name':'Company Name',
                                    'Contact_Number_1':'Contact Number-1',
                                    'Contact_Number_2':'Contact Number-2'})
        
        update_button = st.button('Update',use_container_width=True)

        update_query = """update bizcard_info set Name = %s,Designation = %s,Company_Name = %s,
        Contact_Number_1 = %s,Contact_Number_2 = %s,Email = %s,Website = %s,Area = %s,City = %s,State = %s,
        Pincode = %s where Name = %s""" 

        updated_values = (name,designation,company_name,contact_number_1,contact_number_2,email,website,
                        area,city,state,pincode,name_selection)
        
        if update_button:
            mycursor.execute(update_query, updated_values)
            connection.commit()
            st.success('Details Updated Successfully')   

# Delete Tab
elif selected_tab == 'Delete':
    st.write("### Delete the Records")
    df_4 = stored_cards()
    if df_4.empty:
        st.warning('No Records to Delete. Please Upload and Store a New Card.')
    else:
        col1, col2 = st.columns(2)
        with col1:
            name_selection = st.selectbox('**Select the Name**',df_4['Name'])

        df_5 = stored_cards_details(name_selection)
        st.dataframe(df_5, hide_index=True, use_container_width=True,
                        column_config={'Company_Name':'Company Name',
                                    'Contact_Number_1':'Contact Number-1',
                                    'Contact_Number_2':'Contact Number-2'})
        
        delete_button = st.button('Delete',use_container_width=True)
        if delete_button:
            delete_query = f"delete from bizcard_info where Name = '{name_selection}'"
            mycursor.execute(delete_query)
            connection.commit()
            st.warning('Records Deleted Successfully')