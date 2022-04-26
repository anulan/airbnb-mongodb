from this import d
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pymongo

def main():

    cluster0 = pymongo.MongoClient("mongodb+srv://test:test@cluster0.5zoog.mongodb.net/DSE6200?retryWrites=true&w=majority")

    db = cluster0["DSE6200"]
    #collection = db["CleanSFlisting"]
    collection = db["test"]

	#logo
    st.image('airbnblogo.png', caption=None, width=600, use_column_width=600, clamp=True, channels="RGB", output_format="auto")
    #st.title("Simple streamlit blog")

    menu = ["Create", "Edit", "Query"]
    choice = st.sidebar.selectbox("Menu", menu)




    if choice == "Create":
        
        #st.subheader("Create")
        # creating containers
        header_container = st.container()
        stats_container = st.container()


        with header_container:

            # different levels of text you can include in your app
            st.title("Welcome!")
            # st.header("Welcome!")
            st.subheader("You can add an airbnb place in SF to our database!")
            # st.write("We make it easy for you to find place in San Francisco")

            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Enter place name: ")
                host_name = st.text_input("Enter host name: ")
                id = st.number_input("Enter host ID: ", min_value=1, max_value=99000, step=1)
            with col2:
                # collect room type input using a list of options in a drop down format
                r_type_list = collection.distinct('room_type')
                r_type = st.selectbox('Enter room type: ', r_type_list)  # , key='start_station')

                # Neighbourhoud input using multiple selection
                # st.write('It is possible to select multiple places.')
                n_hood_list = collection.distinct('neighbourhood')
                n_hood = st.selectbox('Enter neighbourhood: ', n_hood_list)  # , key='start_station', default=['Harborside','Marin Light Rail'])

                #Input pirce
                price = st.number_input("Enter price: ", min_value=1, step=1)
        # Adding things inside stats container
        with stats_container:

            # Adding slider option to input number of available days per year
            #st.slider(label, min_value=None, max_value=None, value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False)
            avail_days = st.slider('Enter the number of days the place is available per 365 days a year: ', min_value = 0, max_value = 365, value=None, step=None)

            # Adding slider option to input number of minimum number of nights spent
            # st.slider(label, min_value=None, max_value=None, value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False)
            min_nights = st.slider('Enter the minimum number of nights required to stay in the place: ', min_value=0, max_value=365, value=None, step=None)


            #def create_table():
                #c.execute('CREATE TABLE IF NOT EXISTS datatable( name TEXT, host_name TEXT, neighbourhood TEXT, room_type TEXT, price NUMBER, minimum_nights NUMBER,number_of_reviews NUMBER, availability_365 NUMBER)')


            if st.button("Add place"):
                st.success("Successfully added place: {}".format(name))

                collection.insert_one(
                    {"id" : id,
                     "name": name,
                     "host_name": host_name,
                     "room_type": r_type,
                     "neighbourhood": n_hood,
                     "price": price,
                     "minimum_nights": min_nights,
                     "availability_365":avail_days,
                       }
                    )
                st.write('Check the record you created below.')  # displayed when the button is unclicked




                data = []
                for doc in collection.find().sort("_id", -1).limit(1):
                    data.append(doc)
                df = pd.DataFrame.from_dict(data)
                df = df.iloc[:, 2:]
                # df = df.head()
                df.index = np.arange(1, len(df) + 1)

                if not df.empty:
                    st.dataframe(df)






    elif choice == "Edit":

        st.subheader("Read, Update, Delete")
        # creating containers
        header_container = st.container()
        stats_container = st.container()
        other_container = st.container()


        with header_container:
            st.write(" Below is airbnb data for San Francisco.")

            data = []
            for doc in collection.find().sort("_id", -1):
                data.append(doc)
            df = pd.DataFrame.from_dict(data)
            df = df.iloc[:, 1:]
            # df = df.head()
            df.index = np.arange(1, len(df) + 1)

            if not df.empty:
                st.dataframe(df)

            st.write(" Put ID of the host whose record you want to update below.")
            id = st.number_input("Enter host ID: ", min_value=1, max_value=99000, step=1)
            count = collection.count_documents({"id": id})


            col1, col2 = st.columns(2)
            with col1:
                delete_btn = st.button("Delete")
            
            if delete_btn and count > 0:
                st.success("Successfully deleted a place from our record.")
                try:
                    collection.delete_one( { "id" : id } )
                except:
                    print("Exception occured")

                #collection.deleteOne( id )
            elif delete_btn and count == 0:
                st.error('The requested document doesn\'t exist')

            with col2:
                edit_btn = st.button("Edit")

            if edit_btn and count > 0:
                entry = collection.find_one({"id": id})       
                
                with st.form('Edit'):
                    col3, col4 = st.columns(2)
                    with col3:
                        name = st.text_input("Update place name as: ", value=entry["name"])
                        host_name = st.text_input("Update host name as: ", value=entry["host_name"])
                        new_id = st.number_input("Update host ID as: ", value=entry["id"], min_value=1, max_value=99000, step=1)
                        #submitted1 = st.form_submit_button("Update")
                    with col4:
                        r_type_list = collection.distinct('room_type')
                        r_type = st.selectbox("Update room type as: ", r_type_list, index = r_type_list.index(entry["room_type"]))

                        n_hood = st.text_input("Update neighbourhood as: ", value=entry["neighbourhood"])
                        price = st.number_input("Update price as ", value=entry["price"], min_value=1, step=1)
                        #submitted1 = st.form_submit_button("Update")
                    st.write('Put the updates for the minimum number of nights and available days per week below')
                    min_nights = st.slider('update the minimum number of nights required to stay in the place as: ',
                                min_value=0, max_value=365,
                                value=entry["minimum_nights"], step=None)


                    avail_days = st.slider('Enter the number of days the place is available per 365 days a year: ',
                                    min_value=0,
                                    max_value=365, value=entry["availability_365"], step=None)
                    
                    submitted1 = st.form_submit_button("Update")
                    if submitted1:
                        st.success("Successfully updated place: {}".format(name))

                        collection.update_one({"id": id},
                                            {"$set": {"id": new_id,
                                                        "name": name,
                                                        "host_name": host_name,
                                                        "room_type": r_type,
                                                        "neighbourhood": n_hood,
                                                        "price": price,
                                                        "minimum_nights": min_nights,
                                                        "availability_365": avail_days,
                                                        }}
                                            )

            elif edit_btn and count == 0:
                st.error('The requested document doesn\'t exist')
               

            #if edit_btn:
            #        with st.form('Form1'):
            #            st.selectbox('Select flavor', ['Vanilla', 'Chocolate'], key=1)
            #            st.slider(label='Select intensity', min_value=0, max_value=100, key=4)
            #            submitted1 = st.form_submit_button('Submit 1')






    elif choice == "Query":
        #st.subheader("Query")

        #creating containers
        header_container = st.container()
        stats_container = st.container()
        
        with header_container:

            # different levels of text you can include in your app
            # st.title("Welcome!")
            # st.header("Welcome!")
            st.subheader("We make it easy for you to find place in San Francisco!")
            # st.write("We make it easy for you to find place in San Francisco")


        # Adding things inside stats container
        with stats_container:

            # collect room type input using a list of options in a drop down format
            r_type_list = ['All'] + collection.distinct('room_type')
            r_type = st.selectbox('What type of room are you looking for?', r_type_list)#, key='start_station')


            # Neighbourhoud input using multiple selection
            #st.write('It is possible to select multiple places.')
            n_hood_list = ['All'] + collection.distinct('neighbourhood')
            multi_select = st.multiselect('Which neighbourhoud would you like to check out?  (You can select multiple places.)',n_hood_list)#, key='start_station', default=['Harborside','Marin Light Rail'])

            # Adding slider option for price selection
            max_price = collection.find_one(sort=[("price", pymongo.DESCENDING)])["price"]
            st.write(max_price)
            #st.slider(label, min_value=None, max_value=None, value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False)
            price_value = st.slider('What is the price range you are looking for?', min_value = 0, max_value = int(max_price), value=None, step=None)


            # display results in a table format
            # you can filter/alter the data based on user input and display the results in a plot
            st.write('We suggest the following places for you. Please see all the information for best selection.')
            #st.write('Please see all the information for best selection.')

            if r_type != 'All':
                agg_result = collection.aggregate([
                    { "$match" : {"room_type" : r_type}},
                    { "$match" : { "price": {"$lt": price_value} }},
                    { "$match" : { "neighbourhood": {"$in": multi_select} }}
                ])

            else:
                agg_result = collection.aggregate([
                    { "$match" : { "price": {"$lt": price_value} }},
                    { "$match" : { "neighbourhood": {"$in": multi_select} }}
                ])

            data = []
            for doc in agg_result:
                data.append(doc)
            df = pd.DataFrame.from_dict(data)
            df = df.iloc[: , 2:]
            #df = df.head()
            df.index = np.arange(1, len(df) + 1)

            if not df.empty:
                st.dataframe(df)       
                
if __name__ == '__main__':
    main()



