import streamlit as st
pages = ['Locust Breeding Grounds'] # TODO: Put documentation pages if necessary

st.sidebar.title('Locust Breeding Grounds')
page = st.sidebar.radio("Locust Project", pages) # TODO: Change title (knowing that there are anti-locust centers and that they will have insecticide campaigns, the tools is for them)

filters = [] # TODO: fill in filter values str
option = st.selectbox('Filter', filters)
    if option == filters[0]:
# TODO fill in action
    elif option == filster[1]:
#TODO fill in action
    elif option == filters[2]:
#TODO fill in action

if page == pages[0]:
    st.title("Locust Map, with filters") # Change title
    st.image('.jpg') # Add image if necessary
    # TODO: display map

# Has to have access to predictions for the world on locust and display fetching the coordinates and chip size
