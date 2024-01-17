import pandas as pd
import plotly.express as px #pip install plotly

def get_host_information(df, house_id):
    host_info = df[df['id'] == int(house_id)]
    if not host_info.empty:
        print("\nHost Information:")
        print(host_info[['id', 'host_name', 'host_id', 'host_since']])
    else:
        print(f"\nNo information found for house ID {house_id}.")

def filter_houses_by_budget_and_cleanliness(df, budget):
    df['price'] = pd.to_numeric(df['price'].replace('[\$,]', '', regex=True), errors='coerce')
    budget_houses = df[df['price'] <= budget]
    top_clean_houses = budget_houses.sort_values(by='review_scores_cleanliness', ascending=False).head(5)
    print(f'\nTop 5 clean houses within your budget:\n {top_clean_houses["id"]}')

def get_house_link_by_id(df, house_id):
    if house_id in df['id'].values:
        choosed_house = df[df['id'] == house_id]
        link_house = choosed_house["listing_url"].iloc[0]
        print(f"\nLink to the house: {link_house}")
    else:
        print(f"\nNo information found for house ID {house_id}.")

def filter_houses_by_amenity(df, amenity):
    if any(df['amenities'].str.contains(amenity)):
        wanted_house = df[df['amenities'].str.contains(amenity)]
        print("\nHouses with the specified amenity:")
        print(wanted_house["id"])
    else:
        print(f"\nNo houses found with the specified amenity: {amenity}.")

# Data import
df = pd.read_csv('airbnb_listings.csv')

# Show location of houses
fig = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    hover_data=["id"],
    zoom=6,
)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

# Main loop
while True:
    print("\nOptions:")
    print("1. Get house information")
    print("2. Filter houses by budget and cleanliness")
    print("3. Get house link by ID")
    print("4. Filter houses by amenity")
    print("0. Exit")

    choice = input("Enter your choice (1, 2, 3, 4, or 0): ")

    if choice == '0':
        print("Exiting the program. Goodbye!")
        break
    elif choice == '1':
        house_id = input("Enter the house ID: ")
        if house_id.isdigit() and int(house_id) in df['id'].values:
            get_host_information(df, int(house_id))
        else:
            print("Invalid house ID. Please enter a valid numeric ID.")
    elif choice == '2':
        budget = input("Enter your budget: ")
        if budget.isdigit():
            filter_houses_by_budget_and_cleanliness(df, float(budget))
        else:
            print("Please enter a valid numeric budget.")
    elif choice == '3':
        house_id = input("Enter the house ID: ")
        if house_id.isdigit() and int(house_id) in df['id'].values:
            get_house_link_by_id(df, int(house_id))
        else:
            print("Invalid house ID. Please enter a valid numeric ID.")
    elif choice == '4':
        filter_houses_by_amenity(df, input("Enter the amenity you need: "))
    else:
        print("Invalid choice. Please enter a valid option.")
